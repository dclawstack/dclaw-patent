import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Date, DateTime, ForeignKey, JSON, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Patent(Base):
    __tablename__ = "patents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    patent_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=False)
    claims: Mapped[dict] = mapped_column(JSON, nullable=False, default=list)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    filing_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    issue_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("drafted", "filed", "prosecution", "issued", "abandoned", "lapsed", name="patent_status"),
        default="filed",
        nullable=False,
    )
    applicant: Mapped[str] = mapped_column(String(256), nullable=False)
    inventors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    technology_category: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    jurisdiction: Mapped[str] = mapped_column(String(16), nullable=False, default="US")
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    docket_events: Mapped[List["DocketEvent"]] = relationship(
        back_populates="patent",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    prior_arts: Mapped[List["PriorArt"]] = relationship(
        back_populates="patent",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Patent(id={self.id}, number={self.patent_number}, title={self.title})>"
