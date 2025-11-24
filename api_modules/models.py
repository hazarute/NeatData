"""
API Pydantic Models
===================
Tüm request ve response şemaları bu dosyada tanımlanır.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class HealthCheckResponse(BaseModel):
    """Health check endpoint'inin dönüş modeli."""
    status: str = Field(..., description="Sistem durumu (ok/error)")
    message: str = Field(..., description="Durum mesajı")
    timestamp: str = Field(..., description="İstek zamanı (ISO 8601)")
    version: str = Field(default="1.0.0", description="API versiyonu")

    class Config:
        example = {
            "status": "ok",
            "message": "NeatData API çalışıyor",
            "timestamp": "2025-11-24T15:30:00",
            "version": "1.0.0"
        }


class CleanRequest(BaseModel):
    """Veri temizleme isteği."""
    data: str = Field(..., description="Temizlenecek metin")
    operations: Optional[List[str]] = Field(
        default=["trim"],
        description="Uygulanacak işlemler (trim, lowercase, vb.)"
    )
    
    class Config:
        example = {
            "data": "  kirli veri  ",
            "operations": ["trim"]
        }


class CleanResponse(BaseModel):
    """Veri temizleme sonuç modeli."""
    status: str = Field(..., description="İşlem durumu (success/error)")
    original_data: str = Field(..., description="Orijinal veri")
    cleaned_data: str = Field(..., description="Temizlenmiş veri")
    operations_applied: List[str] = Field(..., description="Uygulanan işlemler")
    message: Optional[str] = Field(None, description="İşlem mesajı")
    timestamp: str = Field(..., description="İşlem zamanı")
    
    class Config:
        example = {
            "status": "success",
            "original_data": "  kirli veri  ",
            "cleaned_data": "kirli veri",
            "operations_applied": ["trim"],
            "message": "Veri başarıyla temizlendi",
            "timestamp": "2025-11-24T15:30:10"
        }


class ErrorResponse(BaseModel):
    """Hata yanıt modeli."""
    status: str = Field(default="error", description="Hata durumu")
    error: str = Field(..., description="Hata mesajı")
    details: Optional[str] = Field(None, description="Hata detayları")
    timestamp: str = Field(..., description="Hata zamanı")
    
    class Config:
        example = {
            "status": "error",
            "error": "İntemal sunucu hatası",
            "details": "Traceback...",
            "timestamp": "2025-11-24T15:30:15"
        }


class ModuleInfo(BaseModel):
    """Modül bilgisi (Core veya Custom)."""
    key: str = Field(..., description="Modül anahtarı (unique ID)")
    name: str = Field(..., description="Modül adı (user-friendly)")
    description: str = Field(..., description="Modül açıklaması")
    origin: str = Field(..., description="Modül kaynağı (core/custom)")
    
    class Config:
        example = {
            "key": "trim_spaces",
            "name": "Trim Spaces",
            "description": "Başında ve sonundaki boşlukları temizle",
            "origin": "core"
        }


class AvailableModulesResponse(BaseModel):
    """Mevcut modüller listesi."""
    status: str = Field(default="success", description="İşlem durumu")
    core_modules: List[ModuleInfo] = Field(..., description="Core modülü listesi")
    custom_modules: List[ModuleInfo] = Field(..., description="Custom plugin listesi")
    timestamp: str = Field(..., description="İstek zamanı")
    
    class Config:
        example = {
            "status": "success",
            "core_modules": [
                {
                    "key": "trim_spaces",
                    "name": "Trim Spaces",
                    "description": "Başında ve sonundaki boşlukları temizle",
                    "origin": "core"
                }
            ],
            "custom_modules": [],
            "timestamp": "2025-11-24T17:55:00"
        }


class PipelineRunRequest(BaseModel):
    """Pipeline çalıştırma isteği."""
    data: Dict[str, Any] = Field(..., description="DataFrame'e çevrilecek veri (dict of lists)")
    modules: List[str] = Field(..., description="Çalıştırılacak modül keys veya names")
    
    class Config:
        example = {
            "data": {
                "name": ["  John  ", "  Jane  "],
                "age": [25, 30]
            },
            "modules": ["trim_spaces"]
        }


class PipelineRunResponse(BaseModel):
    """Pipeline çalıştırma sonuç modeli."""
    status: str = Field(..., description="İşlem durumu (success/error)")
    original_shape: tuple = Field(..., description="Orijinal DataFrame şekli (rows, cols)")
    cleaned_shape: tuple = Field(..., description="Temizlenmiş DataFrame şekli")
    result_data: Dict[str, List[Any]] = Field(..., description="Temizlenmiş veri (dict of lists)")
    modules_executed: List[str] = Field(..., description="Çalıştırılan modüller")
    message: Optional[str] = Field(None, description="İşlem mesajı")
    timestamp: str = Field(..., description="İşlem zamanı")
    
    class Config:
        example = {
            "status": "success",
            "original_shape": (2, 2),
            "cleaned_shape": (2, 2),
            "result_data": {
                "name": ["John", "Jane"],
                "age": [25, 30]
            },
            "modules_executed": ["trim_spaces"],
            "message": "Pipeline başarıyla çalıştırıldı",
            "timestamp": "2025-11-24T17:55:10"
        }


