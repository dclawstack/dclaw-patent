import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class PriorArt(Base):
    __tablename__ = "prior_arts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    patent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patents.id", ondelete="CASCADE"), nullable=False)
    source_patent_number: Mapped[str] = mapped_column(String(64), nullable=False)
    source_title: Mapped[str] = mapped_column(String(512), nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    claim_mapping: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    analysis_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    patent: Mapped["Patent"] = relationship(back_populates="prior_arts", lazy="selectin")

    def __repr__(self) -> str:
        return f"<PriorArt(id={self.id}, source={self.source_patent_number}, score={self.relevance_score})>"
