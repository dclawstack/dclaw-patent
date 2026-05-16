from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.competitor_watch import CompetitorWatch
from app.repositories.competitor_watch import CompetitorWatchRepository
from app.schemas.competitor_watch import CompetitorWatchCreate, CompetitorWatchRead, CompetitorWatchUpdate, CompetitorWatchList
from app.services.patent_search import search_patentsview

router = APIRouter(prefix="/competitors", tags=["competitors"])


async def get_repo(db: AsyncSession = Depends(get_db)) -> CompetitorWatchRepository:
    return CompetitorWatchRepository(db)


@router.get("", response_model=CompetitorWatchList)
async def list_competitors(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    items, total = await repo.list_all(limit, offset)
    return CompetitorWatchList(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=CompetitorWatchRead, status_code=201)
async def create_competitor(
    data: CompetitorWatchCreate,
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    existing = await repo.get_by_company_name(data.company_name)
    if existing:
        raise HTTPException(status_code=409, detail="Company already on watch list")
    watch = CompetitorWatch(**data.model_dump())
    created = await repo.create(watch)
    return created


@router.get("/{watch_id}", response_model=CompetitorWatchRead)
async def get_competitor(
    watch_id: UUID,
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    watch = await repo.get_by_id(watch_id)
    if not watch:
        raise HTTPException(status_code=404, detail="Competitor watch not found")
    return watch


@router.put("/{watch_id}", response_model=CompetitorWatchRead)
async def update_competitor(
    watch_id: UUID,
    data: CompetitorWatchUpdate,
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    watch = await repo.get_by_id(watch_id)
    if not watch:
        raise HTTPException(status_code=404, detail="Competitor watch not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(watch, field, value)
    await repo.db.commit()
    await repo.db.refresh(watch)
    return watch


@router.delete("/{watch_id}", status_code=204)
async def delete_competitor(
    watch_id: UUID,
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    watch = await repo.get_by_id(watch_id)
    if not watch:
        raise HTTPException(status_code=404, detail="Competitor watch not found")
    await repo.delete(watch)
    return None


@router.get("/{watch_id}/filings", response_model=dict)
async def get_competitor_filings(
    watch_id: UUID,
    limit: int = Query(20, ge=1, le=50),
    repo: CompetitorWatchRepository = Depends(get_repo),
):
    watch = await repo.get_by_id(watch_id)
    if not watch:
        raise HTTPException(status_code=404, detail="Competitor watch not found")
    keywords = watch.technology_keywords or [watch.company_name]
    query = " OR ".join(keywords)
    results = await search_patentsview(query, limit=limit)
    return {
        "company_name": watch.company_name,
        "query": query,
        "results": results,
        "total": len(results),
    }
