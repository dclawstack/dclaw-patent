from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class PatentStatus(str, Enum):
    DRAFT = "draft"
    FILED = "filed"
    PROSECUTION = "prosecution"
    ISSUED = "issued"
    ABANDONED = "abandoned"
    EXPIRED = "expired"


class Patent(DeclarativeBase):
    __tablename__ = "patents"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    external_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    abstract: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    claims: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[PatentStatus] = mapped_column(SQLEnum(PatentStatus), default=PatentStatus.DRAFT)
    filing_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    publication_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    issue_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    assignee: Mapped[str] = mapped_column(String(255), nullable=False)
    technology_class: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # IPC/CPC code
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    dockets: Mapped[list["Docket"]] = relationship("Docket", back_populates="patent", cascade="all, delete-orphan")
    inventors: Mapped[list["Inventor"]] = relationship("Inventor", secondary="patent_inventors", back_populates="patents")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="patent", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Patent(id={self.id}, title='{self.title}', status={self.status})>"
