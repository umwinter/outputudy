from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Database connection URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create Async Engine
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=(settings.ENV == "development")
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
