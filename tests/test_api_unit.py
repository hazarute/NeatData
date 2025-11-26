"""
API Unit Tests with TestClient
===============================
FastAPI'nin TestClient'ı kullanarak endpoint'leri test et.
"""

import pytest
from fastapi.testclient import TestClient
from api import app
from api_modules.security import APIKeyManager

client = TestClient(app)

# Test için geçerli API key al
manager = APIKeyManager()
test_keys = list(manager.list_keys().keys())
valid_api_key = test_keys[0] if test_keys else None

# Headers with API key
def get_headers_with_key():
    """API key ile request header'ı oluştur."""
    return {"X-API-Key": valid_api_key} if valid_api_key else {}


class TestHealth:
    """Health check endpoint tests."""
    
    def test_health_success(self):
        """GET /v1/health endpoint'ini test et."""
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data
        assert "timestamp" in data








class TestPipeline:
    """Pipeline endpoint tests."""
    
    def test_available_modules(self):
        """GET /v1/pipeline/available endpoint'ini test et."""
        response = client.get("/v1/pipeline/available")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "core_modules" in data
        assert "custom_modules" in data
        assert len(data["core_modules"]) > 0
    
    def test_pipeline_run(self):
        """POST /v1/pipeline/run endpoint'ini test et."""
        # 1. Önce dosya yükle
        csv_content = b"name,age\n  John  ,25\n  Jane  ,30"
        upload_response = client.post(
            "/v1/upload/csv",
            files={"file": ("test_pipeline.csv", csv_content, "text/csv")},
            headers=get_headers_with_key()
        )
        assert upload_response.status_code == 200
        upload_id = upload_response.json()["upload_id"]
        
        # 2. Pipeline çalıştır
        payload = {
            "upload_id": upload_id,
            "modules": ["trim_spaces"]
        }
        response = client.post("/v1/pipeline/run", json=payload, headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Sonuçları kontrol et
        result_data = data["result_data"]
        assert "name" in result_data
        assert result_data["name"] == ["John", "Jane"]  # Trim edilmiş olmalı
        assert "trim_spaces" in data["modules_executed"]
    
    def test_pipeline_run_missing_api_key(self):
        """POST /v1/pipeline/run endpoint'ini test et (missing API key)."""
        payload = {
            "upload_id": 1,
            "modules": ["trim_spaces"]
        }
        response = client.post("/v1/pipeline/run", json=payload)  # No API key
        assert response.status_code == 401


class TestUpload:
    """File upload endpoint tests."""
    
    def test_upload_csv_success(self):
        """POST /v1/upload/csv endpoint'ini test et (valid CSV)."""
        csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA\nBob,35,Chicago"
        
        response = client.post(
            "/v1/upload/csv",
            files={"file": ("test_data.csv", csv_content, "text/csv")},
            headers=get_headers_with_key()
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["filename"] == "test_data.csv"
        assert data["rows"] == 3
        assert data["columns"] == 3
        assert data["file_size"] == len(csv_content)
        assert "upload_id" in data
        assert isinstance(data["upload_id"], int)
    
    def test_upload_csv_invalid_extension(self):
        """POST /v1/upload/csv endpoint'ini test et (invalid extension)."""
        response = client.post(
            "/v1/upload/csv",
            files={"file": ("test_data.xlsx", b"invalid", "application/octet-stream")},
            headers=get_headers_with_key()
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_upload_csv_empty_file(self):
        """POST /v1/upload/csv endpoint'ini test et (empty file)."""
        response = client.post(
            "/v1/upload/csv",
            files={"file": ("test_data.csv", b"", "text/csv")},
            headers=get_headers_with_key()
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_upload_csv_missing_api_key(self):
        """POST /v1/upload/csv endpoint'ini test et (missing API key)."""
        csv_content = b"name,age\nJohn,25"
        response = client.post(
            "/v1/upload/csv",
            files={"file": ("test.csv", csv_content, "text/csv")}
            # No headers with API key
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_upload_csv_invalid_api_key(self):
        """POST /v1/upload/csv endpoint'ini test et (invalid API key)."""
        csv_content = b"name,age\nJohn,25"
        response = client.post(
            "/v1/upload/csv",
            files={"file": ("test.csv", csv_content, "text/csv")},
            headers={"X-API-Key": "invalid-key-12345"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestDatabase:
    """Database endpoint tests."""
    
    def test_get_uploads_history(self):
        """GET /v1/db/uploads endpoint'ini test et."""
        response = client.get("/v1/db/uploads")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_uploads" in data
        assert "uploads" in data
        assert isinstance(data["uploads"], list)
        assert "timestamp" in data
    
    def test_get_upload_details(self):
        """GET /v1/db/uploads/{upload_id} endpoint'ini test et."""
        # İlk olarak boş ID ile test et (bulunamadı)
        response = client.get("/v1/db/uploads/99999")
        assert response.status_code == 404
        
        # Geçerli yanıt formatı kontrol et
        data = response.json()
        assert "detail" in data or "message" in data
    
    def test_get_processing_logs(self):
        """GET /v1/db/logs/{upload_id} endpoint'ini test et."""
        response = client.get("/v1/db/logs/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "upload_id" in data
        assert "total_logs" in data
        assert "logs" in data
        assert isinstance(data["logs"], list)
        assert "timestamp" in data


class TestQueue:
    """Queue/Batch processing endpoint tests."""
    
    def test_submit_job(self):
        """POST /v1/queue/submit endpoint'ini test et."""
        payload = {
            "upload_id": 1,
            "modules": ["trim_spaces", "drop_duplicates"]
        }
        response = client.post("/v1/queue/submit", json=payload, headers=get_headers_with_key())
        
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success" or "id" in data
        assert data["upload_id"] == 1
        assert data["status"] == "pending"
        assert "id" in data
        assert len(data["modules"]) == 2
    
    def test_list_jobs(self):
        """GET /v1/queue/jobs endpoint'ini test et."""
        response = client.get("/v1/queue/jobs", headers=get_headers_with_key())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_jobs" in data
        assert "jobs" in data
        assert isinstance(data["jobs"], list)
    
    def test_get_job_details(self):
        """GET /v1/queue/jobs/{job_id} endpoint'ini test et."""
        # İlk job'u al
        response = client.post(
            "/v1/queue/submit",
            json={"upload_id": 2, "modules": ["trim_spaces"]},
            headers=get_headers_with_key()
        )
        assert response.status_code == 201
        job_data = response.json()
        job_id = job_data["id"]
        
        # Job detaylarını al
        response = client.get(f"/v1/queue/jobs/{job_id}", headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["upload_id"] == 2
    
    def test_get_job_not_found(self):
        """GET /v1/queue/jobs/{job_id} endpoint'ini test et (job bulunamadı)."""
        response = client.get("/v1/queue/jobs/nonexistent-id", headers=get_headers_with_key())
        assert response.status_code == 404
    
    def test_cancel_job(self):
        """POST /v1/queue/jobs/{job_id}/cancel endpoint'ini test et."""
        # Job oluştur
        response = client.post(
            "/v1/queue/submit",
            json={"upload_id": 3, "modules": ["trim_spaces"]},
            headers=get_headers_with_key()
        )
        job_id = response.json()["id"]
        
        # Job'u iptal et
        response = client.post(f"/v1/queue/jobs/{job_id}/cancel", headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["status"] == "cancelled"
    
    def test_queue_stats(self):
        """GET /v1/queue/stats endpoint'ini test et."""
        response = client.get("/v1/queue/stats", headers=get_headers_with_key())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_jobs" in data
        assert "pending" in data
        assert "processing" in data
        assert "completed" in data
        assert "failed" in data
        assert "cancelled" in data


class TestWebSocket:
    """WebSocket endpoint tests."""
    
    def test_websocket_job_not_found(self):
        """WebSocket /v1/ws/{job_id} endpoint'i - job not found."""
        with client.websocket_connect("/v1/ws/nonexistent-job-id") as websocket:
            data = websocket.receive_text()
            import json
            message = json.loads(data)
            assert message["status"] == "ERROR"
            assert message["job_id"] == "nonexistent-job-id"
            assert "not found" in message["message"].lower()
    
    def test_websocket_submit_and_track(self):
        """WebSocket job submission ve progress tracking."""
        # First, submit a job
        from api_modules.queue import ProcessingQueue
        queue = ProcessingQueue()
        
        payload = {
            "upload_id": 1,
            "modules": ["trim_spaces", "drop_duplicates"]
        }
        response = client.post("/v1/queue/submit", json=payload, headers=get_headers_with_key())
        assert response.status_code == 201
        job_id = response.json()["id"]
        
        # Connect to WebSocket for this job
        with client.websocket_connect(f"/v1/ws/{job_id}") as websocket:
            # Should receive initial job state
            data = websocket.receive_text()
            import json
            message = json.loads(data)
            assert message["job_id"] == job_id
            assert message["status"] in ["pending", "processing", "completed", "failed", "cancelled", "error"]
            assert "progress_percent" in message
            assert "current_step" in message
    
    def test_websocket_progress_update(self):
        """WebSocket progress updates."""
        from api_modules.queue import ProcessingQueue
        queue = ProcessingQueue()
        
        # Submit job
        payload = {
            "upload_id": 1,
            "modules": ["test_module"]
        }
        response = client.post("/v1/queue/submit", json=payload, headers=get_headers_with_key())
        job_id = response.json()["id"]
        
        # Start job
        queue.start_job(job_id)
        
        # Connect and get initial state
        with client.websocket_connect(f"/v1/ws/{job_id}") as websocket:
            # Receive initial state
            data = websocket.receive_text()
            import json
            message = json.loads(data)
            
            # Update progress
            queue.update_job_progress(
                job_id,
                progress_percent=50,
                current_step="processing",
                step_message="Processing step 2 of 5"
            )
            
            # Get updated job
            job = queue.get_job(job_id)
            assert job is not None
            assert job.progress_percent == 50
            assert job.current_step == "processing"
            assert job.step_message == "Processing step 2 of 5"
    
    def test_websocket_broadcast_channel(self):
        """WebSocket broadcast channel."""
        with client.websocket_connect("/v1/ws/?channel=all") as websocket:
            # Should receive welcome message
            data = websocket.receive_json()
            assert data["status"] == "connected"
            assert data["channel"] == "all"
            assert "message" in data
            
            # Send ping command
            websocket.send_json({"command": "ping"})
            response = websocket.receive_json()
            assert response["status"] == "pong"
    
    def test_websocket_unsubscribe_command(self):
        """WebSocket unsubscribe command."""
        from api_modules.queue import ProcessingQueue
        queue = ProcessingQueue()
        
        # Submit job
        payload = {
            "upload_id": 1,
            "modules": ["test"]
        }
        response = client.post("/v1/queue/submit", json=payload, headers=get_headers_with_key())
        job_id = response.json()["id"]
        
        with client.websocket_connect(f"/v1/ws/{job_id}") as websocket:
            # Receive initial state
            websocket.receive_text()
            
            # Send unsubscribe command
            import json
            websocket.send_text(json.dumps({"command": "unsubscribe"}))
            
            # Should receive unsubscribed confirmation
            response = websocket.receive_json()
            assert response["status"] == "unsubscribed"
            assert response["job_id"] == job_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
