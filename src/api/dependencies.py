from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.db import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class Pagination(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    per_page: Annotated[int | None, Query(ge=1, le=100)] = None


PaginationDep = Annotated[Pagination, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_curr_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_curr_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
