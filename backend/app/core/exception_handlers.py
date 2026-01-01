from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from structlog import get_logger

from app.core.config import settings

logger = get_logger()


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("global_exception_handler", error=str(exc))
    if settings.ENV == "production":
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)  # type: ignore
