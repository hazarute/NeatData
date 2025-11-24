"""
Logging Service
===============
Structured logging for API requests, responses, and errors.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import sys
from enum import Enum


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredLogger:
    """Structured JSON logger for API logging."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("neatdata_api")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler (JSON format)
        self.log_file = self.log_dir / "api.log"
        file_handler = logging.FileHandler(self.log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(file_handler)
        
        # Console handler (JSON format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
        
        self._initialized = True
    
    def _format_log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format log entry as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message
        }
        
        if context:
            log_entry["context"] = context
        
        if extra:
            log_entry.update(extra)
        
        return json.dumps(log_entry)
    
    def debug(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        **extra
    ):
        """Log debug message."""
        log_msg = self._format_log(LogLevel.DEBUG, message, context, extra if extra else None)
        self.logger.debug(log_msg)
    
    def info(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        **extra
    ):
        """Log info message."""
        log_msg = self._format_log(LogLevel.INFO, message, context, extra if extra else None)
        self.logger.info(log_msg)
    
    def warning(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        **extra
    ):
        """Log warning message."""
        log_msg = self._format_log(LogLevel.WARNING, message, context, extra if extra else None)
        self.logger.warning(log_msg)
    
    def error(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None,
        **extra
    ):
        """Log error message."""
        extra_data = extra if extra else {}
        
        if error:
            extra_data["error_type"] = type(error).__name__
            extra_data["error_message"] = str(error)
        
        log_msg = self._format_log(LogLevel.ERROR, message, context, extra_data if extra_data else None)
        self.logger.error(log_msg)
    
    def critical(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Exception] = None,
        **extra
    ):
        """Log critical message."""
        extra_data = extra if extra else {}
        
        if error:
            extra_data["error_type"] = type(error).__name__
            extra_data["error_message"] = str(error)
        
        log_msg = self._format_log(LogLevel.CRITICAL, message, context, extra_data if extra_data else None)
        self.logger.critical(log_msg)
    
    def log_request(
        self,
        method: str,
        path: str,
        query_params: Optional[Dict[str, Any]] = None,
        api_key_masked: Optional[str] = None
    ):
        """Log incoming request."""
        context = {
            "method": method,
            "path": path,
            "query_params": query_params
        }
        
        if api_key_masked:
            context["api_key"] = api_key_masked
        
        self.info("API Request", context=context)
    
    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        response_time_ms: float
    ):
        """Log response."""
        context = {
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": response_time_ms
        }
        
        level = LogLevel.ERROR if status_code >= 500 else LogLevel.INFO
        self.info("API Response", context=context) if level == LogLevel.INFO else self.error("API Response", context=context)
    
    def log_database_operation(
        self,
        operation: str,
        table: str,
        success: bool,
        duration_ms: float,
        rows_affected: int = 0
    ):
        """Log database operation."""
        context = {
            "operation": operation,
            "table": table,
            "success": success,
            "duration_ms": duration_ms,
            "rows_affected": rows_affected
        }
        
        self.info("Database Operation", context=context)
    
    def log_job_event(
        self,
        job_id: str,
        event: str,
        status: Optional[str] = None,
        upload_id: Optional[int] = None,
        modules: Optional[list] = None
    ):
        """Log job queue event."""
        context = {
            "job_id": job_id,
            "event": event,
            "status": status,
            "upload_id": upload_id,
            "modules": modules
        }
        
        self.info("Job Event", context=context)
    
    def log_pipeline_execution(
        self,
        upload_id: int,
        modules: list,
        success: bool,
        duration_ms: float,
        error: Optional[str] = None
    ):
        """Log pipeline execution."""
        context = {
            "upload_id": upload_id,
            "modules": modules,
            "success": success,
            "duration_ms": duration_ms
        }
        
        if error:
            context["error"] = error
        
        if success:
            self.info("Pipeline Execution Success", context=context)
        else:
            self.error("Pipeline Execution Failed", context=context)
