"""Route handlers - API endpoint modules."""

from .health import router as health_router
from .clean import router as clean_router
from .pipeline import router as pipeline_router
from .info import router as info_router
from .upload import router as upload_router
from .database import router as database_router
from .queue import router as queue_router
from .websocket import router as websocket_router

__all__ = [
    "health_router",
    "clean_router",
    "pipeline_router",
    "info_router",
    "upload_router",
    "database_router",
    "queue_router",
    "websocket_router"
]
