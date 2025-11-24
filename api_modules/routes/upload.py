"""
File Upload Routes
==================
CSV dosyası yüklemesi ve ayrıştırması endpoint'leri.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from api_modules.models import FileUploadResponse
from api_modules.utils import get_iso_timestamp
from db import Database, UploadRecord
import pandas as pd
import io
from typing import Optional
import json

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post(
    "/csv",
    response_model=FileUploadResponse,
    summary="CSV Dosyası Yükle",
    responses={
        200: {"description": "Dosya başarıyla yüklendi"},
        400: {"description": "Hatalı dosya formatı"},
        413: {"description": "Dosya çok büyük (max 50MB)"},
        500: {"description": "Sunucu hatası"}
    }
)
async def upload_csv(file: UploadFile = File(...)) -> FileUploadResponse:
    """
    CSV dosyasını sunucuya yükle ve ayrıştır.
    
    Bu endpoint:
    - Multipart/form-data formatında CSV dosyası kabul eder
    - Dosya boyutunu kontrol eder (max 50MB)
    - Dosya türünü doğrular (application/octet-stream veya text/csv)
    - Pandas ile DataFrame'e dönüştürür
    - Satır ve sütun sayısını döner
    
    Args:
        file: Yüklenecek CSV dosyası (UploadFile)
    
    Returns:
        FileUploadResponse: Upload sonuç bilgisi
    
    Raises:
        HTTPException: Dosya formatı veya boyut hatası
    """
    try:
        # Dosya adı validasyonu
        if not file.filename:
            raise ValueError("Dosya adı boş olamaz")
        
        # Dosya uzantısı kontrolü
        if not file.filename.lower().endswith(('.csv', '.txt')):
            raise ValueError(f"Desteklenmeyen dosya türü: {file.filename}. Sadece .csv ve .txt dosyaları kabul edilir.")
        
        # Dosya boyutu kontrolü (50MB max)
        max_size = 50 * 1024 * 1024  # 50 MB
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > max_size:
            raise ValueError(f"Dosya çok büyük: {file_size / (1024*1024):.2f}MB. Maximum 50MB.")
        
        if file_size == 0:
            raise ValueError("Dosya boş olamaz")
        
        # CSV dosyasını DataFrame'e dönüştür
        try:
            # UTF-8 ile başla, başarısız olursa ISO-8859-1 kullan
            try:
                df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(contents), encoding='iso-8859-1')
        except Exception as e:
            raise ValueError(f"CSV dosyası ayrıştırılamadı: {str(e)}")
        
        # DataFrame bilgilerini al
        rows, cols = df.shape
        
        # Veritabanına kaydet
        upload_id = None
        try:
            db = Database()
            upload_record = UploadRecord(
                filename=file.filename,
                file_size=file_size,
                rows=rows,
                columns=cols,
                original_shape=json.dumps([rows, cols]),
                user_agent=None
            )
            upload_id = upload_record.save()
        except Exception as db_error:
            # Veritabanı hatası, response'a upload_id olmadan gönder
            print(f"Database save error: {db_error}")
        
        return FileUploadResponse(
            status="success",
            filename=file.filename,
            file_size=file_size,
            rows=rows,
            columns=cols,
            upload_id=upload_id,
            message=f"Dosya başarıyla yüklendi: {rows} satır, {cols} sütun",
            timestamp=get_iso_timestamp()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dosya yükleme hatası: {str(e)}"
        )
