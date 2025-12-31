from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

if TYPE_CHECKING:
    pass

# Database connection URL
# Use settings.DATABASE_URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create Async Engine
# Echo logs in development
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=(settings.ENV == "development")
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
