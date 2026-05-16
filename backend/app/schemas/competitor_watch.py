import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CompetitorWatchBase(BaseModel):
    company_name: str
    technology_keywords: Optional[List[str]] = []


class CompetitorWatchCreate(CompetitorWatchBase):
    pass


class CompetitorWatchUpdate(BaseModel):
    company_name: Optional[str] = None
    technology_keywords: Optional[List[str]] = None


class CompetitorWatchRead(CompetitorWatchBase):
    id: uuid.UUID
    last_scan_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompetitorWatchList(BaseModel):
    items: List[CompetitorWatchRead]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
