"""
Text Cleaning Routes
====================
Metin temizleme endpoint'leri.
"""

from fastapi import APIRouter, HTTPException, Depends
from api_modules.models import CleanRequest, CleanResponse
from api_modules.utils import get_iso_timestamp
from api_modules.security import verify_api_key
from typing import List

router = APIRouter(prefix="/clean", tags=["Cleaning"])


def clean_text_simple(text: str, operations: List[str]) -> str:
    """
    Basit metin temizleme fonksiyonu.
    
    Args:
        text: Temizlenecek metin
        operations: Uygulanacak işlemler listesi
    
    Returns:
        Temizlenmiş metin
    """
    result = text
    for op in operations:
        if op == "trim":
            result = result.strip()
        elif op == "lowercase":
            result = result.lower()
        elif op == "uppercase":
            result = result.upper()
    return result


@router.post(
    "",
    response_model=CleanResponse,
    summary="Metni Temizle",
    responses={
        200: {"description": "Başarılı temizleme"},
        400: {"description": "Hatalı istek"},
        401: {"description": "Unauthorized - geçersiz API key"},
        500: {"description": "İntemal sunucu hatası"}
    }
)
async def clean_data(request: CleanRequest, api_key: str = Depends(verify_api_key)) -> CleanResponse:
    """
    Verilen metni belirtilen işlemler ile temizle.
    
    Bu endpoint, basit metin temizleme işlemleri (trim, lowercase vb.)
    gerçekleştirir. İleriki versiyonlarda PipelineManager ile entegre
    edilerek dinamik plugin'leri çalıştıracaktır.
    
    Args:
        request: CleanRequest (data + operations)
    
    Returns:
        CleanResponse: Temizleme sonucu
    
    Raises:
        HTTPException: Hata durumunda
    """
    try:
        # Veri validasyonu
        if not request.data:
            raise ValueError("Temizlenecek veri boş olamaz")
        
        # Default operations'u ayarla
        operations = request.operations if request.operations else ["trim"]
        
        # İşlem kontrolü
        valid_operations = {"trim", "lowercase", "uppercase"}
        for op in operations:
            if op not in valid_operations:
                raise ValueError(f"Geçersiz işlem: {op}")
        
        # Temizleme işlemi
        cleaned = clean_text_simple(request.data, operations)
        
        return CleanResponse(
            status="success",
            original_data=request.data,
            cleaned_data=cleaned,
            operations_applied=operations,
            message="Veri başarıyla temizlendi",
            timestamp=get_iso_timestamp()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İçsel hata: {str(e)}")
