import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class CompetitorWatch(Base):
    __tablename__ = "competitor_watches"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(256), nullable=False)
    technology_keywords: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True, default=list)
    last_scan_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CompetitorWatch(id={self.id}, company={self.company_name})>"
