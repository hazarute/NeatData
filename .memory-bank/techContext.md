# Tech Context

## Teknoloji Yığını
* **Dil:** Python 3.10+
* **GUI:** CustomTkinter (Modern masaüstü UI)
* **Veri İşleme:** Pandas (Core & Custom modüller için)
* **Sistem:** `importlib` (Dinamik modül yükleme), `threading` (Arka plan işlemleri)
* **Web API:** FastAPI (Modern, hızlı REST framework)
* **API Routing:** APIRouter (Blueprint Pattern)
* **Server:** Uvicorn (ASGI server)
* **Validasyon:** Pydantic (API request/response şemaları)
* **Serialization:** JSON (API veri formatı)

## Klasör Yapısı (Güncel - Faz 6)
```text
NeatData/
├── neatdata_gui.py                    # GUI entry point
├── api.py                             # API entry point (app factory)
│
├── modules/
│   ├── core/                          # Standart temizlik araçları (dropna, trim vb.)
│   ├── custom/                        # Müşteriye özel pluginler (process() + META)
│   ├── pipeline_manager.py            # Modül keşif ve çalıştırma motoru
│   ├── pipeline_config.toml
│   └── utils/                         # GUI utilities
│       ├── gui_helpers.py
│       ├── gui_io.py
│       ├── gui_logger.py
│       ├── pipeline_runner.py
│       └── ui_state.py
│
├── api_modules/                       # API-specific modüller (Blueprint yaklaşımı)
│   ├── __init__.py
│   ├── models.py                      # 7 Pydantic model (200 satır)
│   ├── dependencies.py                # FastAPI dependencies (PipelineManager factory)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py                  # GET /health (50 satır)
│   │   ├── clean.py                   # POST /clean (80 satır)
│   │   ├── pipeline.py                # GET/POST /pipeline/* (120 satır)
│   │   └── info.py                    # GET / (30 satır)
│   └── utils/
│       ├── __init__.py
│       ├── validators.py              # Input validation
│       ├── responses.py               # Response formatters
│       └── timestamp.py               # Utility functions
│
├── tests/
│   ├── test_core_modules.py
│   ├── test_clean_hepsiburada_scrape.py
│   ├── test_text_normalize.py
│   ├── test_text_normalize_extended.py
│   ├── test_io_save_csv.py
│   ├── test_cafe_business_logic.py
│   └── api/                           # API tests
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_clean.py
│       └── test_pipeline.py
│
├── requirements.txt
├── ReadMe.md
└── ...
```

## API Modülerleştirme (Blueprint Pattern)

### Dosya Sorumlulukları

| Dosya | Satır | Sorumluluk |
|-------|-------|-----------|
| **api.py** | 30-40 | App factory, router registration |
| **api_modules/models.py** | 200 | 7 Pydantic model |
| **api_modules/routes/health.py** | 50 | GET /health endpoint |
| **api_modules/routes/clean.py** | 80 | POST /clean endpoint |
| **api_modules/routes/pipeline.py** | 120 | GET /pipeline/available, POST /pipeline/run |
| **api_modules/routes/info.py** | 30 | GET / endpoint |
| **api_modules/utils/validators.py** | 50 | Input validation functions |
| **api_modules/utils/responses.py** | 50 | Response formatters |
| **api_modules/utils/timestamp.py** | 20 | get_iso_timestamp() ve helpers |
| **api_modules/dependencies.py** | 40 | PipelineManager factory dependency |

### Blueprint App Factory Örneği
```python
# api.py (clean)
from fastapi import FastAPI
from api_modules.routes import health, clean, pipeline, info

def create_app() -> FastAPI:
    app = FastAPI(title="NeatData API", version="1.0.0", docs_url="/docs")
    
    app.include_router(health.router)
    app.include_router(clean.router)
    app.include_router(pipeline.router)
    app.include_router(info.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
```

## API Çalıştırma
```bash
uvicorn api:app --reload
# Swagger UI: http://127.0.0.1:8000/docs
```

## Test Çalıştırma
```bash
# Tüm testler
pytest

# Sadece API testleri
pytest tests/api/

# Single test
pytest tests/api/test_pipeline.py::test_pipeline_run
```
