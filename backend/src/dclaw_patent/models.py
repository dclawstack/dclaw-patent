from pydantic import BaseModel
from datetime import datetime
from typing import List

class PatentSearch(BaseModel):
    id: str
    description: str
    similar_patents_count: int
    novelty_score: int
    filing_recommendation: str
    created_at: datetime

class PatentCreate(BaseModel):
    description: str
