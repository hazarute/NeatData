"""
Queue System
============
Batch processing için job queue sistemi (in-memory + database logging).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
import uuid
from threading import Lock
import json

class JobStatus(str, Enum):
    """Job durumları."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Batch processing job."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    upload_id: int = field(default=0)
    status: JobStatus = JobStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    modules: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    progress_percent: int = 0  # 0-100
    current_step: str = ""  # e.g., "reading_file", "processing", "saving_results"
    step_message: str = ""  # Detailed message about current step
    
    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {
            "id": self.id,
            "upload_id": self.upload_id,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "modules": self.modules,
            "error_message": self.error_message,
            "progress_percent": self.progress_percent,
            "current_step": self.current_step,
            "step_message": self.step_message
        }


class ProcessingQueue:
    """In-memory job queue (FIFO)."""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._queue: List[Job] = []  # FIFO queue
        self._jobs: Dict[str, Job] = {}  # Job ID -> Job mapping
        self._lock = Lock()
        self._initialized = True
    
    def submit_job(self, upload_id: int, modules: List[str]) -> Job:
        """Job'u queue'ya ekle."""
        job = Job(
            upload_id=upload_id,
            modules=modules,
            status=JobStatus.PENDING
        )
        
        with self._lock:
            self._queue.append(job)
            self._jobs[job.id] = job
        
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Job'u ID'ye göre al."""
        return self._jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Job]:
        """Tüm job'ları getir."""
        return list(self._jobs.values())
    
    def get_pending_jobs(self) -> List[Job]:
        """Pending job'ları getir (FIFO sırasında)."""
        with self._lock:
            return [j for j in self._queue if j.status == JobStatus.PENDING]
    
    def start_job(self, job_id: str) -> bool:
        """Job'u başla (PROCESSING durumuna geç)."""
        job = self._jobs.get(job_id)
        if not job:
            return False
        
        with self._lock:
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.PROCESSING
                job.started_at = datetime.utcnow().isoformat()
                return True
        
        return False
    
    def complete_job(self, job_id: str) -> bool:
        """Job'u tamamla (COMPLETED durumuna geç)."""
        job = self._jobs.get(job_id)
        if not job:
            return False
        
        with self._lock:
            if job.status == JobStatus.PROCESSING:
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.utcnow().isoformat()
                # Queue'dan çıkar
                if job in self._queue:
                    self._queue.remove(job)
                return True
        
        return False
    
    def fail_job(self, job_id: str, error_message: str) -> bool:
        """Job'u başarısız işaretle."""
        job = self._jobs.get(job_id)
        if not job:
            return False
        
        with self._lock:
            job.status = JobStatus.FAILED
            job.error_message = error_message
            job.completed_at = datetime.utcnow().isoformat()
            # Queue'dan çıkar
            if job in self._queue:
                self._queue.remove(job)
            return True
        
        return False
    
    def cancel_job(self, job_id: str) -> bool:
        """Job'u iptal et."""
        job = self._jobs.get(job_id)
        if not job:
            return False
        
        with self._lock:
            if job.status in [JobStatus.PENDING, JobStatus.PROCESSING]:
                job.status = JobStatus.CANCELLED
                job.completed_at = datetime.utcnow().isoformat()
                # Queue'dan çıkar
                if job in self._queue:
                    self._queue.remove(job)
                return True
        
        return False
    
    def get_queue_stats(self) -> dict:
        """Queue istatistikleri."""
        with self._lock:
            all_jobs = list(self._jobs.values())
            return {
                "total_jobs": len(all_jobs),
                "pending": len([j for j in all_jobs if j.status == JobStatus.PENDING]),
                "processing": len([j for j in all_jobs if j.status == JobStatus.PROCESSING]),
                "completed": len([j for j in all_jobs if j.status == JobStatus.COMPLETED]),
                "failed": len([j for j in all_jobs if j.status == JobStatus.FAILED]),
                "cancelled": len([j for j in all_jobs if j.status == JobStatus.CANCELLED])
            }
    
    def update_job_progress(
        self,
        job_id: str,
        progress_percent: int,
        current_step: str = "",
        step_message: str = ""
    ) -> bool:
        """
        Update job progress without changing status.
        
        Args:
            job_id: Job ID
            progress_percent: Progress percentage (0-100)
            current_step: Current processing step (e.g., "reading_file")
            step_message: Detailed message about the step
        
        Returns:
            True if update successful, False if job not found
        """
        job = self._jobs.get(job_id)
        if not job:
            return False
        
        with self._lock:
            job.progress_percent = min(100, max(0, progress_percent))
            job.current_step = current_step
            job.step_message = step_message
            return True
