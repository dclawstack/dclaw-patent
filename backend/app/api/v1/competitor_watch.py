"""Competitive patent watch API endpoints."""

from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.competitor_watch import CompetitorWatch, CompetitorAlert, WatchStatus

router = APIRouter(prefix="/watch", tags=["competitor-watch"])


# Schemas
class CompetitorWatchCreate(BaseModel):
    competitor_name: str
    jurisdiction: str = "US"
    technology_areas: Optional[list[str]] = None
    alert_frequency: str = "weekly"


class CompetitorWatchUpdate(BaseModel):
    competitor_name: Optional[str] = None
    status: Optional[WatchStatus] = None
    alert_frequency: Optional[str] = None


class CompetitorWatchResponse(BaseModel):
    id: UUID
    competitor_name: str
    jurisdiction: str
    status: WatchStatus
    alert_frequency: str
    last_alert_date: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class CompetitorAlertResponse(BaseModel):
    id: UUID
    patent_title: str
    patent_number: Optional[str]
    filing_date: Optional[str]
    technology_area: Optional[str]
    relevance_score: float
    read: bool
    created_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=list[CompetitorWatchResponse])
async def list_watches(
    user_id: Optional[str] = Query(None),
    status: Optional[WatchStatus] = None,
    session: AsyncSession = Depends(get_session),
):
    """List competitor watches for user."""
    query = select(CompetitorWatch)

    if user_id:
        query = query.where(CompetitorWatch.user_id == user_id)

    if status:
        query = query.where(CompetitorWatch.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=CompetitorWatchResponse)
async def create_watch(
    watch: CompetitorWatchCreate,
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    """Create competitor watch (free tier feature)."""
    db_watch = CompetitorWatch(
        id=uuid4(),
        user_id=user_id,
        competitor_name=watch.competitor_name,
        jurisdiction=watch.jurisdiction,
        alert_frequency=watch.alert_frequency,
    )
    session.add(db_watch)
    await session.commit()
    await session.refresh(db_watch)
    return db_watch


@router.get("/{watch_id}", response_model=CompetitorWatchResponse)
async def get_watch(
    watch_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get watch by ID."""
    result = await session.execute(select(CompetitorWatch).where(CompetitorWatch.id == watch_id))
    watch = result.scalar_one_or_none()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")
    return watch


@router.put("/{watch_id}", response_model=CompetitorWatchResponse)
async def update_watch(
    watch_id: UUID,
    watch: CompetitorWatchUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update watch."""
    result = await session.execute(select(CompetitorWatch).where(CompetitorWatch.id == watch_id))
    db_watch = result.scalar_one_or_none()
    if not db_watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    if watch.competitor_name is not None:
        db_watch.competitor_name = watch.competitor_name
    if watch.status is not None:
        db_watch.status = watch.status
    if watch.alert_frequency is not None:
        db_watch.alert_frequency = watch.alert_frequency

    await session.commit()
    await session.refresh(db_watch)
    return db_watch


@router.delete("/{watch_id}")
async def delete_watch(
    watch_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Delete watch."""
    result = await session.execute(select(CompetitorWatch).where(CompetitorWatch.id == watch_id))
    db_watch = result.scalar_one_or_none()
    if not db_watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    await session.delete(db_watch)
    await session.commit()
    return {"status": "deleted", "id": str(watch_id)}


@router.get("/{watch_id}/alerts", response_model=list[CompetitorAlertResponse])
async def get_watch_alerts(
    watch_id: UUID,
    unread_only: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get alerts for a watch."""
    query = select(CompetitorAlert).where(CompetitorAlert.watch_id == watch_id)

    if unread_only:
        query = query.where(CompetitorAlert.read == False)

    query = query.order_by(CompetitorAlert.created_at.desc()).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/{watch_id}/alerts/{alert_id}/read")
async def mark_alert_read(
    watch_id: UUID,
    alert_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Mark alert as read."""
    result = await session.execute(select(CompetitorAlert).where(CompetitorAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.read = True
    await session.commit()
    return {"status": "marked_read", "alert_id": str(alert_id)}


@router.get("/{watch_id}/summary")
async def get_watch_summary(
    watch_id: UUID,
    days: int = Query(7, ge=1, le=365),
    session: AsyncSession = Depends(get_session),
):
    """Get summary of recent alerts."""
    from datetime import timedelta

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = select(CompetitorAlert).where(
        and_(
            CompetitorAlert.watch_id == watch_id,
            CompetitorAlert.created_at >= cutoff_date,
        )
    )
    result = await session.execute(query)
    alerts = result.scalars().all()

    unread_count = sum(1 for a in alerts if not a.read)
    avg_relevance = sum(a.relevance_score for a in alerts) / len(alerts) if alerts else 0

    return {
        "watch_id": str(watch_id),
        "total_alerts": len(alerts),
        "unread_alerts": unread_count,
        "avg_relevance_score": round(avg_relevance, 2),
        "date_range": f"Last {days} days",
        "top_technologies": list(set(a.technology_area for a in alerts if a.technology_area))[:5],
    }
