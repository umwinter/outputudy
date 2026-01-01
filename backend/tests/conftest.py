import asyncio
import os
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.infrastructure.database import Base, get_db

# Import models to ensure they are registered with Base.metadata
from app.infrastructure.orm_models import UserORM  # noqa: F401
from app.main import app


def get_worker_id() -> str:
    # gw0, gw1, etc. if running with xdist
    return os.environ.get("PYTEST_XDIST_WORKER", "master")


@pytest_asyncio.fixture(scope="session")  # type: ignore
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, Any]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def get_test_db_url(worker_id: str) -> str:
    # Construct distinct DB name
    base_url = make_url(settings.DATABASE_URL)
    test_db_name = f"test_db_{worker_id}"
    # Replace database name
    return base_url.set(database=test_db_name).render_as_string(hide_password=False)


def get_admin_db_url() -> str:
    # Connect to 'postgres' database to create/drop other databases
    base_url = make_url(settings.DATABASE_URL)
    return base_url.set(database="postgres").render_as_string(hide_password=False)


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    worker_id = get_worker_id()
    test_db_url = get_test_db_url(worker_id)
    admin_db_url = get_admin_db_url()

    # 1. Create Database
    # We need a separate engine to connect to 'postgres' DB and create the test DB.
    # AUTOCOMMIT is required for CREATE DATABASE
    admin_engine = create_async_engine(admin_db_url, isolation_level="AUTOCOMMIT")
    async with admin_engine.connect() as conn:
        db_name = f"test_db_{worker_id}"
        # Drop if exists (cleanup from previous interrupted runs)
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(text(f"CREATE DATABASE {db_name}"))
    await admin_engine.dispose()

    # 2. Connect to the Test Database
    from sqlalchemy.pool import NullPool

    engine = create_async_engine(test_db_url, echo=False, poolclass=NullPool)

    # 3. Create Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 4. Cleanup
    await engine.dispose()

    # Drop Database
    admin_engine = create_async_engine(admin_db_url, isolation_level="AUTOCOMMIT")
    async with admin_engine.connect() as conn:
        db_name = f"test_db_{worker_id}"
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
    await admin_engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session
        # Depending on test strategy, we might want to truncate tables here
        # For now, simplistic approach implies transactions rollbacks
        # or separate handling.
        # But 'engine' scope is session, so data persists across tests
        # unless cleaned.
        # Ideally, we wrap execution in a transaction and rollback,
        # but dependency override makes that tricky.
        # Common pattern: truncate all tables after each test.
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )
        await session.commit()


@pytest_asyncio.fixture
async def client(
    engine: AsyncEngine, db_session: AsyncSession
) -> AsyncGenerator[AsyncClient, None]:
    # Override get_db to create a NEW session from the test engine.
    # This prevents InterfaceError caused by sharing the same session object between test and app.
    # Data is visible because tests commit their changes.
    test_session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # Use ASGITransport to properly bind the app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    # Cleanup overrides after each test
    app.dependency_overrides.clear()
