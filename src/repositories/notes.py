from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.notes import NotesOrm

class NotesRepository(BaseRepository):
    model = NotesOrm

    async def get_all(
            self,
            owner_id,
            title=None,
            content=None,
            folder_id=None,
            is_public=None,
            created_at=None,
            limit=5,
            offset=0,
    ):
        query = select(self.model).filter_by(owner_id=owner_id)

        if title:
            query = query.where(
                    self.model.title.ilike(f"%{title.strip()}%")
            )

        if content:
            query =query.where(
                    self.model.content.ilike(f"%{content.strip()}%")
            )


        if folder_id is not None:
            query=query.filter_by(folder_id=folder_id)

        if is_public is not None:
            query = query.filter_by(is_public=is_public)

        if created_at is not None:
            query=query.filter_by(created_at=created_at)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()

