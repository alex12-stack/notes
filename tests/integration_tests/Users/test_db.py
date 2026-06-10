from src.db import async_session_maker
from src.schemas.users import UserAdd
from src.utils.db_manager import DBManager


async def test_create_user(db):
    user_data = UserAdd(username="alex",email="sumarokov.lsha@bk.ru",hashed_password="lalala")
    new_user_data = await db.users.add(user_data)
    await db.commit()

    assert new_user_data