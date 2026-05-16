from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class Comment(DeclarativeBase):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    patent_id: Mapped[UUID] = mapped_column(ForeignKey("patents.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)  # User identifier (email or UUID)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    resolved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patent: Mapped["Patent"] = relationship("Patent", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, patent_id={self.patent_id}, resolved={self.resolved})>"
