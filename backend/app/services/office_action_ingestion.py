"""Office action webhook ingestion and auto-docketing service."""

from datetime import datetime, timedelta
from uuid import UUID
from pathlib import Path
import base64

from app.models.docket import Docket, DocketEventType, DocketStatus
from app.models.patent import Patent
from app.services.legal_automation import OfficeActionParser, DeadlineReminderService


class OfficeActionIngestionService:
    """Handle incoming office action documents and auto-docket them."""

    @staticmethod
    def parse_office_action_document(document_content: str, jurisdiction: str = "US") -> dict:
        """Parse office action document and extract structured data."""
        action_type = OfficeActionParser.extract_office_action_type(document_content)
        deadline = OfficeActionParser.extract_deadline(document_content, jurisdiction)
        rejections = OfficeActionParser.extract_rejections(document_content)
        requirements = OfficeActionParser.extract_requirements(document_content)

        return {
            "action_type": action_type,
            "deadline": deadline,
            "rejections": rejections,
            "requirements": requirements,
            "raw_text": document_content,
        }

    @staticmethod
    def create_docket_from_office_action(
        patent_id: UUID,
        parsed_data: dict,
        jurisdiction: str = "US",
    ) -> dict:
        """Generate docket entry from parsed office action."""
        deadline = parsed_data["deadline"]
        action_type = parsed_data["action_type"]

        # Map office action type to docket event type
        event_type_map = {
            "first examination report": DocketEventType.OFFICE_ACTION,
            "further office action": DocketEventType.OFFICE_ACTION,
            "restriction requirement": DocketEventType.OFFICE_ACTION,
            "final rejection": DocketEventType.OFFICE_ACTION,
            "allowance": DocketEventType.ALLOWANCE,
            "appeal": DocketEventType.APPEAL,
            "unknown": DocketEventType.OFFICE_ACTION,
        }

        event_type = event_type_map.get(action_type, DocketEventType.OFFICE_ACTION)

        # Build description
        requirements_summary = "; ".join(parsed_data["requirements"][:2]) if parsed_data["requirements"] else "Review required"
        description = f"{action_type.title()} - {requirements_summary}"

        docket_data = {
            "patent_id": patent_id,
            "event_type": event_type,
            "due_date": deadline.date() if deadline else None,
            "jurisdiction": jurisdiction,
            "status": DocketStatus.PENDING,
            "description": description,
            "auto_generated": True,
        }

        return docket_data

    @staticmethod
    def get_reminder_schedule(due_date: datetime) -> list[dict]:
        """Get reminder schedule for the docket deadline."""
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)
        schedule = DeadlineReminderService.schedule_reminder_emails("patent", due_date)
        return schedule.get("scheduled_reminders", [])

    @staticmethod
    def validate_office_action_content(content: str) -> bool:
        """Validate that content appears to be a real office action."""
        required_keywords = ["office", "action", "applicant", "claim"]
        content_lower = content.lower()

        keyword_count = sum(1 for kw in required_keywords if kw in content_lower)
        return keyword_count >= 2 and len(content) > 100

    @staticmethod
    def decode_document_content(document_base64: str) -> str:
        """Decode base64-encoded document content (for API requests)."""
        try:
            decoded = base64.b64decode(document_base64).decode("utf-8")
            return decoded
        except Exception:
            raise ValueError("Invalid base64-encoded document")
