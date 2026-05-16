"""Tests for docketing service."""

import pytest
from datetime import date
from app.services.docketing import DocketingService, DeadlineCalculator


class TestDocketingService:
    """Test deadline calculation logic."""

    def test_calculate_response_deadline_us(self):
        """Test US office action response deadline (3 months)."""
        action_date = date(2026, 1, 1)
        deadline = DocketingService.calculate_response_deadline("US", action_date)
        # 3 months ≈ 90 days
        assert (deadline - action_date).days == 90

    def test_calculate_response_deadline_ep(self):
        """Test EP office action response deadline (4 months)."""
        action_date = date(2026, 1, 1)
        deadline = DocketingService.calculate_response_deadline("EP", action_date)
        # 4 months ≈ 120 days
        assert (deadline - action_date).days == 120

    def test_calculate_maintenance_fees_us(self):
        """Test US maintenance fee deadlines (3.5, 7.5, 11.5 years)."""
        issue_date = date(2020, 1, 1)
        fees = DocketingService.calculate_maintenance_fee_dates("US", issue_date)
        assert len(fees) == 3
        # Check approximate years
        assert 1200 < (fees[0] - issue_date).days < 1400  # 3.5 years
        assert 2600 < (fees[1] - issue_date).days < 2800  # 7.5 years
        assert 4000 < (fees[2] - issue_date).days < 4300  # 11.5 years

    def test_get_urgency_level_overdue(self):
        """Test urgency level for overdue dates."""
        today = date(2026, 5, 16)
        due_date = date(2026, 5, 1)
        urgency = DocketingService.get_urgency_level(due_date, today)
        assert urgency == "overdue"

    def test_get_urgency_level_urgent(self):
        """Test urgency level for dates <30 days away."""
        today = date(2026, 5, 16)
        due_date = date(2026, 5, 31)
        urgency = DocketingService.get_urgency_level(due_date, today)
        assert urgency == "urgent"

    def test_get_urgency_level_warning(self):
        """Test urgency level for dates 30-60 days away."""
        today = date(2026, 5, 16)
        due_date = date(2026, 6, 15)
        urgency = DocketingService.get_urgency_level(due_date, today)
        assert urgency == "warning"

    def test_get_urgency_level_ok(self):
        """Test urgency level for dates >60 days away."""
        today = date(2026, 5, 16)
        due_date = date(2026, 8, 1)
        urgency = DocketingService.get_urgency_level(due_date, today)
        assert urgency == "ok"


class TestDeadlineCalculator:
    """Test deadline calculation engine."""

    def test_calculate_all_deadlines(self):
        """Test calculating all relevant deadlines."""
        filing_date = date(2020, 1, 1)
        issue_date = date(2023, 6, 15)
        calculator = DeadlineCalculator()
        deadlines = calculator.calculate_all_deadlines(
            "test-patent", filing_date, issue_date, jurisdiction="US"
        )
        # Should have publication + 3 maintenance fees
        assert len(deadlines) >= 3
        event_types = [d["event_type"] for d in deadlines]
        assert "publication" in event_types
        assert "maintenance_fee" in event_types


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
