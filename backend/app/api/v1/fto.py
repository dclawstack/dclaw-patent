"""Freedom-to-Operate analysis API endpoints."""

from uuid import UUID, uuid4
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.fto import FTOAnalysis, RiskLevel
from app.services.prior_art import PriorArtAnalyzer

router = APIRouter(prefix="/fto", tags=["fto-analysis"])


# Schemas
class FTOAnalysisCreate(BaseModel):
    product_name: str
    product_description: str
    technology_areas: Optional[list[str]] = None


class FTOAnalysisResponse(BaseModel):
    id: UUID
    product_name: str
    risk_level: RiskLevel
    risk_score: float
    confidence_score: float
    blocking_patents: Optional[list]
    recommendations: Optional[list]
    created_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=list[FTOAnalysisResponse])
async def list_analyses(
    user_id: Optional[str] = Query(None),
    risk_level: Optional[RiskLevel] = None,
    session: AsyncSession = Depends(get_session),
):
    """List FTO analyses for user."""
    query = select(FTOAnalysis)

    if user_id:
        query = query.where(FTOAnalysis.user_id == user_id)

    if risk_level:
        query = query.where(FTOAnalysis.risk_level == risk_level)

    query = query.order_by(FTOAnalysis.created_at.desc())
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=FTOAnalysisResponse)
async def create_fto_analysis(
    analysis: FTOAnalysisCreate,
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    """Create Freedom-to-Operate analysis."""
    # Search for potentially blocking patents
    blocking_patents = await PriorArtAnalyzer().search_blocking_patents(
        analysis.product_description,
        analysis.technology_areas or [],
    )

    # Generate FTO report
    fto_report = PriorArtAnalyzer.generate_fto_report(
        analysis.product_description,
        blocking_patents,
    )

    # Create analysis record
    db_analysis = FTOAnalysis(
        id=uuid4(),
        user_id=user_id,
        product_name=analysis.product_name,
        product_description=analysis.product_description,
        risk_level=RiskLevel(fto_report.get("risk_level", "medium")),
        risk_score=fto_report.get("risk_score", 5.0),
        blocking_patents=fto_report.get("blocking_patents"),
        recommendations=fto_report.get("recommendations"),
        confidence_score=0.7,  # Hardcoded for MVP
    )

    session.add(db_analysis)
    await session.commit()
    await session.refresh(db_analysis)
    return db_analysis


@router.get("/{analysis_id}", response_model=FTOAnalysisResponse)
async def get_fto_analysis(
    analysis_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get FTO analysis by ID."""
    result = await session.execute(select(FTOAnalysis).where(FTOAnalysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.delete("/{analysis_id}")
async def delete_fto_analysis(
    analysis_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Delete FTO analysis."""
    result = await session.execute(select(FTOAnalysis).where(FTOAnalysis.id == analysis_id))
    db_analysis = result.scalar_one_or_none()
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    await session.delete(db_analysis)
    await session.commit()
    return {"status": "deleted", "id": str(analysis_id)}


@router.get("/{analysis_id}/recommendations")
async def get_recommendations(
    analysis_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get design-around recommendations from analysis."""
    result = await session.execute(select(FTOAnalysis).where(FTOAnalysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "analysis_id": str(analysis_id),
        "product_name": analysis.product_name,
        "risk_level": analysis.risk_level.value,
        "blocking_patents": analysis.blocking_patents or [],
        "design_around_suggestions": analysis.recommendations or [],
        "confidence_score": analysis.confidence_score,
    }


@router.post("/{analysis_id}/export")
async def export_fto_report(
    analysis_id: UUID,
    format: str = Query("pdf", regex="^(pdf|docx|json)$"),
    session: AsyncSession = Depends(get_session),
):
    """Export FTO analysis report."""
    result = await session.execute(select(FTOAnalysis).where(FTOAnalysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Stub: in production, generate actual report files
    return {
        "status": "export_pending",
        "format": format,
        "analysis_id": str(analysis_id),
        "message": f"Report export to {format.upper()} not yet implemented",
    }
