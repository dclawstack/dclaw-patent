from typing import Optional
from uuid import UUID, uuid4
from datetime import date, datetime, timedelta
from io import StringIO

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.docket import Docket, DocketStatus, DocketEventType
from app.services.docketing import DeadlineCalculator

router = APIRouter(prefix="/dockets", tags=["dockets"])


# Schemas
class DocketCreate(BaseModel):
    patent_id: UUID
    event_type: DocketEventType
    due_date: date
    jurisdiction: str = "US"
    description: Optional[str] = None


class DocketUpdate(BaseModel):
    status: Optional[DocketStatus] = None
    description: Optional[str] = None
    due_date: Optional[date] = None


class DocketResponse(BaseModel):
    id: UUID
    patent_id: UUID
    event_type: DocketEventType
    due_date: str
    jurisdiction: str
    status: DocketStatus
    auto_generated: bool
    created_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=list[DocketResponse])
async def list_dockets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[DocketStatus] = None,
    jurisdiction: Optional[str] = None,
    patent_id: Optional[UUID] = None,
    event_type: Optional[DocketEventType] = None,
    due_date_from: Optional[date] = None,
    due_date_to: Optional[date] = None,
    session: AsyncSession = Depends(get_session),
) -> list[Docket]:
    """List dockets with filters (status, jurisdiction, patent, event type, date range)."""
    query = select(Docket)

    if status:
        query = query.where(Docket.status == status)

    if jurisdiction:
        query = query.where(Docket.jurisdiction == jurisdiction)

    if patent_id:
        query = query.where(Docket.patent_id == patent_id)

    if event_type:
        query = query.where(Docket.event_type == event_type)

    if due_date_from:
        query = query.where(Docket.due_date >= due_date_from)

    if due_date_to:
        query = query.where(Docket.due_date <= due_date_to)

    query = query.offset(skip).limit(limit).order_by(Docket.due_date)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=DocketResponse)
async def create_docket(
    docket: DocketCreate,
    session: AsyncSession = Depends(get_session),
) -> Docket:
    """Create docket entry."""
    db_docket = Docket(
        id=uuid4(),
        patent_id=docket.patent_id,
        event_type=docket.event_type,
        due_date=docket.due_date,
        jurisdiction=docket.jurisdiction,
        description=docket.description,
    )
    session.add(db_docket)
    await session.commit()
    await session.refresh(db_docket)
    return db_docket


@router.put("/{docket_id}", response_model=DocketResponse)
async def update_docket(
    docket_id: UUID,
    docket: DocketUpdate,
    session: AsyncSession = Depends(get_session),
) -> Docket:
    """Update docket status."""
    result = await session.execute(select(Docket).where(Docket.id == docket_id))
    db_docket = result.scalar_one_or_none()
    if not db_docket:
        raise HTTPException(status_code=404, detail="Docket not found")

    if docket.status is not None:
        db_docket.status = docket.status
    if docket.description is not None:
        db_docket.description = docket.description
    if docket.due_date is not None:
        db_docket.due_date = docket.due_date

    await session.commit()
    await session.refresh(db_docket)
    return db_docket


