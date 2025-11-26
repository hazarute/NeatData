"""
Pipeline Routes
===============
Pipeline çalıştırma endpoint'leri.
"""

from fastapi import APIRouter, HTTPException, Depends
from api_modules.models import (
    AvailableModulesResponse,
    ModuleInfo,
    PipelineRunByIdRequest,
    PipelineRunResponse
)
from api_modules.utils import get_iso_timestamp
from api_modules.dependencies import get_pipeline_manager
from api_modules.security import verify_api_key
from modules.pipeline_manager import PipelineManager
from typing import Dict, List, Any
from typing import cast
import pandas as pd

router = APIRouter(prefix="/v1/pipeline", tags=["Pipeline"])


@router.get(
    "/available",
    response_model=AvailableModulesResponse,
    summary="Mevcut Modülleri Listele"
)
async def get_available_modules(
    pm: PipelineManager = Depends(get_pipeline_manager)
) -> AvailableModulesResponse:
    """
    Tüm mevcut Core ve Custom modülleri listele.
    
    Returns:
        AvailableModulesResponse: Core ve Custom modüllerin listesi
    """
    try:
        # Core modülleri
        core_modules_info = [
            ModuleInfo(
                key=descriptor.key,
                name=descriptor.name,
                description=descriptor.description,
                origin="core"
            )
            for descriptor in pm.available_core_modules().values()
        ]
        
        # Custom modülleri
        custom_modules_info = [
            ModuleInfo(
                key=descriptor.key,
                name=descriptor.name,
                description=descriptor.description,
                origin="custom"
            )
            for descriptor in pm.available_custom_modules().values()
        ]
        
        return AvailableModulesResponse(
            status="success",
            core_modules=core_modules_info,
            custom_modules=custom_modules_info,
            timestamp=get_iso_timestamp()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Modüller listelenirken hata: {str(e)}")


@router.post(
    "/run",
    response_model=PipelineRunResponse,
    summary="Pipeline Çalıştır",
    responses={
        200: {"description": "Pipeline başarıyla çalıştırıldı"},
        400: {"description": "Hatalı istek (veri formatı)"},
        401: {"description": "Unauthorized - geçersiz API key"},
        500: {"description": "Pipeline çalıştırırken hata"}
    }
)
async def run_pipeline(
    request: PipelineRunByIdRequest,
    pm: PipelineManager = Depends(get_pipeline_manager),
    api_key: str = Depends(verify_api_key)
) -> PipelineRunResponse:
    """
    Verilen DataFrame'de seçili modülleri çalıştır.
    
    Bu endpoint, PipelineManager'ı kullanarak core ve custom modülleri
    dinamik olarak tetikler. Veri JSON dict formatında gönderilir
    ve pandas DataFrame'e dönüştürülür.
    
    Args:
        request: PipelineRunRequest
            - data: Dict[str, List] formatında veri (DataFrame'e çevrilecek)
            - modules: Çalıştırılacak modül keys veya names
    
    Returns:
        PipelineRunResponse: İşlem sonucu
    
    Raises:
        HTTPException: Veri formatı veya modül hatası
    """
    try:
        # upload_id üzerinden çalışacak şekilde revize edildi
        if not request.upload_id:
            raise ValueError("upload_id belirtilmelidir")

        if not request.modules:
            raise ValueError("En az bir modül seçilmelidir")

        # Veritabanından upload kaydını çek
        from db import get_upload_by_id

        record = get_upload_by_id(request.upload_id)
        if not record:
            raise ValueError(f"Upload ID bulunamadı: {request.upload_id}")

        file_path = record.get("file_path")
        if not file_path:
            raise ValueError(f"Upload kaydında file_path yok (upload_id={request.upload_id})")

        # Dosyayı pandas ile oku
        try:
            try:
                df_original = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df_original = pd.read_csv(file_path, encoding='iso-8859-1')
        except Exception as e:
            raise ValueError(f"Dosya okunamadı veya CSV değil: {str(e)}")

        original_shape = df_original.shape

        # PipelineManager'ı oluştur ve çalıştır
        pm_runner = PipelineManager(selected_modules_list=request.modules)
        df_cleaned = pm_runner.run_pipeline(df_original)
        
        cleaned_shape = df_cleaned.shape
        
        # DataFrame'i dict'e dönüştür (JSON serialization için)
        result_data = cast(Dict[str, List[Any]], df_cleaned.to_dict(orient="list"))
        
        return PipelineRunResponse(
            status="success",
            original_shape=original_shape,
            cleaned_shape=cleaned_shape,
            result_data=result_data,
            modules_executed=request.modules,
            message=f"Pipeline başarıyla çalıştırıldı. {len(request.modules)} modül uygulandı.",
            timestamp=get_iso_timestamp()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline hatası: {str(e)}")
