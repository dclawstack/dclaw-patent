from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.patent import Patent
from app.repositories.base_repo import BaseRepository


class PatentRepository(BaseRepository[Patent]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Patent)

    async def get_by_patent_number(self, patent_number: str) -> Patent | None:
        result = await self.db.execute(
            select(Patent).where(Patent.patent_number == patent_number)
        )
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        status: str | None = None,
        jurisdiction: str | None = None,
        technology_category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Patent], int]:
        query = select(Patent)
        count_query = select(func.count()).select_from(Patent)

        if status:
            query = query.where(Patent.status == status)
            count_query = count_query.where(Patent.status == status)
        if jurisdiction:
            query = query.where(Patent.jurisdiction == jurisdiction)
            count_query = count_query.where(Patent.jurisdiction == jurisdiction)
        if technology_category:
            query = query.where(Patent.technology_category == technology_category)
            count_query = count_query.where(Patent.technology_category == technology_category)

        result = await self.db.execute(query.limit(limit).offset(offset))
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        return items, total
