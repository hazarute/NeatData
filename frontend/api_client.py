import requests
from typing import List, Dict, Any, Optional
import os

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-API-Key": api_key
        }

    def set_api_key(self, api_key: str):
        """API anahtarını günceller."""
        self.headers["X-API-Key"] = api_key

    def check_health(self) -> bool:
        """API sağlık durumunu kontrol eder."""
        try:
            response = requests.get(f"{self.base_url}/v1/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def get_modules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Mevcut modülleri getirir."""
        try:
            response = requests.get(f"{self.base_url}/v1/pipeline/available", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Modül listesi alınamadı: {e}")
            return {"core_modules": [], "custom_modules": []}

    def upload_file(self, file_obj) -> Optional[int]:
        """
        Dosyayı yükler ve upload_id döner.
        file_obj: Streamlit UploadedFile veya file-like object
        """
        try:
            # Streamlit file object'in name attribute'u vardır
            files = {"file": (file_obj.name, file_obj, "text/csv")}
            response = requests.post(
                f"{self.base_url}/v1/upload/csv",
                headers=self.headers,
                files=files
            )
            response.raise_for_status()
            data = response.json()
            return data.get("upload_id")
        except requests.exceptions.RequestException as e:
            print(f"Dosya yükleme hatası: {e}")
            return None

    def run_pipeline(self, upload_id: int, modules: List[str]) -> Optional[Dict[str, Any]]:
        """
        Pipeline'ı çalıştırır.
        """
        try:
            payload = {
                "upload_id": upload_id,
                "modules": modules
            }
            response = requests.post(
                f"{self.base_url}/v1/pipeline/run",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Pipeline hatası: {e}")
            return None
