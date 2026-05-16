"""Tests for office action ingestion service."""

import pytest
import base64
from uuid import uuid4
from app.services.office_action_ingestion import OfficeActionIngestionService
from app.models.docket import DocketEventType


class TestOfficeActionIngestionService:
    """Test office action ingestion service."""

    def test_parse_office_action_document(self):
        """Test office action document parsing."""
        content = """
        OFFICE ACTION

        Claims 1-5 are rejected under 35 U.S.C. § 103 as obvious.

        The applicant is required to respond within 3 months from the date of mailing.

        This is a first examination report.
        """

        parsed = OfficeActionIngestionService.parse_office_action_document(content, "US")

        assert parsed["action_type"] == "first examination report"
        assert parsed["deadline"] is not None
        assert len(parsed["rejections"]) > 0
        assert len(parsed["requirements"]) > 0
        assert parsed["raw_text"] == content

    def test_validate_office_action_content_valid(self):
        """Test validation of valid office action content."""
        content = """
        OFFICE ACTION FROM THE USPTO

        The applicant is required to respond.
        Claims 1 and 2 are rejected under 35 U.S.C. § 103.
        """

        is_valid = OfficeActionIngestionService.validate_office_action_content(content)
        assert is_valid is True

    def test_validate_office_action_content_invalid(self):
        """Test validation of invalid office action content."""
        content = "Just some random text"

        is_valid = OfficeActionIngestionService.validate_office_action_content(content)
        assert is_valid is False

    def test_create_docket_from_office_action(self):
        """Test docket creation from parsed office action."""
        patent_id = uuid4()
        parsed_data = {
            "action_type": "final rejection",
            "deadline": None,
            "rejections": [
                {"claims": [1, 2], "reason": "obvious under § 103"}
            ],
            "requirements": ["Submit detailed explanation"],
            "raw_text": "",
        }

        docket_data = OfficeActionIngestionService.create_docket_from_office_action(
            patent_id, parsed_data, "US"
        )

        assert docket_data["patent_id"] == patent_id
        assert docket_data["event_type"] == DocketEventType.OFFICE_ACTION
        assert docket_data["jurisdiction"] == "US"
        assert docket_data["auto_generated"] is True
        assert "final rejection" in docket_data["description"].lower()

    def test_create_docket_allowance(self):
        """Test docket creation for allowance."""
        patent_id = uuid4()
        parsed_data = {
            "action_type": "allowance",
            "deadline": None,
            "rejections": [],
            "requirements": ["Pay issue fee"],
            "raw_text": "",
        }

        docket_data = OfficeActionIngestionService.create_docket_from_office_action(
            patent_id, parsed_data, "US"
        )

        assert docket_data["event_type"] == DocketEventType.ALLOWANCE

    def test_get_reminder_schedule(self):
        """Test reminder schedule generation."""
        from datetime import datetime, timedelta

        due_date = datetime.now() + timedelta(days=30)
        schedule = OfficeActionIngestionService.get_reminder_schedule(due_date)

        assert isinstance(schedule, list)
        assert len(schedule) > 0
        assert all("reminder_type" in r for r in schedule)
        assert all("send_date" in r for r in schedule)
        assert all("priority" in r for r in schedule)

    def test_decode_document_content_base64(self):
        """Test base64 document decoding."""
        content = "This is a test document"
        encoded = base64.b64encode(content.encode()).decode()

        decoded = OfficeActionIngestionService.decode_document_content(encoded)
        assert decoded == content

    def test_decode_document_content_invalid(self):
        """Test handling of invalid base64."""
        invalid_base64 = "not_valid_base64!!!"

        with pytest.raises(ValueError, match="Invalid base64"):
            OfficeActionIngestionService.decode_document_content(invalid_base64)

    def test_parse_us_deadline(self):
        """Test US-specific deadline parsing."""
        content = """
        OFFICE ACTION

        Deadline: 3 months from the date of mailing.
        This is the initial examination report.
        """

        parsed = OfficeActionIngestionService.parse_office_action_document(content, "US")
        assert parsed["deadline"] is not None

    def test_parse_ep_deadline(self):
        """Test EP-specific deadline parsing."""
        content = """
        EUROPEAN PATENT OFFICE COMMUNICATION

        Response deadline: 4 months from notification.
        """

        parsed = OfficeActionIngestionService.parse_office_action_document(content, "EP")
        assert parsed["deadline"] is not None
