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
        query = select(self.model)

        if name:
            query = (
                query
                .filter(func.lower(FoldersOrm.name)
                .contains(name.strip().lower()))
            )

        if owner_id:
            query = query.filter(FoldersOrm.owner_id==owner_id)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()




















