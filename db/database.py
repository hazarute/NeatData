"""
Database Models
===============
SQLAlchemy ORM modelleri - SQLite database şeması.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Database file path
DB_PATH = Path(__file__).parent / "neatdata.db"


class Database:
    """SQLite database manager - singleton pattern."""
    
    _instance: Optional['Database'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.db_path = DB_PATH
        self._initialized = True
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Uploads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                rows INTEGER NOT NULL,
                columns INTEGER NOT NULL,
                original_shape TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                status TEXT DEFAULT 'success'
            )
        """)
        
        # Processing logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id INTEGER,
                module_name TEXT NOT NULL,
                module_origin TEXT,
                status TEXT DEFAULT 'success',
                error_message TEXT,
                execution_time_ms REAL,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (upload_id) REFERENCES uploads(id)
            )
        """)
        
        # Pipeline results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id INTEGER,
                modules_applied TEXT,
                original_shape TEXT,
                cleaned_shape TEXT,
                execution_time_ms REAL,
                result_saved INTEGER DEFAULT 0,
                result_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (upload_id) REFERENCES uploads(id)
            )
        """)
        
        conn.commit()
        conn.close()


class UploadRecord:
    """Upload record model."""
    
    def __init__(
        self,
        filename: str,
        file_size: int,
        rows: int,
        columns: int,
        original_shape: str,
        user_agent: Optional[str] = None,
        id: Optional[int] = None
    ):
        self.id = id
        self.filename = filename
        self.file_size = file_size
        self.rows = rows
        self.columns = columns
        self.original_shape = original_shape
        self.user_agent = user_agent
        self.uploaded_at = datetime.utcnow()
        self.status = "success"
    
    def save(self) -> int:
        """Save to database and return ID."""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO uploads 
            (filename, file_size, rows, columns, original_shape, user_agent, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.filename,
            self.file_size,
            self.rows,
            self.columns,
            self.original_shape,
            self.user_agent,
            self.status
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "file_size": self.file_size,
            "rows": self.rows,
            "columns": self.columns,
            "original_shape": self.original_shape,
            "status": self.status,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class ProcessingLog:
    """Processing log model."""
    
    def __init__(
        self,
        upload_id: int,
        module_name: str,
        module_origin: str = "core",
        status: str = "success",
        error_message: Optional[str] = None,
        execution_time_ms: Optional[float] = None
    ):
        self.upload_id = upload_id
        self.module_name = module_name
        self.module_origin = module_origin
        self.status = status
        self.error_message = error_message
        self.execution_time_ms = execution_time_ms
        self.processed_at = datetime.utcnow()
    
    def save(self) -> int:
        """Save to database and return ID."""
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO processing_logs
            (upload_id, module_name, module_origin, status, error_message, execution_time_ms)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.upload_id,
            self.module_name,
            self.module_origin,
            self.status,
            self.error_message,
            self.execution_time_ms
        ))
        
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        return log_id


def get_upload_by_id(upload_id: int) -> Optional[Dict[str, Any]]:
    """Get upload record by ID."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM uploads WHERE id = ?", (upload_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_all_uploads() -> List[Dict[str, Any]]:
    """Get all upload records."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM uploads ORDER BY uploaded_at DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_logs_by_upload_id(upload_id: int) -> List[Dict[str, Any]]:
    """Get processing logs for an upload."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM processing_logs WHERE upload_id = ? ORDER BY processed_at DESC",
        (upload_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
