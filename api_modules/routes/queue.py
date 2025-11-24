"""
Queue Routes
============
Batch processing job queue endpoint'leri.
"""

from fastapi import APIRouter, HTTPException, Depends
from api_modules.models import (
    PipelineRunRequest,
)
from api_modules.security import verify_api_key
from api_modules.queue import ProcessingQueue, JobStatus
from api_modules.utils import get_iso_timestamp
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/queue", tags=["Queue"])


class JobSubmitRequest(BaseModel):
    """Job submission request."""
    upload_id: int
    modules: List[str]
    
    class Config:
        example = {
            "upload_id": 1,
            "modules": ["trim_spaces", "drop_duplicates"]
        }


class JobResponse(BaseModel):
    """Job response model."""
    id: str
    upload_id: int
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    modules: List[str]
    error_message: Optional[str] = None


class JobListResponse(BaseModel):
    """Job list response."""
    status: str
    total_jobs: int
    jobs: List[JobResponse]
    timestamp: str


class QueueStatsResponse(BaseModel):
    """Queue statistics response."""
    status: str
    total_jobs: int
    pending: int
    processing: int
    completed: int
    failed: int
    cancelled: int
    timestamp: str


@router.post(
    "/submit",
    response_model=JobResponse,
    status_code=201,
    summary="Job'u Queue'ya Gönder",
    responses={
        201: {"description": "Job başarıyla queue'ya eklendi"},
        400: {"description": "Hatalı istek (upload_id, modules)"},
        401: {"description": "Unauthorized - geçersiz API key"},
        500: {"description": "Sunucu hatası"}
    }
)
async def submit_job(
    request: JobSubmitRequest,
    api_key: str = Depends(verify_api_key)
) -> JobResponse:
    """
    Pipeline işlemini batch olarak queue'ya gönder.
    
    Bu endpoint, verilen upload ve modüller için bir job oluşturur
    ve işlenmek üzere queue'ya ekler. Job'un durumunu daha sonra
    sorgulayabilirsiniz.
    
    Args:
        request: JobSubmitRequest
            - upload_id: İşlenecek upload'ın ID'si
            - modules: Çalıştırılacak modül listesi
    
    Returns:
        JobResponse: Oluşturulan job'un bilgileri
    
    Raises:
        HTTPException: Hatalı istek veya sunucu hatası
    """
    try:
        if not request.upload_id or not request.modules:
            raise ValueError("upload_id ve modules gereklidir")
        
        queue = ProcessingQueue()
        job = queue.submit_job(request.upload_id, request.modules)
        
        return JobResponse(
            id=job.id,
            upload_id=job.upload_id,
            status=job.status.value,
            created_at=job.created_at,
            modules=job.modules
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job gönderilirken hata: {str(e)}")


@router.get(
    "/jobs",
    response_model=JobListResponse,
    summary="Tüm Job'ları Listele",
    responses={
        200: {"description": "Job'lar başarıyla listelendi"},
        500: {"description": "Sunucu hatası"}
    }
)
async def list_jobs(
    status: Optional[str] = None,
    api_key: Optional[str] = Depends(verify_api_key)
) -> JobListResponse:
    """
    Tüm job'ları listele (isteğe bağlı olarak durum filtresiyle).
    
    Args:
        status: İsteğe bağlı durum filtresi (pending, processing, completed, failed, cancelled)
        api_key: API authentication
    
    Returns:
        JobListResponse: Job listesi
    """
    try:
        queue = ProcessingQueue()
        all_jobs = queue.get_all_jobs()
        
        # Filter by status if provided
        if status:
            try:
                status_enum = JobStatus[status.upper()]
                all_jobs = [j for j in all_jobs if j.status == status_enum]
            except KeyError:
                raise ValueError(f"Geçersiz status: {status}")
        
        jobs = [
            JobResponse(
                id=j.id,
                upload_id=j.upload_id,
                status=j.status.value,
                created_at=j.created_at,
                started_at=j.started_at,
                completed_at=j.completed_at,
                modules=j.modules,
                error_message=j.error_message
            )
            for j in all_jobs
        ]
        
        return JobListResponse(
            status="success",
            total_jobs=len(jobs),
            jobs=jobs,
            timestamp=get_iso_timestamp()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job'lar listelenirken hata: {str(e)}")


@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    summary="Job Detaylarını Getir",
    responses={
        200: {"description": "Job detayları başarıyla alındı"},
        404: {"description": "Job bulunamadı"},
        500: {"description": "Sunucu hatası"}
    }
)
async def get_job_details(
    job_id: str,
    api_key: Optional[str] = Depends(verify_api_key)
) -> JobResponse:
    """
    Belirli bir job'un detaylarını getir.
    
    Args:
        job_id: Job ID'si
        api_key: API authentication
    
    Returns:
        JobResponse: Job detayları
    
    Raises:
        HTTPException: Job bulunamadı veya server hatası
    """
    try:
        queue = ProcessingQueue()
        job = queue.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} bulunamadı")
        
        return JobResponse(
            id=job.id,
            upload_id=job.upload_id,
            status=job.status.value,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            modules=job.modules,
            error_message=job.error_message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job detayları alınırken hata: {str(e)}")


@router.post(
    "/jobs/{job_id}/cancel",
    response_model=JobResponse,
    summary="Job'u İptal Et",
    responses={
        200: {"description": "Job başarıyla iptal edildi"},
        404: {"description": "Job bulunamadı"},
        409: {"description": "Job iptal edilemez (durumu uygun değil)"},
        401: {"description": "Unauthorized - geçersiz API key"},
        500: {"description": "Sunucu hatası"}
    }
)
async def cancel_job(
    job_id: str,
    api_key: str = Depends(verify_api_key)
) -> JobResponse:
    """
    Pending veya Processing durumundaki job'u iptal et.
    
    Args:
        job_id: İptal edilecek job'un ID'si
        api_key: API authentication
    
    Returns:
        JobResponse: İptal edilen job'un bilgileri
    
    Raises:
        HTTPException: Job bulunamadı, iptal edilemez, veya server hatası
    """
    try:
        queue = ProcessingQueue()
        job = queue.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} bulunamadı")
        
        if job.status not in [JobStatus.PENDING, JobStatus.PROCESSING]:
            raise HTTPException(
                status_code=409,
                detail=f"Job iptal edilemez (durumu: {job.status.value})"
            )
        
        if not queue.cancel_job(job_id):
            raise HTTPException(status_code=409, detail="Job iptal edilemedi")
        
        job = queue.get_job(job_id)  # Refresh
        return JobResponse(
            id=job.id,
            upload_id=job.upload_id,
            status=job.status.value,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            modules=job.modules,
            error_message=job.error_message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job iptal edilirken hata: {str(e)}")


@router.get(
    "/stats",
    response_model=QueueStatsResponse,
    summary="Queue İstatistikleri",
    responses={
        200: {"description": "İstatistikler başarıyla alındı"},
        500: {"description": "Sunucu hatası"}
    }
)
async def get_queue_stats(
    api_key: Optional[str] = Depends(verify_api_key)
) -> QueueStatsResponse:
    """
    Queue'daki job'ların istatistiklerini getir.
    
    Returns:
        QueueStatsResponse: İstatistikler
    """
    try:
        queue = ProcessingQueue()
        stats = queue.get_queue_stats()
        
        return QueueStatsResponse(
            status="success",
            total_jobs=stats["total_jobs"],
            pending=stats["pending"],
            processing=stats["processing"],
            completed=stats["completed"],
            failed=stats["failed"],
            cancelled=stats["cancelled"],
            timestamp=get_iso_timestamp()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İstatistikler alınırken hata: {str(e)}")
