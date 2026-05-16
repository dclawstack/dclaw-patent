from datetime import datetime
from uuid import UUID

from sqlalchemy import String, DateTime, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import DeclarativeBase

# Association table for Patent-Inventor many-to-many
patent_inventors = Table(
    "patent_inventors",
    DeclarativeBase.metadata,
    ForeignKey("patents.id", ondelete="CASCADE"),
    ForeignKey("inventors.id", ondelete="CASCADE"),
)


class Inventor(DeclarativeBase):
    __tablename__ = "inventors"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=lambda: UUID('00000000-0000-0000-0000-000000000000'))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    organization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patents: Mapped[list["Patent"]] = relationship("Patent", secondary=patent_inventors, back_populates="inventors")
    disclosures: Mapped[list["InventionDisclosure"]] = relationship("InventionDisclosure", back_populates="inventor")

    def __repr__(self) -> str:
        return f"<Inventor(id={self.id}, name='{self.name}', email='{self.email}')>"
