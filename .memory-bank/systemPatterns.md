# System Patterns

## Mimari Tasarım (Modular & Layered & Multi-Interface & Blueprint)

Proje, sorumlulukların ayrıldığı katmanlı bir mimari izler. **Birden fazla interface (GUI & API)** aynı Core'u kullanır ve **Blueprint Pattern** ile API modülerleştirilir:

```
┌─────────────────────────────────────────┐
│  Client Layer (Interface)               │
├─────────────────────────────────────────┤
│  GUI (CustomTkinter)  │  API (FastAPI) │
│  neatdata_gui.py      │  api.py        │
├─────────────────────────────────────────┤
│  API Blueprints (Modular Routing)       │
│  api_modules/routes/*.py (health,clean) │
├─────────────────────────────────────────┤
│  Controller / Orchestrator              │
│  PipelineRunner (GUI) │ Dependencies    │
├─────────────────────────────────────────┤
│  Core Business Logic                    │
│  PipelineManager (Dinamik Modül Yükle) │
├─────────────────────────────────────────┤
│  Plugins (Core & Custom)                │
│  modules/core/* + modules/custom/*      │
└─────────────────────────────────────────┘
```

### Katmanlar

1.  **View / Interface Layer:**
    * **GUI (`neatdata_gui.py`):** CustomTkinter tabanlı masaüstü uygulaması. "Aptal" katman, iş mantığı yok.
    * **API (`api.py`):** FastAPI app factory. Router registration ve middleware setup.

2.  **API Blueprint Layer (YENİ - Faz 6):**
    * **`api_modules/routes/health.py`:** `GET /health` endpoint (50 satır)
    * **`api_modules/routes/clean.py`:** `POST /clean` endpoint (80 satır)
    * **`api_modules/routes/pipeline.py`:** `GET/POST /pipeline/*` endpoint'leri (120 satır)
    * **`api_modules/routes/info.py`:** `GET /` endpoint (30 satır)
    * Her route `APIRouter` ile ayrı olarak kaydediliyor
    * **`api_modules/models.py`:** 7 Pydantic model (200 satır)
    * **`api_modules/utils/`:** Validator'lar, response formatters, utility fonksiyonlar
    * **`api_modules/dependencies.py`:** FastAPI dependencies (PipelineManager factory)

3.  **Controller / Orchestrator Layer:**
    * **GUI için:** `modules/utils/pipeline_runner.py` → Süreci yönetir, GUI ↔ Backend köprüsü.
    * **API için:** `api_modules/dependencies.py` → PipelineManager instance'ı sağlar.

4.  **Core Logic (`modules/pipeline_manager.py`):**
    * Dinamik modül yükleyicisidir.
    * `modules/core/` ve `modules/custom/` klasörlerini tarar.
    * Seçilen modülleri sırasıyla çalıştırır (`run_pipeline`).
    * GUI ve API'den çağrılabilir.

5.  **Plugins (Core & Custom):**
    * Tüm temizlik işlemleri bağımsız `.py` dosyalarıdır.
    * Protokol: `process(df: pd.DataFrame, **kwargs) -> pd.DataFrame`
    * Metadata: `META` sözlüğü ile tanımlanır.

## Tasarım Desenleri

### 1. Blueprint Pattern (API Modülerleştirme)
FastAPI `APIRouter` kullanarak route'ları bölünmüş dosyalara organize etme:
- Her endpoint'in kendi dosyası olması (Single Responsibility)
- `api.py` sadece app factory ve router registration
- Test etmesi ve bakımı kolay

### 2. Dependency Injection
FastAPI `Depends()` kullanarak:
- `get_pipeline_manager()` → PipelineManager instance'ı inject etme
- Request-scoped dependencies

### 3. Plugin (Eklenti) Deseni
Custom modüller dinamik olarak keşfedilir. Her plugin şu protokolü uygulamalıdır:
* **Fonksiyon:** `process(df: pd.DataFrame, **kwargs) -> pd.DataFrame`
* **Metadata:** `META` sözlüğü (key, name, description, defaults)

### 4. Helper / Utility Ayrımı
- **`modules/utils/`:** GUI utilities (gui_helpers, gui_io, gui_logger, pipeline_runner, ui_state)
- **`api_modules/utils/`:** API utilities (validators, responses, timestamp)

## Kod Standartları
* **Type Hinting:** Tüm fonksiyonlarda tip tanımlamaları kullanılmalı.
* **Docstrings:** Modüllerin ve fonksiyonların açıklaması.
* **API Response:** Yapılandırılmış JSON (status + data + timestamp).
* **Pydantic Models:** API request/response şemaları.
* **Blueprint Organization:** Her route kendi dosyasında, max 100-150 satır/dosya.