"""
Database Routes
===============
Veritabanı sorgulama ve raporlama endpoint'leri.
"""

from fastapi import APIRouter, HTTPException
from api_modules.models import UploadHistoryResponse, UploadHistoryItem, ProcessingLogsResponse, ProcessingLogItem
from api_modules.utils import get_iso_timestamp
from db import get_all_uploads, get_logs_by_upload_id, get_upload_by_id

router = APIRouter(prefix="/v1/db", tags=["Database"])


@router.get(
    "/uploads",
    response_model=UploadHistoryResponse,
    summary="Yükleme Geçmişini Getir",
    responses={
        200: {"description": "Yükleme geçmişi başarıyla alındı"},
        500: {"description": "Veritabanı hatası"}
    }
)
async def get_uploads_history() -> UploadHistoryResponse:
    """
    Tüm yüklenen dosyaların geçmişini getir.
    
    Bu endpoint:
    - Son 100 yüklemeyi veritabanından alır
    - Dosya bilgilerini (ad, boyut, satır/sütun sayısı) döner
    - Yükleme zamanını ve durumunu gösterir
    
    Returns:
        UploadHistoryResponse: Yükleme geçmişi
    
    Raises:
        HTTPException: Veritabanı hatası
    """
    try:
        uploads = get_all_uploads()
        
        items = [
            UploadHistoryItem(
                id=u["id"],
                filename=u["filename"],
                file_size=u["file_size"],
                rows=u["rows"],
                columns=u["columns"],
                status=u["status"],
                uploaded_at=u["uploaded_at"]
            )
            for u in uploads
        ]
        
        return UploadHistoryResponse(
            status="success",
            total_uploads=len(items),
            uploads=items,
            timestamp=get_iso_timestamp()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Veritabanı hatası: {str(e)}"
        )


@router.get(
    "/uploads/{upload_id}",
    summary="Yükleme Detaylarını Getir",
    responses={
        200: {"description": "Yükleme detayları başarıyla alındı"},
        404: {"description": "Yükleme bulunamadı"},
        500: {"description": "Veritabanı hatası"}
    }
)
async def get_upload_details(upload_id: int):
    """
    Belirli bir yüklemenin detaylarını getir.
    
    Args:
        upload_id: Yükleme ID'si
    
    Returns:
        Upload detayları
    
    Raises:
        HTTPException: Yükleme bulunamadı veya DB hatası
    """
    try:
        upload = get_upload_by_id(upload_id)
        
        if not upload:
            raise HTTPException(
                status_code=404,
                detail=f"Yükleme {upload_id} bulunamadı"
            )
        
        return {
            "status": "success",
            "data": upload,
            "timestamp": get_iso_timestamp()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Veritabanı hatası: {str(e)}"
        )


@router.get(
    "/logs/{upload_id}",
    response_model=ProcessingLogsResponse,
    summary="İşleme Günlüğünü Getir",
    responses={
        200: {"description": "Günlük başarıyla alındı"},
        500: {"description": "Veritabanı hatası"}
    }
)
async def get_processing_logs(upload_id: int) -> ProcessingLogsResponse:
    """
    Belirli bir yüklemenin işleme günlüğünü getir.
    
    Bu endpoint:
    - Yükleme ID'sine göre işleme günlüğünü sorgulamaktadır
    - Her modülün çalışma süresini ve durumunu gösterir
    - Hata mesajlarını (varsa) döner
    
    Args:
        upload_id: Yükleme ID'si
    
    Returns:
        ProcessingLogsResponse: İşleme günlüğü
    
    Raises:
        HTTPException: Veritabanı hatası
    """
    try:
        logs = get_logs_by_upload_id(upload_id)
        
        items = [
            ProcessingLogItem(
                id=log["id"],
                upload_id=log["upload_id"],
                module_name=log["module_name"],
                module_origin=log["module_origin"],
                status=log["status"],
                execution_time_ms=log["execution_time_ms"],
                error_message=log["error_message"],
                processed_at=log["processed_at"]
            )
            for log in logs
        ]
        
        return ProcessingLogsResponse(
            status="success",
            upload_id=upload_id,
            total_logs=len(items),
            logs=items,
            timestamp=get_iso_timestamp()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Veritabanı hatası: {str(e)}"
        )
