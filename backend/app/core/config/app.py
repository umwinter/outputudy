from pydantic import Field

from .base import BaseConfig


class AppSettings(BaseConfig):
    # App
    APP_NAME: str = "outputudy-backend"
    ENV: str = Field("development", description="Environment (development, production)")
    FRONTEND_URL: str = Field("http://localhost:3000", description="Frontend URL")

    # Google Cloud
    GCP_PROJECT_ID: str = Field("local-project", description="GCP Project ID")
    REGION: str = Field("asia-northeast1", description="GCP Region")
