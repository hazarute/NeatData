"""Route handlers for v1 API endpoints."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .health import router as health_router
# from .clean import router as clean_router
from .pipeline import router as pipeline_router
from .info import router as info_router
from .upload import router as upload_router
from .database import router as database_router
from .queue import router as queue_router
from .websocket import router as websocket_router

class DeprecationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/v1/"):
            response.headers["X-API-Deprecation"] = "true"
            response.headers["X-API-Deprecation-Date"] = "2026-01-01"
        return response

__all__ = [
    "health_router",
    # "clean_router",
    "pipeline_router",
    "info_router",
    "upload_router",
    "database_router",
    "queue_router",
    "websocket_router"
]