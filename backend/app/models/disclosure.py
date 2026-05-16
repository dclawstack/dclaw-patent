from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class DisclosureStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    FILED = "filed"


class InventionDisclosure(DeclarativeBase):
    __tablename__ = "invention_disclosures"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    inventor_id: Mapped[UUID] = mapped_column(ForeignKey("inventors.id", ondelete="CASCADE"), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # AI-generated abstract
    claims_draft: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # AI-generated claims
    status: Mapped[DisclosureStatus] = mapped_column(SQLEnum(DisclosureStatus), default=DisclosureStatus.DRAFT)
    ai_assist_used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventor: Mapped["Inventor"] = relationship("Inventor", back_populates="disclosures")

    def __repr__(self) -> str:
        return f"<InventionDisclosure(id={self.id}, title='{self.title}', status={self.status})>"
