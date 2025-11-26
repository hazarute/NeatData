"""
File Upload Routes
==================
CSV dosyası yüklemesi ve ayrıştırması endpoint'leri.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from api_modules.models import FileUploadResponse
from api_modules.utils import get_iso_timestamp
from api_modules.security import verify_api_key
from db import Database, UploadRecord
import pandas as pd
from typing import Optional
import json
from pathlib import Path
from api_modules.utils.storage import save_upload_file
import os

router = APIRouter(prefix="/v1/upload", tags=["Upload"])


@router.post(
    "/csv",
    response_model=FileUploadResponse,
    summary="CSV Dosyası Yükle",
    responses={
        200: {"description": "Dosya başarıyla yüklendi"},
        400: {"description": "Hatalı dosya formatı"},
        401: {"description": "Unauthorized - geçersiz API key"},
        413: {"description": "Dosya çok büyük (max 50MB)"},
        500: {"description": "Sunucu hatası"}
    }
)
async def upload_csv(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)) -> FileUploadResponse:
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

        # Disk'e kaydet (stream olarak) ve path döndür
        saved_path = await save_upload_file(file)
        saved_path_obj = Path(saved_path)

        # Dosya boyutu kontrolü (50MB max)
        max_size = 50 * 1024 * 1024  # 50 MB
        try:
            file_size = saved_path_obj.stat().st_size
        except Exception:
            raise ValueError("Kaydedilen dosyanın boyutu alınamadı")

        if file_size > max_size:
            # büyük dosyayı temizle
            try:
                os.remove(saved_path)
            except Exception:
                pass
            raise ValueError(f"Dosya çok büyük: {file_size / (1024*1024):.2f}MB. Maximum 50MB.")

        if file_size == 0:
            raise ValueError("Dosya boş olamaz")

        # CSV dosyasını DataFrame'e dönüştür (dosya yolundan)
        try:
            try:
                df = pd.read_csv(str(saved_path_obj), encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(str(saved_path_obj), encoding='iso-8859-1')
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
                user_agent=None,
                file_path=str(saved_path)
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
