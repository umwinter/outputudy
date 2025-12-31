from pydantic import Field

from .base import BaseConfig


class AuthSettings(BaseConfig):
    # Security
    SECRET_KEY: str = Field(..., description="JWT Secret Key")
    ALGORITHM: str = Field("HS256", description="JWT Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24, description="Access token expiration in minutes"
    )
    # Used for NextAuth secret if needed, but primarily SECRET_KEY is used for JWT
    AUTH_SECRET: str | None = Field(None, description="NextAuth Secret")
