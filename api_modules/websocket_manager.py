"""
WebSocket Manager for Real-Time Progress Streaming
====================================================
Manages WebSocket connections and broadcasts job progress updates
to connected clients in real-time.

Features:
- Connection tracking (list of active connections)
- Broadcast methods for progress updates
- Job-specific subscriptions
- Connection pool management with locks
"""

import json
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from threading import Lock
from fastapi import WebSocket


@dataclass
class ProgressUpdate:
    """Real-time job progress update model."""
    job_id: str
    status: str  # PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED
    progress_percent: int  # 0-100
    current_step: str  # "reading_file", "processing", "saving_results", etc.
    message: str
    timestamp: str  # ISO 8601
    error_details: Optional[str] = None
    
    def to_json(self) -> str:
        """Convert to JSON string for WebSocket transmission."""
        return json.dumps(asdict(self))


class WebSocketManager:
    """
    Singleton: Manages WebSocket connections and broadcasts progress updates.
    
    Thread-safe with Lock for connection list mutations.
    Tracks active connections and job subscriptions.
    """
    
    _instance: Optional['WebSocketManager'] = None
    _lock: Lock = Lock()
    
    def __new__(cls) -> 'WebSocketManager':
        """Singleton pattern: ensure only one instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize WebSocket connection pool."""
        if self._initialized:
            return
        
        self.active_connections: List[WebSocket] = []
        self.job_subscriptions: Dict[str, Set[WebSocket]] = {}  # job_id -> set of WebSocket connections
        self.connection_lock = Lock()
        self._initialized = True
    
    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept and register a WebSocket connection.
        
        Args:
            websocket: FastAPI WebSocket connection
        """
        await websocket.accept()
        with self.connection_lock:
            self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
        """
        with self.connection_lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            
            # Remove from all job subscriptions
            for job_id in list(self.job_subscriptions.keys()):
                if websocket in self.job_subscriptions[job_id]:
                    self.job_subscriptions[job_id].remove(websocket)
                    if not self.job_subscriptions[job_id]:
                        del self.job_subscriptions[job_id]
    
    def subscribe(self, websocket: WebSocket, job_id: str) -> None:
        """
        Subscribe a connection to job progress updates.
        
        Args:
            websocket: WebSocket connection
            job_id: Job ID to subscribe to
        """
        with self.connection_lock:
            if job_id not in self.job_subscriptions:
                self.job_subscriptions[job_id] = set()
            self.job_subscriptions[job_id].add(websocket)
    
    def unsubscribe(self, websocket: WebSocket, job_id: str) -> None:
        """
        Unsubscribe a connection from job progress updates.
        
        Args:
            websocket: WebSocket connection
            job_id: Job ID to unsubscribe from
        """
        with self.connection_lock:
            if job_id in self.job_subscriptions:
                self.job_subscriptions[job_id].discard(websocket)
                if not self.job_subscriptions[job_id]:
                    del self.job_subscriptions[job_id]
    
    async def broadcast(self, update: ProgressUpdate) -> None:
        """
        Broadcast progress update to all subscribed connections for this job.
        
        Args:
            update: ProgressUpdate dataclass with job info
        """
        with self.connection_lock:
            subscribed_connections = list(
                self.job_subscriptions.get(update.job_id, set())
            )
        
        disconnected = []
        for websocket in subscribed_connections:
            try:
                await websocket.send_text(update.to_json())
            except RuntimeError:
                # Connection closed or disconnected
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        if disconnected:
            await self.disconnect(disconnected[0])  # Cleanup via disconnect method
    
    async def broadcast_to_all(self, message: dict) -> None:
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Dictionary message to broadcast
        """
        with self.connection_lock:
            all_connections = list(self.active_connections)
        
        disconnected = []
        for websocket in all_connections:
            try:
                await websocket.send_json(message)
            except RuntimeError:
                disconnected.append(websocket)
        
        # Clean up disconnected connections
        for ws in disconnected:
            await self.disconnect(ws)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections."""
        with self.connection_lock:
            return len(self.active_connections)
    
    def get_job_subscriber_count(self, job_id: str) -> int:
        """Get number of connections subscribed to a specific job."""
        with self.connection_lock:
            return len(self.job_subscriptions.get(job_id, set()))


def get_websocket_manager() -> WebSocketManager:
    """Get WebSocket manager singleton instance."""
    return WebSocketManager()
