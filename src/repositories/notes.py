from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.notes import NotesOrm

class NotesRepository(BaseRepository):
    model = NotesOrm

    async def get_all(
            self,
            title,
            content,
            owner_id,
            folder_id,
            is_public,
            created_at,
            limit,
            offset,
    ):
        query = select(NotesOrm).filter_by(is_public=True)

        if title:
            query = (
                query
                .filter(func.lower(NotesOrm.title)
                .contains(title.strip().lower()))
            )

        if content:
            query = (
                query
                .filter(func.lower(NotesOrm.content)
                .contains(content.strip().lower()))
            )

        if owner_id:
            query.filter_by(owner_id=owner_id)

        if folder_id:
            query.filter_by(folder_id=folder_id)

        if created_at:
            query.filter_by(created_at=created_at)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        res = await self.session.execute(query)

        return res.scalars().all()

