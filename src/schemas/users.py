from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class User_With_Hashed_Password(User):
    hashed_password: str

class PatchMe(BaseModel):
    username: str | None = None
    email: EmailStr | None = None