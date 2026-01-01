from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exception_handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import RequestIDMiddleware
from app.router import api_router
from app.schemas.system import HealthCheckResponse, RootResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    yield


description = "Outputudy のバックエンド API です。"

tags_metadata = [
    {
        "name": "auth",
        "description": "認証およびアカウント管理",
    },
    {
        "name": "users",
        "description": "ユーザー情報の取得・管理",
    },
    {
        "name": "system",
        "description": "システムの稼働確認",
    },
]

app = FastAPI(
    title="Outputudy API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None,
)

# CORS configuration
origins = settings.BACKEND_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)

app.include_router(api_router, prefix="/api")

add_exception_handlers(app)


@app.get(
    "/",
    tags=["system"],
    response_model=RootResponse,
    summary="ルートエンドポイント",
    description="アプリケーションの基本情報を取得します。",
)
async def read_root() -> RootResponse:
    return RootResponse(
        app=settings.APP_NAME,
        env=settings.ENV,
        status="running",
    )


@app.get(
    "/health",
    tags=["system"],
    response_model=HealthCheckResponse,
    summary="ヘルスチェック",
    description="システムの稼働状況を確認するためのエンドポイントです。",
)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
