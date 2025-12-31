from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL Connection String")

    # Security
    SECRET_KEY: str = Field(..., description="JWT Secret Key")
    ALGORITHM: str = Field("HS256", description="JWT Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24, description="Access token expiration in minutes"
    )

    # Google Cloud
    GCP_PROJECT_ID: str = Field("local-project", description="GCP Project ID")
    REGION: str = Field("asia-northeast1", description="GCP Region")

    # App
    APP_NAME: str = "outputudy-backend"
    ENV: str = Field("development", description="Environment (development, production)")


settings = Settings()
