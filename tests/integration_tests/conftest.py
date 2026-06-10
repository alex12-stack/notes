import pytest

from src.db import Base, engine_null_pool


@pytest.fixture(scope="function", autouse=True)
async def clean_db(test_check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)