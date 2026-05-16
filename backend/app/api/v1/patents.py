from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.patent import Patent, PatentStatus

router = APIRouter(prefix="/patents", tags=["patents"])


# Schemas
class PatentCreate(BaseModel):
    title: str
    abstract: Optional[str] = None
    assignee: str
    status: Optional[PatentStatus] = PatentStatus.DRAFT
    external_id: Optional[str] = None
    technology_class: Optional[str] = None


class PatentUpdate(BaseModel):
    title: Optional[str] = None
    abstract: Optional[str] = None
    status: Optional[PatentStatus] = None
    claims: Optional[str] = None


class PatentResponse(BaseModel):
    id: UUID
    external_id: Optional[str]
    title: str
    abstract: Optional[str]
    status: PatentStatus
    assignee: str
    technology_class: Optional[str]
    filing_date: Optional[str]
    ai_generated: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=list[PatentResponse])
async def list_patents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[PatentStatus] = None,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
) -> list[Patent]:
    """List patents with pagination and filters."""
    query = select(Patent)

    if status:
        query = query.where(Patent.status == status)

    if search:
        query = query.where(
            (Patent.title.ilike(f"%{search}%")) |
            (Patent.abstract.ilike(f"%{search}%"))
        )

    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=PatentResponse)
async def create_patent(
    patent: PatentCreate,
    session: AsyncSession = Depends(get_session),
) -> Patent:
    """Create a new patent."""
    db_patent = Patent(
        id=uuid4(),
        title=patent.title,
        abstract=patent.abstract,
        assignee=patent.assignee,
        status=patent.status,
        external_id=patent.external_id,
        technology_class=patent.technology_class,
    )
    session.add(db_patent)
    await session.commit()
    await session.refresh(db_patent)
    return db_patent


@router.get("/{patent_id}", response_model=PatentResponse)
async def get_patent(
    patent_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> Patent:
    """Get patent by ID."""
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")
    return patent


@router.put("/{patent_id}", response_model=PatentResponse)
async def update_patent(
    patent_id: UUID,
    patent: PatentUpdate,
    session: AsyncSession = Depends(get_session),
) -> Patent:
    """Update patent."""
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    db_patent = result.scalar_one_or_none()
    if not db_patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    if patent.title is not None:
        db_patent.title = patent.title
    if patent.abstract is not None:
        db_patent.abstract = patent.abstract
    if patent.status is not None:
        db_patent.status = patent.status
    if patent.claims is not None:
        db_patent.claims = patent.claims

    await session.commit()
    await session.refresh(db_patent)
    return db_patent


@router.delete("/{patent_id}")
async def delete_patent(
    patent_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Delete patent."""
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    db_patent = result.scalar_one_or_none()
    if not db_patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    await session.delete(db_patent)
    await session.commit()
    return {"status": "deleted", "id": str(patent_id)}


@router.post("/import")
async def bulk_import_patents(
    file: bytes,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Bulk import patents from USPTO/EPO."""
    # TODO: Implement bulk import from CSV/JSON
    return {"status": "pending", "message": "Bulk import not yet implemented"}
