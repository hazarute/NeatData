"""
Info Routes
===========
API bilgilendirme endpoint'leri.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Info"])


@router.get(
    "/",
    summary="Ana Sayfa"
)
async def root():
    """
    API'nin ana sayfası. Kullanılabilir endpoint'ler hakkında bilgi.
    """
    return {
        "name": "NeatData API",
        "version": "1.0.0",
        "description": "CSV/Excel veri temizleme REST API servisi",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "health": "GET /health - Sistem durumu kontrolü",
            "clean": "POST /clean - Metin temizleme (POC)",
            "available_modules": "GET /pipeline/available - Mevcut modülleri listele",
            "pipeline_run": "POST /pipeline/run - DataFrame üzerinde pipeline çalıştır"
        }
    }
