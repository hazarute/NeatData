"""
NeatData REST API
=================
Veri temizleme işlemlerini Web API üzerinden sunan FastAPI uygulaması.

Bu API, masaüstü GUI'si ile aynı Core (PipelineManager) kullanarak,
dış sistemlerin NeatData temizleme fonksiyonlarına JSON aracılığıyla
erişmesini sağlar.

Başlatma:
    uvicorn api:app --reload

Swagger UI:
    http://127.0.0.1:8000/docs

OpenAPI Schema:
    http://127.0.0.1:8000/openapi.json
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api_modules.utils import get_iso_timestamp
from api_modules.logging_service import StructuredLogger
from api_modules.routes.v1.health import router as health_router
# from api_modules.routes.v1.clean import router as clean_router
from api_modules.routes.v1.pipeline import router as pipeline_router
from api_modules.routes.v1.info import router as info_router
from api_modules.routes.v1.upload import router as upload_router
from api_modules.routes.v1.database import router as database_router
from api_modules.routes.v1.queue import router as queue_router
from api_modules.routes.v1.websocket import router as websocket_router
import time
import sys

sys.path.append("E:\\NewWork\\NeatData - CSV Veri Temizleme")


try:
    from api_modules.routes.v1.health import router as health_router
    print("Import başarılı.")
except ModuleNotFoundError as e:
    print("Import hatası:", e)


def create_app() -> FastAPI:
    """
    FastAPI uygulaması oluştur ve router'ları kaydet.
    
    Returns:
        FastAPI: Konfigüre edilmiş FastAPI uygulaması
    """
    app = FastAPI(
        title="NeatData API",
        description="CSV/Excel veri temizleme REST API servisi",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        redoc_url=None  # ReDoc kullanmıyoruz, Swagger yeterli
    )
    
    # Router'ları kaydet
    app.include_router(info_router)
    app.include_router(health_router)
    # app.include_router(clean_router)
    app.include_router(pipeline_router)
    app.include_router(upload_router)
    app.include_router(database_router)
    app.include_router(queue_router)
    app.include_router(websocket_router)
    app.include_router(queue_router)
    
    # Logging middleware
    logger = StructuredLogger()
    
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        """Log requests ve responses."""
        start_time = time.time()
        
        # Mask API key
        api_key = request.headers.get("X-API-Key")
        api_key_masked = f"{api_key[:8]}...{api_key[-4:]}" if api_key else None
        
        # Log request
        logger.log_request(
            method=request.method,
            path=request.url.path,
            query_params=dict(request.query_params) if request.query_params else None,
            api_key_masked=api_key_masked
        )
        
        # Call endpoint
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            logger.error(
                "Request processing failed",
                context={
                    "method": request.method,
                    "path": request.url.path
                },
                error=e
            )
            raise
        
        # Log response
        process_time = (time.time() - start_time) * 1000  # milliseconds
        logger.log_response(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            response_time_ms=process_time
        )
        
        return response
    
    # Error Handler
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Genel exception handler."""
        logger.error(
            "Unhandled exception",
            context={
                "method": request.method,
                "path": request.url.path
            },
            error=exc
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": "İntemal sunucu hatası",
                "details": str(exc),
                "timestamp": get_iso_timestamp()
            }
        )
    
    return app


# App örneğini oluştur
app = create_app()

# Python path'ini yazdır (debug amaçlı)
import sys
print('PYTHONPATH:', sys.path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
