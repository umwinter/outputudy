import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Bind request_id to structlog context
        bind_contextvars(request_id=request_id)

        response = await call_next(request)

        # Add request_id to response headers
        response.headers["X-Request-ID"] = request_id
        return response
