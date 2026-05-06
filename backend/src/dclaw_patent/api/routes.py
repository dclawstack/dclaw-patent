from fastapi import APIRouter
from datetime import datetime
from uuid import uuid4
import random
from dclaw_patent.models import PatentSearch, PatentCreate

router = APIRouter()

@router.post("/searches", response_model=PatentSearch)
async def create_item(payload: PatentCreate):
    return PatentSearch(
        id=str(uuid4()),
        description=payload.description,
        similar_patents_count=random.randint(0, 50),
        novelty_score=random.randint(1, 100),
        filing_recommendation="Recommended with claims refinement",
        created_at=datetime.utcnow(),
    )

@router.get("/searches/{search_id}/citations")
async def get_item(search_id: str):
    return [{"patent_id": "US12345678", "title": "Thermal management in batteries"}, {"patent_id": "US87654321", "title": "Liquid cooling for EVs"}, {"patent_id": "US11223344", "title": "Battery pack heat dissipation"}]
