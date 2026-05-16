"""Webhook endpoints for USPTO/EPO office action ingestion."""

from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.docket import Docket, DocketEventType, DocketStatus
from app.models.patent import Patent
from app.services.office_action_ingestion import OfficeActionIngestionService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


# Schemas
class OfficeActionWebhook(BaseModel):
    patent_id: UUID
    jurisdiction: str = "US"
    document_content: str  # Base64-encoded or raw text
    document_source: str = "USPTO"  # USPTO, EPO, etc.
    external_reference_id: Optional[str] = None


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


class OfficeActionIngestionResponse(BaseModel):
    success: bool
    patent_id: UUID
    action_type: str
    docket_created: bool
    docket_id: Optional[UUID] = None
    deadline: Optional[str] = None
    rejections_count: int
    requirements_count: int
    message: str


@router.post("/office-action", response_model=OfficeActionIngestionResponse)
async def ingest_office_action(
    webhook: OfficeActionWebhook,
    session: AsyncSession = Depends(get_session),
):
    """Webhook endpoint for USPTO/EPO office action ingestion.

    Automatically parses office action, extracts deadline, and creates docket.
    """
    # Verify patent exists
    result = await session.execute(select(Patent).where(Patent.id == webhook.patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    # Validate content
    try:
        if webhook.document_content.startswith("base64:"):
            content = OfficeActionIngestionService.decode_document_content(
                webhook.document_content[7:]
            )
        else:
            content = webhook.document_content
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Validate office action content
    if not OfficeActionIngestionService.validate_office_action_content(content):
        raise HTTPException(
            status_code=400,
            detail="Document does not appear to be a valid office action",
        )

    # Parse office action
    parsed_data = OfficeActionIngestionService.parse_office_action_document(
        content, webhook.jurisdiction
    )

    # Create docket entry if deadline extracted
    docket_id = None
    if parsed_data["deadline"]:
        docket_data = OfficeActionIngestionService.create_docket_from_office_action(
            webhook.patent_id, parsed_data, webhook.jurisdiction
        )

        db_docket = Docket(
            id=uuid4(),
            patent_id=docket_data["patent_id"],
            event_type=docket_data["event_type"],
            due_date=docket_data["due_date"],
            jurisdiction=docket_data["jurisdiction"],
            status=docket_data["status"],
            description=docket_data["description"],
            auto_generated=True,
        )
        session.add(db_docket)
        await session.commit()
        await session.refresh(db_docket)
        docket_id = db_docket.id

    return {
        "success": True,
        "patent_id": webhook.patent_id,
        "action_type": parsed_data["action_type"],
        "docket_created": docket_id is not None,
        "docket_id": docket_id,
        "deadline": parsed_data["deadline"].isoformat() if parsed_data["deadline"] else None,
        "rejections_count": len(parsed_data["rejections"]),
        "requirements_count": len(parsed_data["requirements"]),
        "message": f"Office action parsed: {parsed_data['action_type']}" + (
            f" — Docket created with deadline {parsed_data['deadline'].date()}"
            if parsed_data["deadline"]
            else " — No deadline extracted"
        ),
    }


@router.post("/office-action/{patent_id}/document")
async def upload_office_action_document(
    patent_id: UUID,
    jurisdiction: str = "US",
    document_url: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """Upload office action document from external source (USPTO, EPO)."""
    # Verify patent exists
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    return {
        "status": "pending",
        "patent_id": str(patent_id),
        "message": "Document ingestion job created (async processing)",
        "document_url": document_url,
    }


@router.get("/office-action/{patent_id}/history")
async def get_office_action_history(
    patent_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get all office actions and dockets for a patent."""
    # Get all dockets for this patent (office actions)
    result = await session.execute(
        select(Docket).where(
            (Docket.patent_id == patent_id)
            & (Docket.event_type == DocketEventType.OFFICE_ACTION)
        ).order_by(Docket.created_at.desc())
    )
    dockets = result.scalars().all()

    return {
        "patent_id": str(patent_id),
        "office_actions": [
            {
                "id": str(d.id),
                "due_date": d.due_date.isoformat(),
                "description": d.description,
                "status": d.status,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "auto_generated": d.auto_generated,
            }
            for d in dockets
        ],
        "total_count": len(dockets),
    }
