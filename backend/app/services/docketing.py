"""Patent docketing and deadline calculation service."""

from datetime import date, timedelta
from enum import Enum

# US Patent Office deadline rules (simplified)
DEADLINE_RULES = {
    "US": {
        "office_action_response": 3,  # months
        "maintenance_fee_3_5": (3.5, "years"),  # 3.5 years from issue
        "maintenance_fee_7_5": (7.5, "years"),
        "maintenance_fee_11_5": (11.5, "years"),
    },
    "EP": {
        "office_action_response": 4,  # months (extendable)
        "publication": 18,  # months from filing
    },
    "WO": {
        "office_action_response": 4,  # months
        "publication": 18,  # months from filing
    },
    "JP": {
        "office_action_response": 3,  # months
        "publication": 18,  # months from filing
    },
    "CN": {
        "office_action_response": 4,  # months
        "publication": 18,  # months from filing
    },
}


class DocketingService:
    """Service for calculating patent deadlines and managing dockets."""

    @staticmethod
    def calculate_response_deadline(jurisdiction: str, action_date: date) -> date:
        """Calculate office action response deadline."""
        if jurisdiction not in DEADLINE_RULES:
            return action_date + timedelta(days=90)

        months = DEADLINE_RULES[jurisdiction].get("office_action_response", 3)
        # Simple calculation: add months (approximate as days)
        days = months * 30
        return action_date + timedelta(days=days)

    @staticmethod
    def calculate_maintenance_fee_dates(jurisdiction: str, issue_date: date) -> list[date]:
        """Calculate maintenance fee due dates."""
        if jurisdiction != "US":
            return []

        fees = []
        # US: fees due at 3.5, 7.5, and 11.5 years
        fees.append(issue_date + timedelta(days=int(3.5 * 365)))
        fees.append(issue_date + timedelta(days=int(7.5 * 365)))
        fees.append(issue_date + timedelta(days=int(11.5 * 365)))
        return fees

    @staticmethod
    def get_urgency_level(due_date: date, today: date = None) -> str:
        """Determine urgency level (red/yellow/green)."""
        if today is None:
            today = date.today()

        days_remaining = (due_date - today).days
        if days_remaining < 0:
            return "overdue"
        elif days_remaining < 30:
            return "urgent"  # red
        elif days_remaining < 60:
            return "warning"  # yellow
        else:
            return "ok"  # green

    @staticmethod
    def parse_office_action_pdf(pdf_text: str) -> dict:
        """Extract deadline info from office action PDF (stub)."""
        # TODO: Implement PDF parsing with pypdf or similar
        return {
            "action_type": "office_action",
            "requirements": [],
            "drawing_objections": False,
        }


class DeadlineCalculator:
    """Calculate country-specific patent deadlines."""

    def __init__(self):
        self.docketing = DocketingService()

    def calculate_all_deadlines(self, patent_id: str, filing_date: date, issue_date: date = None, jurisdiction: str = "US") -> list[dict]:
        """Calculate all relevant deadlines for a patent."""
        deadlines = []

        # Publication deadline (18 months from filing)
        pub_deadline = filing_date + timedelta(days=18 * 30)
        deadlines.append({
            "event_type": "publication",
            "due_date": pub_deadline,
            "description": "Patent publication expected",
        })

        if issue_date:
            # Maintenance fees (US only)
            if jurisdiction == "US":
                maintenance_dates = self.docketing.calculate_maintenance_fee_dates(jurisdiction, issue_date)
                for i, fee_date in enumerate(maintenance_dates, 1):
                    deadlines.append({
                        "event_type": "maintenance_fee",
                        "due_date": fee_date,
                        "description": f"Maintenance fee {i} due",
                    })

        return deadlines
