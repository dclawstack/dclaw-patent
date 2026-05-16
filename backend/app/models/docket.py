from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Date, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class DocketEventType(str, Enum):
    OFFICE_ACTION = "office_action"
    RESPONSE_DEADLINE = "response_deadline"
    MAINTENANCE_FEE = "maintenance_fee"
    PUBLICATION = "publication"
    ISSUANCE = "issuance"
    APPEAL = "appeal"
    CUSTOM = "custom"


class DocketStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class Docket(DeclarativeBase):
    __tablename__ = "dockets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    patent_id: Mapped[UUID] = mapped_column(ForeignKey("patents.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[DocketEventType] = mapped_column(SQLEnum(DocketEventType), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(10), default="US")  # US, EP, WO, JP, CN, IN, etc.
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[DocketStatus] = mapped_column(SQLEnum(DocketStatus), default=DocketStatus.PENDING)
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patent: Mapped["Patent"] = relationship("Patent", back_populates="dockets")

    def __repr__(self) -> str:
        return f"<Docket(id={self.id}, event_type={self.event_type}, due_date={self.due_date}, status={self.status})>"
