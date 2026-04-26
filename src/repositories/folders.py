from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.folders import FoldersOrm


class FoldersRepository(BaseRepository):
    model = FoldersOrm

    async def get_all(
            self,
            name,
            owner_id,
            limit,
            offset,
    ):
        query = select(self.model).filter_by(owner_id=owner_id)

        if name:
            query = query.where(
                FoldersOrm.name.ilike(f"%{name.strip()}%")
            )


        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()




















