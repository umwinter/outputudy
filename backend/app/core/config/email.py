from pydantic import Field

from .base import BaseConfig


class EmailSettings(BaseConfig):
    # Email
    SMTP_HOST: str = Field("mailpit", description="SMTP Host")
    SMTP_PORT: int = Field(1025, description="SMTP Port")
    SMTP_USER: str = Field("", description="SMTP User")
    SMTP_PASSWORD: str = Field("", description="SMTP Password")
    SMTP_FROM_EMAIL: str = Field("noreply@outputudy.com", description="SMTP From Email")
    SMTP_TLS: bool = Field(False, description="SMTP TLS")
