from pydantic import Field

from .base import BaseConfig


class DatabaseSettings(BaseConfig):
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL Connection String")
