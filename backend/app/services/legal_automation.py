"""Legal automation service for USPTO/EPO office action processing."""

import re
from datetime import datetime, timedelta
from typing import Optional


class OfficeActionParser:
    """Parse and extract information from office action documents."""

    @staticmethod
    def extract_deadline(office_action_text: str, jurisdiction: str = "US") -> Optional[datetime]:
        """Extract response deadline from office action."""
        if jurisdiction == "US":
            # US: Look for "3 months from date of mailing"
            patterns = [
                r"(\d+)\s+months?\s+(?:from|after)\s+(?:the\s+)?date\s+(?:of\s+mailing|hereof)",
                r"(?:by|on\s+or\s+before)\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})",
            ]

            for pattern in patterns:
                match = re.search(pattern, office_action_text, re.IGNORECASE)
                if match:
                    months = int(match.group(1)) if pattern == patterns[0] else 3
                    return datetime.now() + timedelta(days=months * 30)

        elif jurisdiction == "EP":
            # EP: "4 months from date of notification"
            pattern = r"(\d+)\s+months?\s+(?:from|after)\s+(?:notification|mailing)"
            match = re.search(pattern, office_action_text, re.IGNORECASE)
            if match:
                months = int(match.group(1))
                return datetime.now() + timedelta(days=months * 30)

        return None

    @staticmethod
    def extract_office_action_type(office_action_text: str) -> str:
        """Classify the type of office action."""
        office_action_types = {
            "first examination report": r"first\s+examination\s+report|initial\s+office\s+action",
            "further office action": r"further\s+office\s+action|second\s+office\s+action",
            "restriction requirement": r"restriction\s+requirement",
            "final rejection": r"final\s+rejection",
            "allowance": r"notice\s+of\s+allowance|allowance",
            "appeal": r"patent\s+application\s+appeal",
        }

        for action_type, pattern in office_action_types.items():
            if re.search(pattern, office_action_text, re.IGNORECASE):
                return action_type

        return "unknown"

    @staticmethod
    def extract_rejections(office_action_text: str) -> list[dict]:
        """Extract rejection claims from office action."""
        rejections = []

        # Pattern: "Claims X, Y, Z are rejected under..."
        pattern = r"Claims?\s+([\d\s,]+)\s+(?:is|are)\s+rejected\s+under\s+([^.]+)"
        matches = re.finditer(pattern, office_action_text, re.IGNORECASE)

        for match in matches:
            claims = [int(c.strip()) for c in match.group(1).split(",") if c.strip().isdigit()]
            reason = match.group(2).strip()
            rejections.append({
                "claims": claims,
                "reason": reason,
            })

        return rejections

    @staticmethod
    def extract_requirements(office_action_text: str) -> list[str]:
        """Extract examiner requirements from office action."""
        requirements = []

        # Pattern: "The applicant is required to..."
        pattern = r"(?:applicant|applicants?|inventor)\s+(?:is|are)\s+required\s+to\s+([^.]+)"
        matches = re.finditer(pattern, office_action_text, re.IGNORECASE)

        for match in matches:
            requirements.append(match.group(1).strip())

        return requirements


class MaintenanceFeeCalculator:
    """Calculate maintenance fee due dates."""

    # US maintenance fee schedule: 3.5, 7.5, 11.5 years from issue date
    US_MAINTENANCE_SCHEDULE = [3.5, 7.5, 11.5]

    @staticmethod
    def get_maintenance_fees_us(issue_date: datetime) -> list[dict]:
        """Get US maintenance fee due dates."""
        fees = []

        for year_fraction in MaintenanceFeeCalculator.US_MAINTENANCE_SCHEDULE:
            due_date = issue_date + timedelta(days=int(year_fraction * 365))
            grace_period_end = due_date + timedelta(days=180)

            fees.append({
                "due_date": due_date.isoformat(),
                "grace_period_end": grace_period_end.isoformat(),
                "amount": "$1,600 (small entity: $800)",  # Placeholder
                "year": f"Year {int(year_fraction)}",
            })

        return fees

    @staticmethod
    def get_maintenance_fees_ep(publication_date: datetime) -> list[dict]:
        """Get EP maintenance fee schedule (annual from year 3)."""
        fees = []

        # EP: Annual fees from publication + 2 years (starting year 3)
        for year in range(3, 21):  # Typically 20 years
            due_date = publication_date + timedelta(days=(year * 365))
            fees.append({
                "due_date": due_date.isoformat(),
                "grace_period_days": 6,  # 6 months grace period
                "amount": f"€{300 + (year - 3) * 50}",  # Placeholder increasing schedule
                "year": f"Year {year}",
            })

        return fees


class DeadlineReminderService:
    """Generate deadline reminders at strategic intervals."""

    @staticmethod
    def get_reminders_for_deadline(due_date: datetime) -> list[dict]:
        """Generate reminders at 30, 14, and 7 days before deadline."""
        reminders = []
        today = datetime.now().date()
        due_day = due_date.date() if isinstance(due_date, datetime) else due_date

        days_until = (due_day - today).days

        # 30 days before
        if 28 <= days_until <= 32:
            reminders.append({
                "type": "30_day_warning",
                "days_until": days_until,
                "priority": "low",
                "message": f"Deadline in {days_until} days",
            })

        # 14 days before
        if 12 <= days_until <= 16:
            reminders.append({
                "type": "14_day_warning",
                "days_until": days_until,
                "priority": "medium",
                "message": f"Deadline in {days_until} days - action required",
            })

        # 7 days before
        if 5 <= days_until <= 9:
            reminders.append({
                "type": "7_day_urgent",
                "days_until": days_until,
                "priority": "high",
                "message": f"URGENT: Deadline in {days_until} days",
            })

        # Overdue
        if days_until < 0:
            reminders.append({
                "type": "overdue",
                "days_overdue": abs(days_until),
                "priority": "critical",
                "message": f"OVERDUE by {abs(days_until)} days",
            })

        return reminders

    @staticmethod
    def schedule_reminder_emails(patent_id: str, due_date: datetime) -> dict:
        """Schedule reminder emails at key intervals."""
        reminders = DeadlineReminderService.get_reminders_for_deadline(due_date)

        schedule = {
            "patent_id": patent_id,
            "due_date": due_date.isoformat(),
            "scheduled_reminders": [
                {
                    "reminder_type": r["type"],
                    "send_date": (due_date - timedelta(days=30)).isoformat() if r["type"] == "30_day_warning" else
                                 (due_date - timedelta(days=14)).isoformat() if r["type"] == "14_day_warning" else
                                 (due_date - timedelta(days=7)).isoformat() if r["type"] == "7_day_urgent" else
                                 due_date.isoformat(),
                    "priority": r["priority"],
                }
                for r in reminders
            ],
        }

        return schedule
