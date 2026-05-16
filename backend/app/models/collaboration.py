"""Real-time collaboration models."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase


class ThreadComment(DeclarativeBase):
    """Comment thread on patents or disclosures."""

    __tablename__ = "thread_comments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    patent_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("patents.id", ondelete="CASCADE"), nullable=True)
    disclosure_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("invention_disclosures.id", ondelete="CASCADE"), nullable=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    mentions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON list of @mentions
    parent_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("thread_comments.id", ondelete="CASCADE"), nullable=True)
    resolved: Mapped[bool] = mapped_column(default=False)
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    replies: Mapped[list["ThreadComment"]] = relationship(
        "ThreadComment",
        remote_side=[id],
        cascade="all, delete-orphan",
        backref="parent"
    )

    def __repr__(self) -> str:
        return f"<ThreadComment(id={self.id}, user='{self.user_name}', resolved={self.resolved})>"


class CommentMention(DeclarativeBase):
    """Track @mentions in comments."""

    __tablename__ = "comment_mentions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    comment_id: Mapped[UUID] = mapped_column(ForeignKey("thread_comments.id", ondelete="CASCADE"), nullable=False)
    mentioned_user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    mentioned_user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<CommentMention(id={self.id}, mentioned='{self.mentioned_user_email}', read={self.read})>"
