"""Tests for legal automation service."""

import pytest
from datetime import datetime, timedelta
from app.services.legal_automation import (
    OfficeActionParser,
    MaintenanceFeeCalculator,
    DeadlineReminderService,
)


class TestOfficeActionParser:
    """Test office action parsing."""

    def test_extract_deadline_us_months(self):
        """Test US deadline extraction from months."""
        text = "The applicant is required to respond within 3 months from the date of mailing."
        deadline = OfficeActionParser.extract_deadline(text, "US")
        assert deadline is not None
        assert isinstance(deadline, datetime)

    def test_extract_deadline_ep(self):
        """Test EP deadline extraction."""
        text = "The applicant must respond within 4 months from notification."
        deadline = OfficeActionParser.extract_deadline(text, "EP")
        assert deadline is not None

    def test_extract_office_action_type_first_examination(self):
        """Test classification of first examination report."""
        text = "This is the first examination report from the USPTO..."
        action_type = OfficeActionParser.extract_office_action_type(text)
        assert action_type == "first examination report"

    def test_extract_office_action_type_final_rejection(self):
        """Test classification of final rejection."""
        text = "This is a final rejection under 35 U.S.C. § 112..."
        action_type = OfficeActionParser.extract_office_action_type(text)
        assert action_type == "final rejection"

    def test_extract_office_action_type_allowance(self):
        """Test classification of allowance."""
        text = "Notice of allowance and fees due..."
        action_type = OfficeActionParser.extract_office_action_type(text)
        assert action_type == "allowance"

    def test_extract_rejections(self):
        """Test extraction of claim rejections."""
        text = "Claims 1, 2, 3 are rejected under 35 U.S.C. § 103 as obvious."
        rejections = OfficeActionParser.extract_rejections(text)
        assert len(rejections) > 0
        assert rejections[0]["claims"] == [1, 2, 3]

    def test_extract_requirements(self):
        """Test extraction of applicant requirements."""
        text = """The applicant is required to:
        1. Provide a detailed explanation of the amendments.
        2. Submit a declaration under 37 CFR 1.132."""
        requirements = OfficeActionParser.extract_requirements(text)
        assert len(requirements) >= 1

    def test_unknown_action_type(self):
        """Test handling of unknown action type."""
        text = "Some random patent document"
        action_type = OfficeActionParser.extract_office_action_type(text)
        assert action_type == "unknown"


class TestMaintenanceFeeCalculator:
    """Test maintenance fee calculation."""

    def test_us_maintenance_fees_schedule(self):
        """Test US maintenance fee schedule."""
        issue_date = datetime(2020, 1, 1)
        fees = MaintenanceFeeCalculator.get_maintenance_fees_us(issue_date)
        assert len(fees) == 3  # 3.5, 7.5, 11.5 years
        assert all(f["due_date"] for f in fees)
        assert all(f["grace_period_end"] for f in fees)

    def test_us_fees_structure(self):
        """Test US fee structure includes amount and year."""
        issue_date = datetime(2020, 1, 1)
        fees = MaintenanceFeeCalculator.get_maintenance_fees_us(issue_date)
        assert fees[0]["amount"] == "$1,600 (small entity: $800)"
        assert fees[0]["year"] == "Year 3"  # First fee ~3.5 years

    def test_ep_maintenance_fees_schedule(self):
        """Test EP maintenance fee schedule."""
        pub_date = datetime(2020, 1, 1)
        fees = MaintenanceFeeCalculator.get_maintenance_fees_ep(pub_date)
        assert len(fees) == 18  # Years 3-20
        assert all(f["due_date"] for f in fees)
        assert all(f["grace_period_days"] == 6 for f in fees)

    def test_ep_fees_increasing(self):
        """Test EP fees increase over years."""
        pub_date = datetime(2020, 1, 1)
        fees = MaintenanceFeeCalculator.get_maintenance_fees_ep(pub_date)
        # Extract numeric values from amount strings
        amounts = [int(f["amount"].replace("€", "")) for f in fees]
        # Verify fees generally increase
        assert amounts[-1] > amounts[0]


class TestDeadlineReminderService:
    """Test deadline reminder scheduling."""

    def test_30_day_warning(self):
        """Test 30-day warning generation."""
        due_date = datetime.now() + timedelta(days=30)
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)
        reminder_types = [r["type"] for r in reminders]
        assert "30_day_warning" in reminder_types

    def test_14_day_warning(self):
        """Test 14-day warning generation."""
        due_date = datetime.now() + timedelta(days=14)
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)
        reminder_types = [r["type"] for r in reminders]
        assert "14_day_warning" in reminder_types

    def test_7_day_urgent(self):
        """Test 7-day urgent reminder generation."""
        due_date = datetime.now() + timedelta(days=7)
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)
        reminder_types = [r["type"] for r in reminders]
        assert "7_day_urgent" in reminder_types

    def test_overdue_reminder(self):
        """Test overdue reminder generation."""
        due_date = datetime.now() - timedelta(days=5)
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)
        reminder_types = [r["type"] for r in reminders]
        assert "overdue" in reminder_types

    def test_schedule_reminder_emails(self):
        """Test reminder email scheduling."""
        patent_id = "test-patent-123"
        due_date = datetime.now() + timedelta(days=30)
        schedule = DeadlineReminderService.schedule_reminder_emails(patent_id, due_date)
        assert schedule["patent_id"] == patent_id
        assert schedule["due_date"]
        assert "scheduled_reminders" in schedule
        assert len(schedule["scheduled_reminders"]) > 0

    def test_reminder_priorities(self):
        """Test reminder priority escalation."""
        due_date = datetime.now() + timedelta(days=3)  # Imminent
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)

        # Should have 7-day urgent as highest priority
        priorities = [r["priority"] for r in reminders]
        assert "high" in priorities or "critical" in priorities
