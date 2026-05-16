from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.prior_art import PriorArt
from app.repositories.base_repo import BaseRepository


class PriorArtRepository(BaseRepository[PriorArt]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, PriorArt)

    async def list_by_patent(self, patent_id: UUID, limit: int = 50, offset: int = 0) -> tuple[list[PriorArt], int]:
        result = await self.db.execute(
            select(PriorArt).where(PriorArt.patent_id == patent_id).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(PriorArt).where(PriorArt.patent_id == patent_id)
        )
        total = count_result.scalar() or 0
        return items, total
