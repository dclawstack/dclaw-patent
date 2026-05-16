from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.docket import DocketEvent
from app.repositories.base_repo import BaseRepository


class DocketRepository(BaseRepository[DocketEvent]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DocketEvent)

    async def list_by_patent(self, patent_id: UUID, limit: int = 50, offset: int = 0) -> tuple[list[DocketEvent], int]:
        result = await self.db.execute(
            select(DocketEvent).where(DocketEvent.patent_id == patent_id).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(DocketEvent).where(DocketEvent.patent_id == patent_id)
        )
        total = count_result.scalar() or 0
        return items, total

    async def get_overdue(self, limit: int = 50) -> list[DocketEvent]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        result = await self.db.execute(
            select(DocketEvent)
            .where(DocketEvent.due_date < now)
            .where(DocketEvent.status != "completed")
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_upcoming(self, days: int = 30, limit: int = 50) -> list[DocketEvent]:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        future = now + timedelta(days=days)
        result = await self.db.execute(
            select(DocketEvent)
            .where(DocketEvent.due_date >= now)
            .where(DocketEvent.due_date <= future)
            .where(DocketEvent.status != "completed")
            .limit(limit)
        )
        return list(result.scalars().all())