@router.delete("/{docket_id}")
async def delete_docket(
    docket_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Delete docket."""
    result = await session.execute(select(Docket).where(Docket.id == docket_id))
    db_docket = result.scalar_one_or_none()
    if not db_docket:
        raise HTTPException(status_code=404, detail="Docket not found")

    await session.delete(db_docket)
    await session.commit()
    return {"status": "deleted", "id": str(docket_id)}


@router.get("/overdue")
async def get_overdue_dockets(
    session: AsyncSession = Depends(get_session),
) -> list[DocketResponse]:
    """Get overdue dockets (red alerts)."""
    from datetime import date
    today = date.today()
    query = select(Docket).where(
        and_(
            Docket.due_date < today,
            Docket.status != DocketStatus.COMPLETED,
        )
    )
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/upcoming", response_model=list[DocketResponse])
async def get_upcoming_dockets(
    days_ahead: int = Query(30, ge=1, le=365),
    session: AsyncSession = Depends(get_session),
) -> list[Docket]:
    """Get dockets due in the next N days (for urgency color-coding)."""
    today = date.today()
    future_date = today + timedelta(days=days_ahead)
    query = select(Docket).where(
        and_(
            Docket.due_date >= today,
            Docket.due_date <= future_date,
            Docket.status != DocketStatus.COMPLETED,
        )
    ).order_by(Docket.due_date)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/{docket_id}/mark-complete")
async def mark_docket_complete(
    docket_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> DocketResponse:
    """Mark docket as completed."""
    result = await session.execute(select(Docket).where(Docket.id == docket_id))
    db_docket = result.scalar_one_or_none()
    if not db_docket:
        raise HTTPException(status_code=404, detail="Docket not found")

    db_docket.status = DocketStatus.COMPLETED
    await session.commit()
    await session.refresh(db_docket)
    return db_docket


@router.post("/{docket_id}/mark-pending")
async def mark_docket_pending(
    docket_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> DocketResponse:
    """Mark docket as pending (reopen)."""
    result = await session.execute(select(Docket).where(Docket.id == docket_id))
    db_docket = result.scalar_one_or_none()
    if not db_docket:
        raise HTTPException(status_code=404, detail="Docket not found")

    db_docket.status = DocketStatus.PENDING
    await session.commit()
    await session.refresh(db_docket)
    return db_docket


@router.get("/export/csv")
async def export_dockets_csv(
    status: Optional[DocketStatus] = None,
    jurisdiction: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """Export dockets to CSV format."""
    query = select(Docket)

    if status:
        query = query.where(Docket.status == status)

    if jurisdiction:
        query = query.where(Docket.jurisdiction == jurisdiction)

    query = query.order_by(Docket.due_date)
    result = await session.execute(query)
    dockets = result.scalars().all()

    csv_data = StringIO()
    csv_data.write("Patent ID,Event Type,Due Date,Jurisdiction,Status,Description,Created At\n")

    for docket in dockets:
        csv_data.write(
            f"{docket.patent_id},{docket.event_type},{docket.due_date},"
            f"{docket.jurisdiction},{docket.status},{docket.description or ''},\"{docket.created_at}\"\n"
        )

    return StreamingResponse(
        iter([csv_data.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dockets_export.csv"},
    )


@router.get("/export/ical")
async def export_dockets_ical(
    status: Optional[DocketStatus] = None,
    jurisdiction: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """Export dockets to iCalendar format."""
    query = select(Docket)

    if status:
        query = query.where(Docket.status == status)

    if jurisdiction:
        query = query.where(Docket.jurisdiction == jurisdiction)

    query = query.order_by(Docket.due_date)
    result = await session.execute(query)
    dockets = result.scalars().all()

    ical_data = StringIO()
    ical_data.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//DClaw Patent//docket-export//EN\n")

    for docket in dockets:
        due_date_str = docket.due_date.isoformat().replace("-", "")
        ical_data.write(
            f"BEGIN:VEVENT\nDTSTART:{due_date_str}\n"
            f"DTEND:{due_date_str}\nSUMMARY:{docket.event_type} - Patent {docket.patent_id}\n"
            f"DESCRIPTION:{docket.description or 'Docket event'}\nUID:{docket.id}\nEND:VEVENT\n"
        )

    ical_data.write("END:VCALENDAR\n")

    return StreamingResponse(
        iter([ical_data.getvalue()]),
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=dockets_export.ics"},
    )


@router.post("/calculate-deadlines")
async def calculate_deadlines(
    patent_id: UUID,
    jurisdiction: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Calculate deadlines by jurisdiction."""
    from app.models.patent import Patent

    # Get patent
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    # Calculate deadlines
    calculator = DeadlineCalculator()
    deadlines = calculator.calculate_all_deadlines(
        str(patent_id),
        patent.filing_date or date.today(),
        patent.issue_date,
        jurisdiction,
    )

    return {
        "patent_id": str(patent_id),
        "jurisdiction": jurisdiction,
        "deadlines": deadlines,
        "count": len(deadlines),
    }
