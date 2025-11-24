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

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api_modules.utils import get_iso_timestamp
from api_modules.routes import health_router, clean_router, pipeline_router, info_router


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
    app.include_router(clean_router)
    app.include_router(pipeline_router)
    
    # Error Handler
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Genel exception handler."""
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
