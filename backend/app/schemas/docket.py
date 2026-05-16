import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class DocketEventBase(BaseModel):
    event_type: str
    due_date: datetime
    description: str
    status: str = "pending"
    assignee: Optional[str] = None

    @field_validator("due_date", mode="after")
    @classmethod
    def _strip_tz(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class DocketEventCreate(DocketEventBase):
    patent_id: uuid.UUID


class DocketEventUpdate(BaseModel):
    event_type: Optional[str] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None

    @field_validator("due_date", mode="after")
    @classmethod
    def _strip_tz(cls, v):
        if isinstance(v, datetime) and v.tzinfo is not None:
            return v.replace(tzinfo=None)
        return v


class DocketEventRead(DocketEventBase):
    id: uuid.UUID
    patent_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocketEventList(BaseModel):
    items: list[DocketEventRead]
    total: int
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)


class DocketAlerts(BaseModel):
    urgent: list[DocketEventRead]
    upcoming: list[DocketEventRead]

    model_config = ConfigDict(from_attributes=True)
