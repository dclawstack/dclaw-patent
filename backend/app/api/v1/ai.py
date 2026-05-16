from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.ai import (
    PatentSearchRequest,
    PatentSearchResponse,
    PatentSearchResult,
    SimilarPatentsResponse,
    DraftClaimsRequest,
    DraftClaimsResponse,
    DraftedClaim,
    ExaminerPredictionRequest,
    ExaminerPredictionResponse,
)
from app.services.patent_search import search_patentsview, semantic_search_patents, find_similar_patents
import random

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/patent-search", response_model=PatentSearchResponse)
async def ai_patent_search(
    req: PatentSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    # Run both external and semantic search in parallel
    pv_results = await search_patentsview(req.query, limit=req.limit)
    local_results = await semantic_search_patents(db, req.query, limit=req.limit)

    # Merge and dedupe by patent_number, preferring local with distance scoring
    seen = set()
    merged = []
    for r in local_results:
        key = r.get("patent_number") or r.get("id")
        if key and key not in seen:
            seen.add(key)
            # Convert distance to relevance score (closer = higher score)
            distance = r.get("distance") or 1.0
            score = max(0.0, 1.0 - distance)
            merged.append(PatentSearchResult(
                id=r.get("id"),
                patent_number=r.get("patent_number"),
                title=r.get("title"),
                abstract=r.get("abstract"),
                status=r.get("status"),
                jurisdiction=r.get("jurisdiction"),
                relevance_score=round(score, 3),
                distance=round(distance, 4) if distance else None,
                source=r.get("source", "semantic"),
            ))

    for r in pv_results:
        key = r.get("source_patent_number")
        if key and key not in seen:
            seen.add(key)
            merged.append(PatentSearchResult(
                patent_number=r.get("source_patent_number"),
                title=r.get("source_title"),
                abstract=r.get("abstract"),
                date=r.get("date"),
                source=r.get("source", "patentsview"),
            ))

    return PatentSearchResponse(query=req.query, results=merged, total=len(merged))


@router.post("/similar-patents/{patent_id}", response_model=SimilarPatentsResponse)
async def similar_patents(
    patent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    results = await find_similar_patents(db, patent_id, limit=10)
    mapped = [
        PatentSearchResult(
            id=r.get("id"),
            patent_number=r.get("patent_number"),
            title=r.get("title"),
            abstract=r.get("abstract"),
            status=r.get("status"),
            jurisdiction=r.get("jurisdiction"),
            relevance_score=round(max(0.0, 1.0 - (r.get("distance") or 1.0)), 3),
            distance=round(r.get("distance"), 4) if r.get("distance") else None,
            source=r.get("source", "similar"),
        )
        for r in results
    ]
    return SimilarPatentsResponse(patent_id=str(patent_id), results=mapped)


@router.post("/draft-claims", response_model=DraftClaimsResponse)
async def draft_claims(req: DraftClaimsRequest):
    # Stub: deterministic pseudo-claims based on description keywords
    desc = req.invention_description.lower()
    keywords = [w for w in desc.split() if len(w) > 5][:5] or ["device", "system", "method"]
    claims = []
    for i in range(req.num_claims):
        kw = keywords[i % len(keywords)]
        if i == 0:
            text = f"A {kw} comprising: a first component configured to receive an input signal; and a second component operatively coupled to the first component and configured to process the input signal to generate an output."
        else:
            text = f"The {kw} of claim {i}, wherein the second component further comprises a processing module adapted to perform real-time analysis."
        claims.append(DraftedClaim(claim_number=i + 1, claim_text=text))
    return DraftClaimsResponse(
        claims=claims,
        notes="These are AI-suggested draft claims based on your disclosure. Please review with your patent attorney.",
    )


@router.post("/examiner-prediction/{patent_id}", response_model=ExaminerPredictionResponse)
async def examiner_prediction(
    patent_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    # Stub: rule-based heuristic
    # In a real implementation, this would use claim length, tech area, USPTO PAIR data
    prob = round(random.uniform(0.45, 0.85), 2)
    confidence = round(random.uniform(0.60, 0.90), 2)
    amendments = [
        "Narrow claim 1 by adding a specific technical limitation.",
        "Add dependent claim referencing a specific embodiment.",
        "Clarify the term 'processing module' to avoid 112(f) issues.",
    ]
    factors = [
        "Claim 1 is broadly drafted in a crowded art area.",
        "Prior art density for this technology class is moderate.",
        "Prosecution history suggests examiner tends to issue 103 rejections.",
    ]
    return ExaminerPredictionResponse(
        patent_id=str(patent_id),
        allowance_probability=prob,
        confidence=confidence,
        suggested_amendments=amendments,
        factors=factors,
    )
