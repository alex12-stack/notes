from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.folders import FoldersOrm


class FoldersRepository(BaseRepository):
    model = FoldersOrm

    async def get_all(
            self,
            owner_id,
            name=None,
            limit=5,
            offset=0,
    ):
        query = select(self.model).where(self.model.owner_id == owner_id)

        if name:
            query = query.where(
                self.model.name.ilike(f"%{name.strip()}%")
            )


        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()




















