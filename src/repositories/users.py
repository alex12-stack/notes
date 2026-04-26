from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UserOrm
from src.schemas.users import User_With_Hashed_Password


class UserRepository(BaseRepository):
    model = UserOrm

    async def get_user_with_hashed_password(self,email:EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return User_With_Hashed_Password.model_validate(model)



