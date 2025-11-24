"""
API Unit Tests with TestClient
===============================
FastAPI'nin TestClient'ı kullanarak endpoint'leri test et.
"""

import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


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
        response = client.post("/clean", json=payload)
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
        response = client.post("/clean", json=payload)
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
        response = client.post("/clean", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["cleaned_data"] == "kirli veri"


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
        response = client.post("/pipeline/run", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # JSON serializes tuple as list
        assert data["original_shape"] == [2, 2] or data["original_shape"] == (2, 2)
        assert data["cleaned_shape"] == [2, 2] or data["cleaned_shape"] == (2, 2)
        assert "trim_spaces" in data["modules_executed"]


class TestUpload:
    """File upload endpoint tests."""
    
    def test_upload_csv_success(self):
        """POST /upload/csv endpoint'ini test et (valid CSV)."""
        csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA\nBob,35,Chicago"
        
        response = client.post(
            "/upload/csv",
            files={"file": ("test_data.csv", csv_content, "text/csv")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["filename"] == "test_data.csv"
        assert data["rows"] == 3
        assert data["columns"] == 3
        assert data["file_size"] == len(csv_content)
    
    def test_upload_csv_invalid_extension(self):
        """POST /upload/csv endpoint'ini test et (invalid extension)."""
        response = client.post(
            "/upload/csv",
            files={"file": ("test_data.xlsx", b"invalid", "application/octet-stream")}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_upload_csv_empty_file(self):
        """POST /upload/csv endpoint'ini test et (empty file)."""
        response = client.post(
            "/upload/csv",
            files={"file": ("test_data.csv", b"", "text/csv")}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
