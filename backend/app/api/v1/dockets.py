from typing import Optional
from uuid import UUID, uuid4
from datetime import date

from fastapi import APIRouter, Query, Depends, HTTPException
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
    session: AsyncSession = Depends(get_session),
) -> list[Docket]:
    """List dockets with filters."""
    query = select(Docket)

    if status:
        query = query.where(Docket.status == status)

    if jurisdiction:
        query = query.where(Docket.jurisdiction == jurisdiction)

    query = query.offset(skip).limit(limit)
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
