"""Patent landscape visualization and analysis."""

from typing import Optional
from collections import defaultdict


class PatentLandscapeAnalyzer:
    """Analyze patent landscapes and generate visualization data."""

    @staticmethod
    def cluster_by_technology(patents: list[dict], tech_field: Optional[str] = None) -> dict:
        """Cluster patents by technology class (IPC codes)."""
        clusters = defaultdict(list)

        for patent in patents:
            tech_class = patent.get("technology_class", "Uncategorized")
            clusters[tech_class].append(patent)

        # Convert to bubble data
        bubble_data = []
        for tech_class, class_patents in clusters.items():
            bubble_data.append({
                "name": tech_class,
                "value": len(class_patents),  # Bubble size
                "patents": len(class_patents),
                "assignees": len(set(p.get("assignee", "") for p in class_patents)),
                "recent": max(p.get("filing_date", "") for p in class_patents) if class_patents else "",
            })

        return {
            "clusters": sorted(bubble_data, key=lambda x: x["value"], reverse=True),
            "total_patents": len(patents),
            "total_clusters": len(clusters),
        }

    @staticmethod
    def identify_white_spaces(patents: list[dict], threshold: int = 10) -> list[dict]:
        """Identify uncrowded technology areas (white spaces)."""
        tech_counts = defaultdict(int)

        for patent in patents:
            tech_class = patent.get("technology_class", "Uncategorized")
            tech_counts[tech_class] += 1

        white_spaces = [
            {
                "technology": tech,
                "patent_count": count,
                "crowding": "low" if count < threshold else "medium",
                "opportunity": "high" if count < threshold / 2 else "medium",
            }
            for tech, count in tech_counts.items()
            if count < threshold
        ]

        return sorted(white_spaces, key=lambda x: x["patent_count"])

    @staticmethod
    def analyze_competitors(patents: list[dict]) -> dict:
        """Analyze competitive landscape by assignee."""
        assignee_stats = defaultdict(lambda: {
            "patents": 0,
            "technology_areas": set(),
            "recent_filing": None,
        })

        for patent in patents:
            assignee = patent.get("assignee", "Unknown")
            assignee_stats[assignee]["patents"] += 1
            if patent.get("technology_class"):
                assignee_stats[assignee]["technology_areas"].add(patent["technology_class"])
            filing_date = patent.get("filing_date", "")
            if not assignee_stats[assignee]["recent_filing"] or filing_date > assignee_stats[assignee]["recent_filing"]:
                assignee_stats[assignee]["recent_filing"] = filing_date

        # Convert sets to lists for JSON serialization
        competitors = [
            {
                "assignee": assignee,
                "patent_count": stats["patents"],
                "technology_areas": list(stats["technology_areas"]),
                "recent_filing": stats["recent_filing"],
                "market_share": f"{(stats['patents'] / len(patents) * 100):.1f}%",
            }
            for assignee, stats in assignee_stats.items()
        ]

        return {
            "total_assignees": len(competitors),
            "top_competitors": sorted(competitors, key=lambda x: x["patent_count"], reverse=True)[:10],
            "landscape": competitors,
        }

    @staticmethod
    def trend_analysis(patents: list[dict], years: int = 5) -> dict:
        """Analyze patent filing trends over time."""
        from datetime import datetime, timedelta

        year_stats = defaultdict(lambda: {
            "count": 0,
            "technologies": defaultdict(int),
        })

        for patent in patents:
            filing_date = patent.get("filing_date", "")
            if filing_date:
                try:
                    year = filing_date[:4]
                    year_stats[year]["count"] += 1
                    tech = patent.get("technology_class", "Unknown")
                    year_stats[year]["technologies"][tech] += 1
                except (ValueError, IndexError):
                    pass

        trends = [
            {
                "year": year,
                "patent_count": stats["count"],
                "top_technology": max(stats["technologies"].items(), key=lambda x: x[1])[0]
                if stats["technologies"] else "Unknown",
            }
            for year, stats in sorted(year_stats.items())
        ]

        return {
            "trend_data": trends,
            "growth_rate": calculate_cagr([t["patent_count"] for t in trends]),
            "hottest_area": find_hottest_area(year_stats),
        }


def calculate_cagr(values: list[int]) -> float:
    """Calculate Compound Annual Growth Rate."""
    if len(values) < 2 or values[0] == 0:
        return 0.0

    return ((values[-1] / values[0]) ** (1 / (len(values) - 1)) - 1) * 100


def find_hottest_area(year_stats: dict) -> dict:
    """Find the technology area with highest growth."""
    all_techs = defaultdict(int)

    for year, stats in year_stats.items():
        for tech, count in stats["technologies"].items():
            all_techs[tech] += count

    if all_techs:
        hottest = max(all_techs.items(), key=lambda x: x[1])
        return {
            "technology": hottest[0],
            "filings": hottest[1],
            "momentum": "high",
        }

    return {"technology": "N/A", "filings": 0, "momentum": "low"}
