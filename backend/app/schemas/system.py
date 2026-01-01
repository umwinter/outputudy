from pydantic import BaseModel, ConfigDict, Field


class RootResponse(BaseModel):
    app: str = Field(
        ...,
        title="App Name",
        description="**アプリケーションの名前**です。プロジェクトの設定から自動的に取得されます。",
    )
    env: str = Field(
        ...,
        title="Environment",
        description="現在の**実行環境**（例: `development`, `production`）を示します。",
    )
    status: str = Field(
        ...,
        title="App Status",
        description="アプリケーションの**稼働状態**を表します。",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "app": "outputudy-backend",
                "env": "development",
                "status": "running",
            },
            "examples": [
                {
                    "app": "outputudy-backend",
                    "env": "development",
                    "status": "running",
                }
            ],
        }
    )


class HealthCheckResponse(BaseModel):
    status: str = Field(
        ...,
        title="Health Status",
        description="システムが健全であれば `ok` が返されます。",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"status": "ok"},
            "examples": [{"status": "ok"}],
        }
    )
