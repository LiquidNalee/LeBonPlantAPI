import asyncio
from asyncio import current_task

from sqlalchemy import text
from sqlalchemy.exc import DisconnectionError, OperationalError, TimeoutError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from instance import settings
from lebonplantapi.adapters.circuit_breakers import (
    circuit_breaker_registry,
    init_breaker,
)
from lebonplantapi.adapters.database.models.base import Base

engine = create_async_engine(
    settings.sqlalchemy_database_uri,
    pool_size=1,
    pool_pre_ping=True,
    connect_args={
        "timeout": settings.sqlalchemy_connect_timeout,
        "server_settings": {
            # "idle_in_transaction_session_timeout": "300000",
            "application_name": f"{settings.env_name}_{settings.application_name}",
        },
    },
    future=True,
)

SessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
)
session = async_scoped_session(SessionFactory, scopefunc=current_task)

db_breaker = init_breaker(
    registry=circuit_breaker_registry,
    breaker_id="db",
    exception_denylist=[DisconnectionError, TimeoutError, OperationalError],
)


def init_db() -> None:
    async def async_init_db() -> None:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS lebonplantapi"))
            await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(async_init_db())
