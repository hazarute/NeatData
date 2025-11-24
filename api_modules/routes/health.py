"""
Health Check Routes
===================
Sistem durumu kontrolü için endpoint.
"""

from fastapi import APIRouter
from api_modules.models import HealthCheckResponse
from api_modules.utils import get_iso_timestamp

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Sistem Durumu Kontrolü"
)
async def health_check() -> HealthCheckResponse:
    """
    NeatData API'nin çalışıp çalışmadığını kontrol et.
    
    Bu endpoint, API'nin sağlıklı olup olmadığını döndürür.
    Harici monitoring ve health check araçları tarafından kullanılır.
    
    Returns:
        HealthCheckResponse: Sistem durumu (status='ok')
    """
    return HealthCheckResponse(
        status="ok",
        message="NeatData API çalışıyor ve istekleri kabul etmeye hazır",
        timestamp=get_iso_timestamp(),
        version="1.0.0"
    )
