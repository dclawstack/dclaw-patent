from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.docket import DocketEvent
from app.repositories.docket import DocketRepository
from app.schemas.docket import DocketEventCreate, DocketEventRead, DocketEventUpdate, DocketEventList, DocketAlerts

router = APIRouter(tags=["dockets"])


async def get_docket_repo(db: AsyncSession = Depends(get_db)) -> DocketRepository:
    return DocketRepository(db)


@router.get("", response_model=DocketEventList)
async def list_dockets(
    patent_id: UUID | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: DocketRepository = Depends(get_docket_repo),
):
    if patent_id:
        items, total = await repo.list_by_patent(patent_id, limit, offset)
    else:
        items, total = await repo.list_all(limit, offset)
    return DocketEventList(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=DocketEventRead, status_code=201)
async def create_docket(
    data: DocketEventCreate,
    repo: DocketRepository = Depends(get_docket_repo),
):
    event = DocketEvent(**data.model_dump())
    created = await repo.create(event)
    return created


@router.get("/{docket_id}", response_model=DocketEventRead)
async def get_docket(
    docket_id: UUID,
    repo: DocketRepository = Depends(get_docket_repo),
):
    event = await repo.get_by_id(docket_id)
    if not event:
        raise HTTPException(status_code=404, detail="Docket event not found")
    return event


@router.put("/{docket_id}", response_model=DocketEventRead)
async def update_docket(
    docket_id: UUID,
    data: DocketEventUpdate,
    repo: DocketRepository = Depends(get_docket_repo),
):
    event = await repo.get_by_id(docket_id)
    if not event:
        raise HTTPException(status_code=404, detail="Docket event not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    await repo.db.commit()
    await repo.db.refresh(event)
    return event


@router.delete("/{docket_id}", status_code=204)
async def delete_docket(
    docket_id: UUID,
    repo: DocketRepository = Depends(get_docket_repo),
):
    event = await repo.get_by_id(docket_id)
    if not event:
        raise HTTPException(status_code=404, detail="Docket event not found")
    await repo.delete(event)
    return None


@router.get("/alerts/summary", response_model=DocketAlerts)
async def get_docket_alerts(
    days: int = Query(30, ge=1, le=365),
    repo: DocketRepository = Depends(get_docket_repo),
):
    urgent = await repo.get_overdue(limit=50)
    upcoming = await repo.get_upcoming(days=days, limit=50)
    return DocketAlerts(urgent=urgent, upcoming=upcoming)
