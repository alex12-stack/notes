from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=4, max_length=100)
    email: EmailStr = Field(max_length=50)


class UserAdd(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    email: EmailStr = Field(max_length=50)
    hashed_password: str = Field(max_length=500)


class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class User_With_Hashed_Password(User):
    hashed_password: str


class PatchMe(BaseModel):
    username: str | None = Field(default=None, min_length=4, max_length=30)
    email: EmailStr | None = Field(default=None, max_length=50)