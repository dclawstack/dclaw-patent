from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.patent import Patent
from app.services.patent_ai import PatentCopilot, ClaimDraftingAssistant, PatentQualityScorer
from app.services.prior_art import PatentSearchService, PriorArtAnalyzer

router = APIRouter(prefix="/ai", tags=["ai"])


# Schemas
class PatentSearchRequest(BaseModel):
    query: str
    limit: int = 10


class PatentSearchResponse(BaseModel):
    id: UUID
    title: str
    relevance_score: float
    abstract: Optional[str]


class ClaimDraftingRequest(BaseModel):
    disclosure_id: UUID


class ClaimDraftingResponse(BaseModel):
    disclosure_id: UUID
    claims_draft: str
    variants: list[str]
    status: str


class AbstractDraftingRequest(BaseModel):
    description: str


class SimilarPatentsRequest(BaseModel):
    patent_id: UUID
    limit: int = 5


class FTOAnalysisRequest(BaseModel):
    product_description: str
    technology_areas: Optional[list[str]] = None


class FTOAnalysisResponse(BaseModel):
    risk_level: str  # low, medium, high
    risk_score: float
    blocking_patents: list[dict]
    recommendations: list[str]


# Endpoints
@router.post("/patent-search", response_model=list[PatentSearchResponse])
async def search_patents(
    request: PatentSearchRequest,
    session: AsyncSession = Depends(get_session),
):
    """Search patents (keyword + embedding-based)."""
    results = await PatentSearchService.search_combined(
        request.query,
        jurisdictions=["US", "EP"],
        limit=request.limit,
    )
    return results


@router.post("/draft-claims", response_model=ClaimDraftingResponse)
async def draft_claims(
    request: ClaimDraftingRequest,
    session: AsyncSession = Depends(get_session),
):
    """Generate claims from invention disclosure."""
    from app.models.disclosure import InventionDisclosure

    # Get disclosure
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == request.disclosure_id)
    )
    disclosure = result.scalar_one_or_none()
    if not disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")

    # Generate claims
    variants = ClaimDraftingAssistant.draft_claims_from_disclosure(
        disclosure.description,
        num_variants=3,
    )

    return {
        "disclosure_id": request.disclosure_id,
        "claims_draft": variants[0] if variants else "",
        "variants": variants,
        "status": "generated",
    }


@router.post("/draft-abstract")
async def draft_abstract(
    request: AbstractDraftingRequest,
    session: AsyncSession = Depends(get_session),
):
    """Generate abstract from description."""
    abstract = ClaimDraftingAssistant.draft_abstract_from_description(request.description)
    return {
        "abstract": abstract,
        "status": "generated",
    }


@router.post("/similar-patents", response_model=list[PatentSearchResponse])
async def find_similar_patents(
    request: SimilarPatentsRequest,
    session: AsyncSession = Depends(get_session),
):
    """Find similar patents using embeddings."""
    # Get patent
    result = await session.execute(select(Patent).where(Patent.id == request.patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    # Find similar
    similar = PatentCopilot.search_similar_patents(
        patent.abstract or patent.title,
        limit=request.limit,
    )
    return similar


@router.post("/fto-analysis", response_model=FTOAnalysisResponse)
async def analyze_fto(
    request: FTOAnalysisRequest,
    session: AsyncSession = Depends(get_session),
):
    """Freedom-to-Operate analysis."""
    # Find potentially blocking patents
    blocking_patents = await PatentSearchService.search_combined(
        request.product_description,
        jurisdictions=["US"],
        limit=5,
    )

    # Analyze FTO
    fto_report = PriorArtAnalyzer.generate_fto_report(
        request.product_description,
        blocking_patents,
    )

    return fto_report


@router.get("/patent-scores/{patent_id}")
async def get_patent_quality_scores(
    patent_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get patent quality/enforceability scores."""
    # Get patent
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    # Score claims
    if not patent.claims:
        return {
            "patent_id": str(patent_id),
            "message": "No claims to score",
            "overall_score": 0,
        }

    scores = PatentQualityScorer.score_claims(str(patent_id), patent.claims)
    return {
        "patent_id": str(patent_id),
        **scores,
    }
