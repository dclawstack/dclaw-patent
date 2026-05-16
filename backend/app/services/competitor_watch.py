"""Competitive patent watch service."""

from datetime import datetime, timedelta
from typing import Optional
from app.services.prior_art import PatentSearchService


class CompetitorWatchService:
    """Monitor competitor patent filings."""

    @staticmethod
    async def scan_competitor_patents(
        competitor_names: list[str],
        technology_areas: Optional[list[str]] = None,
        jurisdiction: str = "US",
        days_back: int = 7,
    ) -> list[dict]:
        """Search for recent competitor patents."""
        patents = []

        for competitor in competitor_names:
            # Search for patents by competitor assignee
            results = await PatentSearchService.search_combined(
                query=competitor,
                jurisdictions=[jurisdiction],
                limit=10,
            )

            # Filter by technology area if provided
            if technology_areas:
                results = [
                    p for p in results
                    if any(tech.lower() in p.get("abstract", "").lower() for tech in technology_areas)
                ]

            patents.extend(results)

        return patents

    @staticmethod
    def calculate_relevance_score(
        patent_abstract: str,
        technology_areas: Optional[list[str]] = None,
    ) -> float:
        """Calculate relevance score (0-1) of patent to watched technologies."""
        if not technology_areas or not patent_abstract:
            return 0.5

        abstract_lower = patent_abstract.lower()
        matches = sum(1 for tech in technology_areas if tech.lower() in abstract_lower)

        # Relevance = matches / total keywords, capped at 1.0
        return min(1.0, matches / len(technology_areas))

    @staticmethod
    def format_alert_summary(alerts: list[dict], competitor_name: str) -> str:
        """Format alert summary for notification."""
        count = len(alerts)
        if count == 0:
            return f"No new patents from {competitor_name} this week."

        avg_relevance = sum(a.get("relevance_score", 0.5) for a in alerts) / count
        high_relevance = sum(1 for a in alerts if a.get("relevance_score", 0) > 0.7)

        summary = f"{competitor_name} filed {count} new patent(s) this week.\n"
        summary += f"• Average relevance: {avg_relevance:.1%}\n"
        summary += f"• High-relevance filings: {high_relevance}"

        return summary
