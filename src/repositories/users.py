from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UserOrm
from src.schemas.users import User_With_Hashed_Password


class UsersRepository(BaseRepository):
    model = UserOrm

    async def get_user_with_hashed_password(self,username:str, email:EmailStr):
        query = select(self.model).filter_by(username=username,email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return model