class FileUploadResponse(BaseModel):
    """CSV dosyası upload yanıt modeli."""
    status: str = Field(..., description="Upload durumu (success/error)")
    filename: str = Field(..., description="Yüklenen dosya adı")
    file_size: int = Field(..., description="Dosya boyutu (byte)")
    rows: int = Field(..., description="CSV satır sayısı")
    columns: int = Field(..., description="CSV sütun sayısı")
    message: Optional[str] = Field(None, description="İşlem mesajı")
    timestamp: str = Field(..., description="Upload zamanı")
    
    class Config:
        example = {
            "status": "success",
            "filename": "messy_data.csv",
            "file_size": 5240,
            "rows": 100,
            "columns": 5,
            "message": "Dosya başarıyla yüklendi ve ayrıştırıldı",
            "timestamp": "2025-11-25T10:30:00"
        }


class UploadHistoryItem(BaseModel):
    """Yükleme geçmişi öğesi."""
    id: int = Field(..., description="Upload ID")
    filename: str = Field(..., description="Dosya adı")
    file_size: int = Field(..., description="Dosya boyutu (byte)")
    rows: int = Field(..., description="Satır sayısı")
    columns: int = Field(..., description="Sütun sayısı")
    status: str = Field(..., description="İşlem durumu")
    uploaded_at: str = Field(..., description="Yükleme zamanı")
    
    class Config:
        example = {
            "id": 1,
            "filename": "data.csv",
            "file_size": 1024,
            "rows": 10,
            "columns": 3,
            "status": "success",
            "uploaded_at": "2025-11-25T10:30:00"
        }


class UploadHistoryResponse(BaseModel):
    """Yükleme geçmişi yanıtı."""
    status: str = Field(default="success", description="İşlem durumu")
    total_uploads: int = Field(..., description="Toplam yükleme sayısı")
    uploads: List[UploadHistoryItem] = Field(..., description="Yükleme listesi")
    timestamp: str = Field(..., description="İşlem zamanı")
    
    class Config:
        example = {
            "status": "success",
            "total_uploads": 5,
            "uploads": [
                {
                    "id": 1,
                    "filename": "data.csv",
                    "file_size": 1024,
                    "rows": 10,
                    "columns": 3,
                    "status": "success",
                    "uploaded_at": "2025-11-25T10:30:00"
                }
            ],
            "timestamp": "2025-11-25T10:35:00"
        }


class ProcessingLogItem(BaseModel):
    """İşleme günlüğü öğesi."""
    id: int = Field(..., description="Log ID")
    upload_id: int = Field(..., description="Upload ID")
    module_name: str = Field(..., description="Modül adı")
    module_origin: str = Field(..., description="Modül kaynağı (core/custom)")
    status: str = Field(..., description="Durum (success/error)")
    execution_time_ms: Optional[float] = Field(None, description="Çalışma süresi (ms)")
    error_message: Optional[str] = Field(None, description="Hata mesajı")
    processed_at: str = Field(..., description="İşleme zamanı")
    
    class Config:
        example = {
            "id": 1,
            "upload_id": 1,
            "module_name": "trim_spaces",
            "module_origin": "core",
            "status": "success",
            "execution_time_ms": 125.5,
            "error_message": None,
            "processed_at": "2025-11-25T10:30:05"
        }


class ProcessingLogsResponse(BaseModel):
    """İşleme günlüğü yanıtı."""
    status: str = Field(default="success", description="İşlem durumu")
    upload_id: int = Field(..., description="Upload ID")
    total_logs: int = Field(..., description="Toplam günlük sayısı")
    logs: List[ProcessingLogItem] = Field(..., description="Günlük listesi")
    timestamp: str = Field(..., description="İşlem zamanı")
    
    class Config:
        example = {
            "status": "success",
            "upload_id": 1,
            "total_logs": 2,
            "logs": [
                {
                    "id": 1,
                    "upload_id": 1,
                    "module_name": "trim_spaces",
                    "module_origin": "core",
                    "status": "success",
                    "execution_time_ms": 125.5,
                    "error_message": None,
                    "processed_at": "2025-11-25T10:30:05"
                }
            ],
            "timestamp": "2025-11-25T10:35:00"
        }
