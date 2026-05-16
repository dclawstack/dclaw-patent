import uuid
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator


class PatentBase(BaseModel):
    patent_number: str
    title: str
    abstract: str
    claims: List[str]
    description: Optional[str] = None
    filing_date: datetime
    issue_date: Optional[datetime] = None
    status: str = "filed"
    applicant: str
    inventors: Optional[List[str]] = []
    technology_category: Optional[str] = None
    jurisdiction: str = "US"
    extra_metadata: Optional[dict] = {}

    @field_validator("filing_date", "issue_date", mode="after")
    @classmethod
    def _strip_tz(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class PatentCreate(PatentBase):
    pass


class PatentUpdate(BaseModel):
    patent_number: Optional[str] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    claims: Optional[List[str]] = None
    description: Optional[str] = None
    filing_date: Optional[datetime] = None
    issue_date: Optional[datetime] = None
    status: Optional[str] = None
    applicant: Optional[str] = None
    inventors: Optional[List[str]] = None
    technology_category: Optional[str] = None
    jurisdiction: Optional[str] = None
    extra_metadata: Optional[dict] = None

    @field_validator("filing_date", "issue_date", mode="after")
    @classmethod
    def _strip_tz(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class PatentRead(PatentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PatentList(BaseModel):
    items: List[PatentRead]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
