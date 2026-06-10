from src.services.auth import AuthService


def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token,str)


def test_hash_password_not_equal_raw_password():
    data = {"password": "lalala"}

    assert AuthService().hash_password(data["password"]) != data["password"]



def test_verify_password_success():
    data = {"password": "lalala"}

    hashed_password = AuthService().hash_password(data["password"])

    assert AuthService().verify_password(data["password"],hashed_password)