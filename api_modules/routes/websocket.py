"""
WebSocket Routes for Real-Time Progress Streaming
===================================================
WebSocket endpoints for job progress tracking and real-time updates.

Endpoints:
- GET /ws/{job_id} - Subscribe to job progress updates
- GET /ws/all - Subscribe to all updates (broadcast channel)

Features:
- Job-specific subscriptions
- Real-time progress updates
- Connection state management
- Error handling with reconnection support
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from typing import Optional
from api_modules.websocket_manager import WebSocketManager, ProgressUpdate
from api_modules.queue import ProcessingQueue
from api_modules.logging_service import StructuredLogger
from datetime import datetime

router = APIRouter(tags=["websocket"])

# Singletons
ws_manager = WebSocketManager()
queue = ProcessingQueue()
logger = StructuredLogger()


@router.websocket("/ws/{job_id}")
async def websocket_job_progress(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time job progress tracking.
    
    Parameters:
        job_id: Job ID to track progress for
    
    Connection Flow:
        1. Client connects with job_id
        2. Server subscribes connection to job updates
        3. Server sends initial job state
        4. Whenever job status changes, server sends update
        5. Client can send commands: {"command": "unsubscribe"}
    
    Message Format:
        {
            "job_id": "uuid",
            "status": "PROCESSING",
            "progress_percent": 45,
            "current_step": "processing",
            "message": "Processing step 2 of 5",
            "timestamp": "2025-11-25T10:30:00.123456",
            "error_details": null
        }
    """
    try:
        # Accept connection
        await ws_manager.connect(websocket)
        logger.debug(
            "WebSocket Connection Accepted",
            context={"job_id": job_id, "action": "connect"}
        )
        
        # Subscribe to this job's updates
        ws_manager.subscribe(websocket, job_id)
        
        # Get current job state and send to client
        job = queue.get_job(job_id)
        if job:
            initial_update = ProgressUpdate(
                job_id=job.id,
                status=job.status.value,
                progress_percent=0 if job.status.value == "PENDING" else (
                    50 if job.status.value == "PROCESSING" else (
                        100 if job.status.value == "COMPLETED" else 0
                    )
                ),
                current_step="waiting" if job.status.value == "PENDING" else (
                    "processing" if job.status.value == "PROCESSING" else (
                        "completed" if job.status.value == "COMPLETED" else "error"
                    )
                ),
                message=f"Job {job.id} status: {job.status.value}",
                timestamp=datetime.utcnow().isoformat(),
                error_details=job.error_message if job.error_message else None
            )
            await websocket.send_text(initial_update.to_json())
        else:
            # Job not found
            error_update = ProgressUpdate(
                job_id=job_id,
                status="ERROR",
                progress_percent=0,
                current_step="error",
                message=f"Job {job_id} not found",
                timestamp=datetime.utcnow().isoformat(),
                error_details="Job ID does not exist in queue"
            )
            await websocket.send_text(error_update.to_json())
        
        # Keep connection open and listen for client commands
        while True:
            try:
                data = await websocket.receive_text()
                
                # Handle client commands
                import json
                try:
                    command = json.loads(data)
                    if command.get("command") == "unsubscribe":
                        ws_manager.unsubscribe(websocket, job_id)
                        await websocket.send_json({
                            "status": "unsubscribed",
                            "job_id": job_id
                        })
                        break
                except json.JSONDecodeError:
                    # Invalid JSON, ignore
                    pass
            
            except WebSocketDisconnect:
                break
    
    except Exception as e:
        logger.error(
            "WebSocket Error",
            context={"job_id": job_id, "action": "error"},
            error=e
        )
    
    finally:
        # Clean up on disconnect
        await ws_manager.disconnect(websocket)
        logger.debug(
            "WebSocket Disconnected",
            context={"job_id": job_id, "action": "disconnect"}
        )


@router.websocket("/ws")
async def websocket_broadcast(
    websocket: WebSocket,
    channel: Optional[str] = Query("all")
):
    """
    WebSocket endpoint for broadcast channel (all job updates).
    
    Parameters:
        channel: Channel name (default: "all")
    
    This endpoint broadcasts updates for ALL jobs to all connected clients.
    Useful for monitoring dashboards that need to see all activity.
    
    Message Format (same as /ws/{job_id}):
        {
            "job_id": "uuid",
            "status": "PROCESSING",
            "progress_percent": 45,
            ...
        }
    """
    try:
        await ws_manager.connect(websocket)
        logger.debug(
            "WebSocket Broadcast Channel Connected",
            context={"channel": channel, "action": "connect"}
        )
        
        # Send welcome message
        await websocket.send_json({
            "status": "connected",
            "channel": channel,
            "message": f"Subscribed to {channel} updates",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep connection open
        while True:
            try:
                data = await websocket.receive_text()
                
                # Handle client commands
                import json
                try:
                    command = json.loads(data)
                    if command.get("command") == "ping":
                        await websocket.send_json({
                            "status": "pong",
                            "timestamp": datetime.utcnow().isoformat()
                        })
                except json.JSONDecodeError:
                    pass
            
            except WebSocketDisconnect:
                break
    
    except Exception as e:
        logger.error(
            "WebSocket Broadcast Error",
            context={"channel": channel, "action": "error"},
            error=e
        )
    
    finally:
        await ws_manager.disconnect(websocket)
        logger.debug(
            "WebSocket Broadcast Disconnected",
            context={"channel": channel, "action": "disconnect"}
        )
