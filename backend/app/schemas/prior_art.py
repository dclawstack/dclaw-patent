import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PriorArtBase(BaseModel):
    source_patent_number: str
    source_title: str
    relevance_score: float = 0.0
    claim_mapping: Optional[dict] = {}
    analysis_notes: Optional[str] = None


class PriorArtCreate(PriorArtBase):
    patent_id: uuid.UUID


class PriorArtUpdate(BaseModel):
    source_patent_number: Optional[str] = None
    source_title: Optional[str] = None
    relevance_score: Optional[float] = None
    claim_mapping: Optional[dict] = None
    analysis_notes: Optional[str] = None


class PriorArtRead(PriorArtBase):
    id: uuid.UUID
    patent_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PriorArtList(BaseModel):
    items: list[PriorArtRead]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
