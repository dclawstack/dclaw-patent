"""Legal automation and office action processing API endpoints."""

from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.patent import Patent
from app.services.legal_automation import (
    OfficeActionParser,
    MaintenanceFeeCalculator,
    DeadlineReminderService,
)

router = APIRouter(prefix="/legal-automation", tags=["legal-automation"])


# Schemas
class OfficeActionText(BaseModel):
    text: str
    jurisdiction: str = "US"


class OfficeActionAnalysis(BaseModel):
    action_type: str
    deadline: str | None
    rejections: list[dict]
    requirements: list[str]


class MaintenanceFeesResponse(BaseModel):
    patent_id: UUID
    issue_date: str
    jurisdiction: str
    fees: list[dict]


class ReminderScheduleResponse(BaseModel):
    patent_id: UUID
    due_date: str
    scheduled_reminders: list[dict]


@router.post("/analyze-office-action", response_model=OfficeActionAnalysis)
async def analyze_office_action(
    office_action: OfficeActionText,
):
    """Analyze office action document and extract key information."""
    action_type = OfficeActionParser.extract_office_action_type(office_action.text)
    deadline = OfficeActionParser.extract_deadline(office_action.text, office_action.jurisdiction)
    rejections = OfficeActionParser.extract_rejections(office_action.text)
    requirements = OfficeActionParser.extract_requirements(office_action.text)

    return {
        "action_type": action_type,
        "deadline": deadline.isoformat() if deadline else None,
        "rejections": rejections,
        "requirements": requirements,
    }


@router.get("/maintenance-fees/{patent_id}", response_model=MaintenanceFeesResponse)
async def get_maintenance_fees(
    patent_id: UUID,
    jurisdiction: str = "US",
    session: AsyncSession = Depends(get_session),
):
    """Get maintenance fee schedule for a patent."""
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    if not patent.issue_date:
        raise HTTPException(status_code=400, detail="Patent issue date not set")

    if jurisdiction == "US":
        fees = MaintenanceFeeCalculator.get_maintenance_fees_us(patent.issue_date)
    elif jurisdiction == "EP":
        pub_date = patent.publication_date or patent.filing_date
        fees = MaintenanceFeeCalculator.get_maintenance_fees_ep(pub_date)
    else:
        raise HTTPException(status_code=400, detail="Unsupported jurisdiction")

    return {
        "patent_id": patent_id,
        "issue_date": patent.issue_date.isoformat(),
        "jurisdiction": jurisdiction,
        "fees": fees,
    }


@router.post("/schedule-reminders/{patent_id}", response_model=ReminderScheduleResponse)
async def schedule_reminders(
    patent_id: UUID,
    due_date: str,
    session: AsyncSession = Depends(get_session),
):
    """Schedule deadline reminder notifications."""
    result = await session.execute(select(Patent).where(Patent.id == patent_id))
    patent = result.scalar_one_or_none()
    if not patent:
        raise HTTPException(status_code=404, detail="Patent not found")

    due_datetime = datetime.fromisoformat(due_date)
    schedule = DeadlineReminderService.schedule_reminder_emails(str(patent_id), due_datetime)

    return schedule


@router.post("/get-reminders")
async def get_reminders_for_deadline(
    due_date: str,
):
    """Get applicable reminders for a given deadline."""
    due_datetime = datetime.fromisoformat(due_date)
    reminders = DeadlineReminderService.get_reminders_for_deadline(due_datetime)

    return {
        "due_date": due_date,
        "reminders": reminders,
        "reminder_count": len(reminders),
    }
