"""
API Test Script
Endpoint'leri hızlıca test etmek için.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Health check endpoint'ini test et."""
    print("\n" + "="*60)
    print("TEST 1: GET /health")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_clean_trim():
    """POST /clean endpoint'ini test et (trim işlemi)."""
    print("\n" + "="*60)
    print("TEST 2: POST /clean (Trim işlemi)")
    print("="*60)
    payload = {
        "data": "  kirli veri  ",
        "operations": ["trim"]
    }
    print(f"Request:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/clean", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_clean_lowercase():
    """POST /clean endpoint'ini test et (lowercase işlemi)."""
    print("\n" + "="*60)
    print("TEST 3: POST /clean (Lowercase işlemi)")
    print("="*60)
    payload = {
        "data": "KİRLİ VERİ",
        "operations": ["lowercase"]
    }
    print(f"Request:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/clean", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_clean_multiple():
    """POST /clean endpoint'ini test et (multiple işlemler)."""
    print("\n" + "="*60)
    print("TEST 4: POST /clean (Multiple işlemler: trim + lowercase)")
    print("="*60)
    payload = {
        "data": "  KİRLİ VERİ  ",
        "operations": ["trim", "lowercase"]
    }
    print(f"Request:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/clean", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_root():
    """Ana sayfa endpoint'ini test et."""
    print("\n" + "="*60)
    print("TEST 5: GET / (Ana sayfa)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_available_modules():
    """GET /pipeline/available endpoint'ini test et."""
    print("\n" + "="*60)
    print("TEST 6: GET /pipeline/available (Mevcut modülleri listele)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/pipeline/available")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"Core Modülleri: {len(data.get('core_modules', []))}")
    print(f"Custom Modülleri: {len(data.get('custom_modules', []))}")
    return response.status_code == 200


def test_pipeline_run():
    """POST /pipeline/run endpoint'ini test et."""
    print("\n" + "="*60)
    print("TEST 7: POST /pipeline/run")
    print("="*60)
    payload = {
        "data": {
            "name": ["  John  ", "  Jane  "],
            "age": [25, 30]
        },
        "modules": ["trim_spaces"]
    }
    print(f"Request:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
    response = requests.post(f"{BASE_URL}/pipeline/run", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


def test_upload_csv():
    """POST /upload/csv endpoint'ini test et."""
    print("\n" + "="*60)
    print("TEST 8: POST /upload/csv (CSV dosyası yükle)")
    print("="*60)
    
    # Test CSV dosyası oluştur
    csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA\nBob,35,Chicago"
    
    # Multipart/form-data ile gönder
    files = {'file': ('test_data.csv', csv_content, 'text/csv')}
    print(f"File: test_data.csv ({len(csv_content)} bytes)")
    response = requests.post(f"{BASE_URL}/upload/csv", files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200


if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█  NeatData API Test Suite (Extended)")
    print("█"*60)
    
    try:
        results = []
        results.append(("Health Check", test_health()))
        results.append(("Clean (Trim)", test_clean_trim()))
        results.append(("Clean (Lowercase)", test_clean_lowercase()))
        results.append(("Clean (Multiple)", test_clean_multiple()))
        results.append(("Root", test_root()))
        results.append(("Available Modules", test_available_modules()))
        results.append(("Pipeline Run", test_pipeline_run()))
        results.append(("Upload CSV", test_upload_csv()))
        
        print("\n" + "="*60)
        print("SONUÇLAR")
        print("="*60)
        for test_name, passed in results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status:10} - {test_name}")
        
        total = len(results)
        passed_count = sum(1 for _, p in results if p)
        print(f"\nToplam: {passed_count}/{total} test geçti")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ HATA: API'ye bağlanılamadı!")
        print("Lütfen uvicorn api:app --reload komutunu çalıştırdığınızdan emin olun.")
    except Exception as e:
        print(f"\n❌ Beklenmedik hata: {e}")
