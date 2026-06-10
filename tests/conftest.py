import pytest
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.db import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


async def db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db



@pytest.fixture(scope="function")
async def db():
    async for db in db_null_pool():
        yield db


app.dependency_overrides[get_db] = db_null_pool


@pytest.fixture(scope="session",autouse=True)
def test_check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session",autouse=True)
async def setup_db(test_check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url="http://test") as ac:
        yield ac




