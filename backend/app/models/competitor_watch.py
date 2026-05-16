"""Competitive patent watch models."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class WatchStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class CompetitorWatch(DeclarativeBase):
    """Track competitor patent filings."""

    __tablename__ = "competitor_watches"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)  # User email or UUID
    competitor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    assignee_aliases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list of alternative names
    jurisdiction: Mapped[str] = mapped_column(String(10), default="US")  # US, EP, WO, JP, CN, etc.
    technology_areas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list of keywords
    status: Mapped[WatchStatus] = mapped_column(default=WatchStatus.ACTIVE)
    last_alert_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    alert_frequency: Mapped[str] = mapped_column(String(20), default="weekly")  # daily, weekly, monthly
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alerts: Mapped[list["CompetitorAlert"]] = relationship("CompetitorAlert", back_populates="watch", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CompetitorWatch(id={self.id}, competitor='{self.competitor_name}', status={self.status})>"


class CompetitorAlert(DeclarativeBase):
    """Alerts when competitors file new patents."""

    __tablename__ = "competitor_alerts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    watch_id: Mapped[UUID] = mapped_column(ForeignKey("competitor_watches.id", ondelete="CASCADE"), nullable=False)
    patent_title: Mapped[str] = mapped_column(String(512), nullable=False)
    patent_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    filing_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    publication_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    abstract: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technology_area: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    relevance_score: Mapped[float] = mapped_column(default=0.5)  # 0.0-1.0 relevance to watch keywords
    read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    watch: Mapped[CompetitorWatch] = relationship("CompetitorWatch", back_populates="alerts")

    def __repr__(self) -> str:
        return f"<CompetitorAlert(id={self.id}, patent='{self.patent_title}', relevance={self.relevance_score})>"
