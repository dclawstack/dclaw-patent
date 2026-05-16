from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.competitor_watch import CompetitorWatch
from app.repositories.base_repo import BaseRepository


class CompetitorWatchRepository(BaseRepository[CompetitorWatch]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, CompetitorWatch)

    async def get_by_company_name(self, company_name: str) -> CompetitorWatch | None:
        result = await self.db.execute(
            select(CompetitorWatch).where(CompetitorWatch.company_name == company_name)
        )
        return result.scalar_one_or_none()
