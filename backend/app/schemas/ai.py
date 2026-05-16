import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PatentSearchRequest(BaseModel):
    query: str
    limit: int = 20


class PatentSearchResult(BaseModel):
    id: Optional[str] = None
    patent_number: Optional[str] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    status: Optional[str] = None
    jurisdiction: Optional[str] = None
    relevance_score: Optional[float] = None
    distance: Optional[float] = None
    source: str = "patentsview"
    date: Optional[str] = None


class PatentSearchResponse(BaseModel):
    query: str
    results: List[PatentSearchResult]
    total: int

    model_config = ConfigDict(from_attributes=True)


class SimilarPatentsResponse(BaseModel):
    patent_id: str
    results: List[PatentSearchResult]

    model_config = ConfigDict(from_attributes=True)


class DraftClaimsRequest(BaseModel):
    invention_description: str
    num_claims: int = 5


class DraftedClaim(BaseModel):
    claim_number: int
    claim_text: str


class DraftClaimsResponse(BaseModel):
    claims: List[DraftedClaim]
    notes: str = ""

    model_config = ConfigDict(from_attributes=True)


class ExaminerPredictionRequest(BaseModel):
    patent_id: str


class ExaminerPredictionResponse(BaseModel):
    patent_id: str
    allowance_probability: float
    confidence: float
    suggested_amendments: List[str]
    factors: List[str]

    model_config = ConfigDict(from_attributes=True)
