from .app import AppSettings
from .auth import AuthSettings
from .cors import CorsSettings
from .database import DatabaseSettings
from .email import EmailSettings


class Settings(
    AppSettings, AuthSettings, CorsSettings, DatabaseSettings, EmailSettings
):
    pass


settings = Settings()  # type: ignore
