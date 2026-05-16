"""Invention disclosure endpoints."""

from uuid import UUID, uuid4
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.disclosure import InventionDisclosure, DisclosureStatus
from app.models.patent import Patent
from app.services.patent_ai import ClaimDraftingAssistant

router = APIRouter(prefix="/disclosures", tags=["disclosures"])


# Schemas
class DisclosureCreate(BaseModel):
    title: str
    description: str
    inventor_id: UUID


class DisclosureUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DisclosureStatus] = None
    summary: Optional[str] = None
    claims_draft: Optional[str] = None


class DisclosureResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: DisclosureStatus
    summary: Optional[str]
    claims_draft: Optional[str]
    ai_assist_used: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=list[DisclosureResponse])
async def list_disclosures(
    inventor_id: Optional[UUID] = None,
    status: Optional[DisclosureStatus] = None,
    session: AsyncSession = Depends(get_session),
):
    """List invention disclosures."""
    query = select(InventionDisclosure)

    if inventor_id:
        query = query.where(InventionDisclosure.inventor_id == inventor_id)

    if status:
        query = query.where(InventionDisclosure.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=DisclosureResponse)
async def create_disclosure(
    disclosure: DisclosureCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create invention disclosure."""
    db_disclosure = InventionDisclosure(
        id=uuid4(),
        title=disclosure.title,
        description=disclosure.description,
        inventor_id=disclosure.inventor_id,
    )
    session.add(db_disclosure)
    await session.commit()
    await session.refresh(db_disclosure)
    return db_disclosure


@router.get("/{disclosure_id}", response_model=DisclosureResponse)
async def get_disclosure(
    disclosure_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get disclosure by ID."""
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == disclosure_id)
    )
    disclosure = result.scalar_one_or_none()
    if not disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")
    return disclosure


@router.put("/{disclosure_id}", response_model=DisclosureResponse)
async def update_disclosure(
    disclosure_id: UUID,
    disclosure: DisclosureUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update disclosure."""
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == disclosure_id)
    )
    db_disclosure = result.scalar_one_or_none()
    if not db_disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")

    if disclosure.title is not None:
        db_disclosure.title = disclosure.title
    if disclosure.description is not None:
        db_disclosure.description = disclosure.description
    if disclosure.status is not None:
        db_disclosure.status = disclosure.status
    if disclosure.summary is not None:
        db_disclosure.summary = disclosure.summary
    if disclosure.claims_draft is not None:
        db_disclosure.claims_draft = disclosure.claims_draft

    await session.commit()
    await session.refresh(db_disclosure)
    return db_disclosure


@router.delete("/{disclosure_id}")
async def delete_disclosure(
    disclosure_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Delete disclosure."""
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == disclosure_id)
    )
    db_disclosure = result.scalar_one_or_none()
    if not db_disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")

    await session.delete(db_disclosure)
    await session.commit()
    return {"status": "deleted", "id": str(disclosure_id)}


@router.post("/{disclosure_id}/submit")
async def submit_disclosure(
    disclosure_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Submit disclosure for review."""
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == disclosure_id)
    )
    db_disclosure = result.scalar_one_or_none()
    if not db_disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")

    if db_disclosure.status != DisclosureStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Can only submit draft disclosures")

    db_disclosure.status = DisclosureStatus.SUBMITTED
    await session.commit()
    await session.refresh(db_disclosure)
    return {
        "status": "submitted",
        "disclosure_id": str(disclosure_id),
        "message": "Disclosure submitted for review",
    }


@router.post("/{disclosure_id}/file")
async def file_disclosure(
    disclosure_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """File disclosure as patent application."""
    result = await session.execute(
        select(InventionDisclosure).where(InventionDisclosure.id == disclosure_id)
    )
    db_disclosure = result.scalar_one_or_none()
    if not db_disclosure:
        raise HTTPException(status_code=404, detail="Disclosure not found")

    if db_disclosure.status not in [DisclosureStatus.APPROVED, DisclosureStatus.SUBMITTED]:
        raise HTTPException(status_code=400, detail="Disclosure must be approved to file")

    # Create patent from disclosure
    patent = Patent(
        id=uuid4(),
        title=db_disclosure.title,
        abstract=db_disclosure.summary,
        claims=db_disclosure.claims_draft,
        assignee="TBD",  # Would be populated from user/org
        ai_generated=db_disclosure.ai_assist_used,
    )
    session.add(patent)
    db_disclosure.status = DisclosureStatus.FILED
    await session.commit()
    await session.refresh(db_disclosure)

    return {
        "status": "filed",
        "disclosure_id": str(disclosure_id),
        "patent_id": str(patent.id),
        "message": "Disclosure filed as patent application",
    }
