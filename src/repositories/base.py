from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self,*args,**kwargs):
        query = select(self.model)
        res = await self.session.scalars(query)
        # result = await self.session.execute(query)
        # return result.scalars().all()
        return res.all()

    async def get_one_or_none(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.scalars(query)
        return res.one_or_none()

    async def delete(self,**filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def add(self, data:BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(add_stmt)
        return res.scalars().one()

    async def edit(self, data:BaseModel, exclude_unset: bool = False, **filter_by):
        # exclude_unset позволяет сделать так, чтобы, если пользователь что-то не передал, то поставилось значение по умолчанию
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_stmt)






























