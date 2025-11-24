"""
Response Formatters
===================
Yanıt oluşturma ve formatlama fonksiyonları.
"""

from typing import Dict, Any, Optional
from api_modules.utils.timestamp import get_iso_timestamp


def create_response(
    status: str,
    data: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Standart API yanıt oluştur.
    
    Args:
        status: Yanıt durumu (success/error)
        data: Yanıt verisi (opsiyonel)
        message: Durum mesajı (opsiyonel)
        timestamp: Zaman damgası (otomatik oluşturulur)
    
    Returns:
        Dict[str, Any]: Formatlanmış yanıt
    """
    response = {
        "status": status,
        "timestamp": timestamp or get_iso_timestamp()
    }
    
    if data is not None:
        response["data"] = data
    
    if message is not None:
        response["message"] = message
    
    return response


def create_error_response(
    error: str,
    details: Optional[str] = None,
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Standart hata yanıtı oluştur.
    
    Args:
        error: Hata mesajı
        details: Hata detayları (opsiyonel)
        timestamp: Zaman damgası (otomatik oluşturulur)
    
    Returns:
        Dict[str, Any]: Formatlanmış hata yanıtı
    """
    response = {
        "status": "error",
        "error": error,
        "timestamp": timestamp or get_iso_timestamp()
    }
    
    if details is not None:
        response["details"] = details
    
    return response
