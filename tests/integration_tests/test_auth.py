import pytest

from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)

    assert payload
    assert payload["user_id"] == data["user_id"]





@pytest.mark.parametrize("username, password, email, status_code",[
    ("1231234","a,sdsd2","test_email",422),
    ("1231234","a,sdsd2","test_email.ru",422),
    ("1231234","a,sdsd2","test_email@.ru",422),
    ("1231234","a,sdsd2","@mail.ru",422),
    ("1231234","a,sdsd2","asld,@mail.ru",422),
    ("1231234","a,sdsd2","asld@mail.ru",200),
    ("5420","a,sdsd2","asld@mail.ru",200),
    ("","a,sdsd2","asld@mail.ru",422),
    ("","","asld@mail.ru",422),
    ("1"*31,"12345","asld@mail.ru",422),
    ("12345","1"*100,"asld@mail.ru",200),
    ("1","1","asld@mail.ru",422),
    ("1"*31,"1"*101,"asld@mail.ru",422),

])
async def test_register_success(ac,db,username,password,email,status_code):
    response = await ac.post(
        "/auth/register",
        json = {
            "username": username,
            "password": password,
            "email": email,
        }
    )

    assert response.status_code == status_code

    if status_code != 422:
        user = await db.users.get_one_or_none(email=email)

        assert user is not None
        assert user.username == username
        assert user.email == email



