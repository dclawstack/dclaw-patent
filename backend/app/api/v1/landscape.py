"""Technology landscape visualization API endpoints."""

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.services.landscape import PatentLandscapeAnalyzer

router = APIRouter(prefix="/landscape", tags=["landscape"])


@router.post("/clusters")
async def get_landscape_clusters(
    patents: list[dict] = Query(...),
    tech_field: str = Query(None),
):
    """Get technology clusters (bubble chart data)."""
    clustering = PatentLandscapeAnalyzer.cluster_by_technology(patents, tech_field)
    return {
        "type": "bubble_chart",
        "data": clustering,
    }


@router.post("/white-spaces")
async def identify_white_spaces(
    patents: list[dict] = Query(...),
    threshold: int = Query(10, ge=1, le=50),
):
    """Identify uncrowded technology areas (opportunity areas)."""
    white_spaces = PatentLandscapeAnalyzer.identify_white_spaces(patents, threshold)
    return {
        "type": "white_space_analysis",
        "threshold": threshold,
        "opportunities": white_spaces,
        "high_opportunity_count": sum(1 for ws in white_spaces if ws["opportunity"] == "high"),
    }


@router.post("/competitive-analysis")
async def analyze_competitive_landscape(
    patents: list[dict] = Query(...),
):
    """Analyze competitive landscape by assignee."""
    analysis = PatentLandscapeAnalyzer.analyze_competitors(patents)
    return {
        "type": "competitive_landscape",
        "data": analysis,
    }


@router.post("/trends")
async def get_patent_trends(
    patents: list[dict] = Query(...),
    years: int = Query(5, ge=1, le=20),
):
    """Analyze patent filing trends over time."""
    trends = PatentLandscapeAnalyzer.trend_analysis(patents, years)
    return {
        "type": "trend_analysis",
        "data": trends,
    }


@router.post("/full-landscape")
async def get_full_landscape_analysis(
    patents: list[dict] = Query(...),
):
    """Get comprehensive landscape analysis (all visualizations)."""
    clusters = PatentLandscapeAnalyzer.cluster_by_technology(patents)
    white_spaces = PatentLandscapeAnalyzer.identify_white_spaces(patents)
    competitors = PatentLandscapeAnalyzer.analyze_competitors(patents)
    trends = PatentLandscapeAnalyzer.trend_analysis(patents)

    return {
        "type": "comprehensive_landscape",
        "clustering": clusters,
        "white_spaces": white_spaces,
        "competitive_landscape": competitors,
        "trends": trends,
        "summary": {
            "total_patents": len(patents),
            "technology_diversity": len(clusters["clusters"]),
            "competitive_players": len(competitors["top_competitors"]),
            "growth_trajectory": trends["growth_rate"],
        },
    }
