from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.patent import Patent
from app.repositories.patent import PatentRepository
from app.schemas.patent import PatentCreate, PatentRead, PatentUpdate, PatentList

router = APIRouter(tags=["patents"])


async def get_patent_repo(db: AsyncSession = Depends(get_db)) -> PatentRepository:
    return PatentRepository(db)


@router.get("", response_model=PatentList)
async def list_patents(
    status: str | None = Query(None),
    jurisdiction: str | None = Query(None),
    technology_category: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: PatentRepository = Depends(get_patent_repo),
):
    items, total = await repo.list_filtered(status, jurisdiction, technology_category, limit, offset)
    return PatentList(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=PatentRead, status_code=201)
async def create_patent(
    data: PatentCreate,
    repo: PatentRepository = Depends(get_patent_repo),
):
    existing = await repo.get_by_patent_number(data.patent_number)
    if existing:
        raise HTTPException(status_code=409, detail="Patent number already exists")
    patent = Patent(**data.model_dump())
    created = await repo.create(patent)
    return created


@router.get("/{patent_id}", response_model=PatentRead)
async def get_patent(
    patent_id: UUID,
    repo: PatentRepository = Depends(get_patent_repo),
):
    patent = await repo.get_by_id(patent_id)
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")
    return patent


@router.put("/{patent_id}", response_model=PatentRead)
async def update_patent(
    patent_id: UUID,
    data: PatentUpdate,
    repo: PatentRepository = Depends(get_patent_repo),
):
    patent = await repo.get_by_id(patent_id)
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(patent, field, value)
    await repo.db.commit()
    await repo.db.refresh(patent)
    return patent


@router.delete("/{patent_id}", status_code=204)
async def delete_patent(
    patent_id: UUID,
    repo: PatentRepository = Depends(get_patent_repo),
):
    patent = await repo.get_by_id(patent_id)
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")
    await repo.delete(patent)
    return None
