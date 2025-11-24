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
        """GET /health endpoint'ini test et."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data
        assert "timestamp" in data


class TestClean:
    """Text cleaning endpoint tests."""
    
    def test_clean_trim(self):
        """POST /clean endpoint'ini test et (trim)."""
        payload = {
            "data": "  kirli veri  ",
            "operations": ["trim"]
        }
        response = client.post("/clean", json=payload, headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["cleaned_data"] == "kirli veri"
        assert "trim" in data["operations_applied"]
    
    def test_clean_lowercase(self):
        """POST /clean endpoint'ini test et (lowercase)."""
        payload = {
            "data": "KIRLI VERI",
            "operations": ["lowercase"]
        }
        response = client.post("/clean", json=payload, headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["cleaned_data"] == "kirli veri"
    
    def test_clean_multiple_operations(self):
        """POST /clean endpoint'ini test et (multiple ops)."""
        payload = {
            "data": "  KIRLI VERI  ",
            "operations": ["trim", "lowercase"]
        }
        response = client.post("/clean", json=payload, headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["cleaned_data"] == "kirli veri"
    
    def test_clean_missing_api_key(self):
        """POST /clean endpoint'ini test et (missing API key)."""
        payload = {
            "data": "test",
            "operations": ["trim"]
        }
        response = client.post("/clean", json=payload)  # No API key
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestRoot:
    """Root endpoint test."""
    
    def test_root(self):
        """GET / endpoint'ini test et."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NeatData API"
        assert "version" in data
        assert "endpoints" in data


class TestPipeline:
    """Pipeline endpoint tests."""
    
    def test_available_modules(self):
        """GET /pipeline/available endpoint'ini test et."""
        response = client.get("/pipeline/available")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "core_modules" in data
        assert "custom_modules" in data
        assert len(data["core_modules"]) > 0
    
    def test_pipeline_run(self):
        """POST /pipeline/run endpoint'ini test et."""
        payload = {
            "data": {
                "name": ["  John  ", "  Jane  "],
                "age": [25, 30]
            },
            "modules": ["trim_spaces"]
        }
        response = client.post("/pipeline/run", json=payload, headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # JSON serializes tuple as list
        assert data["original_shape"] == [2, 2] or data["original_shape"] == (2, 2)
        assert data["cleaned_shape"] == [2, 2] or data["cleaned_shape"] == (2, 2)
        assert "trim_spaces" in data["modules_executed"]
    
    def test_pipeline_run_missing_api_key(self):
        """POST /pipeline/run endpoint'ini test et (missing API key)."""
        payload = {
            "data": {"col": [1, 2]},
            "modules": ["trim_spaces"]
        }
        response = client.post("/pipeline/run", json=payload)  # No API key
        assert response.status_code == 401


class TestUpload:
    """File upload endpoint tests."""
    
    def test_upload_csv_success(self):
        """POST /upload/csv endpoint'ini test et (valid CSV)."""
        csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA\nBob,35,Chicago"
        
        response = client.post(
            "/upload/csv",
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
        assert data["upload_id"] is None or isinstance(data["upload_id"], int)
    
    def test_upload_csv_invalid_extension(self):
        """POST /upload/csv endpoint'ini test et (invalid extension)."""
        response = client.post(
            "/upload/csv",
            files={"file": ("test_data.xlsx", b"invalid", "application/octet-stream")},
            headers=get_headers_with_key()
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_upload_csv_empty_file(self):
        """POST /upload/csv endpoint'ini test et (empty file)."""
        response = client.post(
            "/upload/csv",
            files={"file": ("test_data.csv", b"", "text/csv")},
            headers=get_headers_with_key()
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_upload_csv_missing_api_key(self):
        """POST /upload/csv endpoint'ini test et (missing API key)."""
        csv_content = b"name,age\nJohn,25"
        response = client.post(
            "/upload/csv",
            files={"file": ("test.csv", csv_content, "text/csv")}
            # No headers with API key
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_upload_csv_invalid_api_key(self):
        """POST /upload/csv endpoint'ini test et (invalid API key)."""
        csv_content = b"name,age\nJohn,25"
        response = client.post(
            "/upload/csv",
            files={"file": ("test.csv", csv_content, "text/csv")},
            headers={"X-API-Key": "invalid-key-12345"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestDatabase:
    """Database endpoint tests."""
    
    def test_get_uploads_history(self):
        """GET /db/uploads endpoint'ini test et."""
        response = client.get("/db/uploads")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_uploads" in data
        assert "uploads" in data
        assert isinstance(data["uploads"], list)
        assert "timestamp" in data
    
    def test_get_upload_details(self):
        """GET /db/uploads/{upload_id} endpoint'ini test et."""
        # İlk olarak boş ID ile test et (bulunamadı)
        response = client.get("/db/uploads/99999")
        assert response.status_code == 404
        
        # Geçerli yanıt formatı kontrol et
        data = response.json()
        assert "detail" in data or "message" in data
    
    def test_get_processing_logs(self):
        """GET /db/logs/{upload_id} endpoint'ini test et."""
        response = client.get("/db/logs/1")
        
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
        """POST /queue/submit endpoint'ini test et."""
        payload = {
            "upload_id": 1,
            "modules": ["trim_spaces", "drop_duplicates"]
        }
        response = client.post("/queue/submit", json=payload, headers=get_headers_with_key())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success" or "id" in data
        assert data["upload_id"] == 1
        assert data["status"] == "pending"
        assert "id" in data
        assert len(data["modules"]) == 2
    
    def test_list_jobs(self):
        """GET /queue/jobs endpoint'ini test et."""
        response = client.get("/queue/jobs", headers=get_headers_with_key())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_jobs" in data
        assert "jobs" in data
        assert isinstance(data["jobs"], list)
    
    def test_get_job_details(self):
        """GET /queue/jobs/{job_id} endpoint'ini test et."""
        # İlk job'u al
        response = client.post(
            "/queue/submit",
            json={"upload_id": 2, "modules": ["trim_spaces"]},
            headers=get_headers_with_key()
        )
        assert response.status_code == 200
        job_data = response.json()
        job_id = job_data["id"]
        
        # Job detaylarını al
        response = client.get(f"/queue/jobs/{job_id}", headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["upload_id"] == 2
    
    def test_get_job_not_found(self):
        """GET /queue/jobs/{job_id} endpoint'ini test et (job bulunamadı)."""
        response = client.get("/queue/jobs/nonexistent-id", headers=get_headers_with_key())
        assert response.status_code == 404
    
    def test_cancel_job(self):
        """POST /queue/jobs/{job_id}/cancel endpoint'ini test et."""
        # Job oluştur
        response = client.post(
            "/queue/submit",
            json={"upload_id": 3, "modules": ["trim_spaces"]},
            headers=get_headers_with_key()
        )
        job_id = response.json()["id"]
        
        # Job'u iptal et
        response = client.post(f"/queue/jobs/{job_id}/cancel", headers=get_headers_with_key())
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["status"] == "cancelled"
    
    def test_queue_stats(self):
        """GET /queue/stats endpoint'ini test et."""
        response = client.get("/queue/stats", headers=get_headers_with_key())
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total_jobs" in data
        assert "pending" in data
        assert "processing" in data
        assert "completed" in data
        assert "failed" in data
        assert "cancelled" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
