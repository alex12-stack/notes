from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UserOrm
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
