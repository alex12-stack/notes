from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.notes import NotesOrm

class NotesRepository(BaseRepository):
    model = NotesOrm

    async def get_all(
            self,
            owner_id,
            title,
            content,
            folder_id,
            is_public,
            created_at,
            limit,
            offset,
    ):
        # query = select(NotesOrm).filter_by(is_public=True)
        query = select(NotesOrm).filter_by(owner_id=owner_id)

        if title:
            query = (
                query
                .where(
                    NotesOrm.title.ilike(f"%{title.strip()}%")
                )
            )

        if content:
            query = (
                query
                .where(
                    NotesOrm.content.ilike(f"%{content.strip()}%")
                )
            )


        if folder_id is not None:
            query=query.filter_by(folder_id=folder_id)

        if created_at is not None:
            query=query.filter_by(created_at=created_at)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()

