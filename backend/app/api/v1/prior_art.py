from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.prior_art import PriorArt
from app.repositories.prior_art import PriorArtRepository
from app.schemas.prior_art import PriorArtCreate, PriorArtRead, PriorArtUpdate, PriorArtList

router = APIRouter(tags=["prior-art"])


async def get_prior_art_repo(db: AsyncSession = Depends(get_db)) -> PriorArtRepository:
    return PriorArtRepository(db)


@router.get("", response_model=PriorArtList)
async def list_prior_art(
    patent_id: UUID | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: PriorArtRepository = Depends(get_prior_art_repo),
):
    if patent_id:
        items, total = await repo.list_by_patent(patent_id, limit, offset)
    else:
        items, total = await repo.list_all(limit, offset)
    return PriorArtList(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=PriorArtRead, status_code=201)
async def create_prior_art(
    data: PriorArtCreate,
    repo: PriorArtRepository = Depends(get_prior_art_repo),
):
    pa = PriorArt(**data.model_dump())
    created = await repo.create(pa)
    return created


@router.get("/{prior_art_id}", response_model=PriorArtRead)
async def get_prior_art(
    prior_art_id: UUID,
    repo: PriorArtRepository = Depends(get_prior_art_repo),
):
    pa = await repo.get_by_id(prior_art_id)
    if not pa:
        raise HTTPException(status_code=404, detail="Prior art not found")
    return pa


@router.put("/{prior_art_id}", response_model=PriorArtRead)
async def update_prior_art(
    prior_art_id: UUID,
    data: PriorArtUpdate,
    repo: PriorArtRepository = Depends(get_prior_art_repo),
):
    pa = await repo.get_by_id(prior_art_id)
    if not pa:
        raise HTTPException(status_code=404, detail="Prior art not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pa, field, value)
    await repo.db.commit()
    await repo.db.refresh(pa)
    return pa


@router.delete("/{prior_art_id}", status_code=204)
async def delete_prior_art(
    prior_art_id: UUID,
    repo: PriorArtRepository = Depends(get_prior_art_repo),
):
    pa = await repo.get_by_id(prior_art_id)
    if not pa:
        raise HTTPException(status_code=404, detail="Prior art not found")
    await repo.delete(pa)
    return None
