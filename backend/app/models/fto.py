"""Freedom-to-Operate analysis models."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, DateTime, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import DeclarativeBase


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FTOAnalysis(DeclarativeBase):
    """Freedom-to-Operate analysis for a product."""

    __tablename__ = "fto_analyses"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_description: Mapped[Text] = mapped_column(Text, nullable=False)
    technology_areas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list
    risk_level: Mapped[RiskLevel] = mapped_column(default=RiskLevel.MEDIUM)
    risk_score: Mapped[float] = mapped_column(default=5.0)  # 1-10 scale
    blocking_patents: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # List of blocking patent refs
    recommendations: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # List of design-around suggestions
    confidence_score: Mapped[float] = mapped_column(default=0.5)  # 0-1 confidence in analysis
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<FTOAnalysis(id={self.id}, product='{self.product_name}', risk={self.risk_level})>"
