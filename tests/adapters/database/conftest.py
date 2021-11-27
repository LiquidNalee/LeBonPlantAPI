from typing import AsyncGenerator

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from lebonplantapi.adapters.database.models.base import Base
from lebonplantapi.adapters.database.settings import SessionFactory, engine


@pytest.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS lebonplantapi"))
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def db_session(db: None) -> AsyncSession:
    # We want only one session shared for all the tests.
    return SessionFactory()


@pytest.fixture(scope="function", autouse=True)
async def db_autoclean(db: None) -> AsyncGenerator[None, None]:
    yield
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        await conn.commit()


@pytest.fixture(scope="function")
async def session_autoclose(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    try:
        yield db_session
    finally:
        await db_session.close()
