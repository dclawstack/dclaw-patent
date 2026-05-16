import uuid
from datetime import datetime
from sqlalchemy import String, Text, Date, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class DocketEvent(Base):
    __tablename__ = "docket_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    patent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patents.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(
        Enum("filing", "response_due", "maintenance_fee", "prosecution_update", "custom", name="docket_event_type"),
        nullable=False,
    )
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("pending", "completed", "overdue", name="docket_status"),
        default="pending",
        nullable=False,
    )
    assignee: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    patent: Mapped["Patent"] = relationship(back_populates="docket_events", lazy="selectin")

    def __repr__(self) -> str:
        return f"<DocketEvent(id={self.id}, type={self.event_type}, due={self.due_date})>"
