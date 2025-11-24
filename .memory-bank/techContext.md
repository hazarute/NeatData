# Tech Context

## Teknoloji Yığını
* **Dil:** Python 3.10+
* **GUI:** CustomTkinter (Modern masaüstü UI)
* **Veri İşleme:** Pandas (Core & Custom modüller için)
* **Sistem:** `importlib` (Dinamik modül yükleme), `threading` (Arka plan işlemleri)
* **Web API:** FastAPI 0.121.3 (Modern, hızlı REST framework)
* **API Routing:** APIRouter (Blueprint Pattern)
* **Server:** Uvicorn (ASGI server)
* **Validasyon:** Pydantic 2.12.4 (API request/response şemaları)
* **Database:** SQLite3 (Veri depolama, auto-initialize)
* **Authentication:** UUID-based API Keys (stateless, expiration support)
* **Logging:** Structured JSON logging (file + console output)
* **Serialization:** JSON (API veri formatı, log formatı)
* **Concurrency:** threading.Lock (Queue thread-safety)

## Klasör Yapısı (Güncel - Faz 7 Adım 1-6 TAMAMLANDI)
```text
NeatData/
├── neatdata_gui.py                    # GUI entry point
├── api.py                             # API entry point (app factory, logging middleware)
├── clean_data.py
│
├── modules/
│   ├── core/                          # Standart temizlik araçları
│   ├── custom/                        # Müşteriye özel pluginler
│   ├── pipeline_manager.py            # Modül keşif ve çalıştırma motoru
│   ├── pipeline_config.toml
│   └── utils/
│       ├── gui_helpers.py
│       ├── gui_io.py
│       ├── gui_logger.py
│       ├── pipeline_runner.py
│       └── ui_state.py
│
├── db/                                # Database layer (NEW - Faz 7 Step 2)
│   ├── __init__.py
│   └── database.py                    # SQLite singleton, ORM models, helpers
│
├── api_modules/                       # API-specific modüller (Blueprint yaklaşımı)
│   ├── __init__.py
│   ├── models.py                      # 13 Pydantic model (280 satır)
│   ├── dependencies.py                # FastAPI dependencies
│   ├── security.py                    # API Key auth (NEW - Faz 7 Step 4, 250 satır)
│   ├── queue.py                       # Batch queue system (NEW - Faz 7 Step 5, 200 satır)
│   ├── logging_service.py             # Structured logging (NEW - Faz 7 Step 6, 200 satır)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py                  # GET /health (public)
│   │   ├── clean.py                   # POST /clean (protected)
│   │   ├── pipeline.py                # GET/POST /pipeline/* (partially protected)
│   │   ├── info.py                    # GET / (public)
│   │   ├── upload.py                  # POST /upload/csv (NEW - Faz 7 Step 1, protected)
│   │   ├── database.py                # GET /db/* (NEW - Faz 7 Step 2, protected)
│   │   └── queue.py                   # 5 queue endpoints (NEW - Faz 7 Step 5, protected)
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── responses.py
│       ├── timestamp.py
│       ├── gui_helpers.py
│       ├── gui_io.py
│       ├── gui_logger.py
│       └── pipeline_runner.py
│
├── tests/
│   ├── test_core_modules.py
│   ├── test_api_unit.py               # Comprehensive API tests (23/23 PASS)
│   ├── generate_messy_data.py
│   ├── test_cafe_business_logic.py
│   ├── test_clean_hepsiburada_scrape.py
│   ├── test_io_save_csv.py
│   ├── test_text_normalize.py
│   ├── test_text_normalize_extended.py
│   └── TEST_REPORT.md
│
├── logs/                              # Logging directory (NEW - Faz 7 Step 6, auto-created)
│   └── api.log                        # Structured JSON logs
│
├── db/                                # Database directory (NEW - Faz 7 Step 2)
│   └── neatdata.db                    # SQLite database (auto-created)
│
├── api_keys.json                      # API Key storage (NEW - Faz 7 Step 4, persistent)
├── requirements.txt
├── ReadMe.md
└── ...
```

## API Architecture (Faz 7 Tamamı)

### 14 API Endpoints

| Endpoint | Metod | Auth | Açıklama |
|----------|-------|------|----------|
| **/** | GET | ❌ | Root info (public) |
| **/health** | GET | ❌ | Health check (public) |
| **/pipeline/available** | GET | ❌ | Available modules (public) |
| **/clean** | POST | ✅ | Text cleaning (protected) |
| **/pipeline/run** | POST | ✅ | Pipeline execution (protected) |
| **/upload/csv** | POST | ✅ | CSV file upload (protected) |
| **/db/uploads** | GET | ✅ | Upload history (protected) |
| **/db/uploads/{id}** | GET | ✅ | Upload details (protected) |
| **/db/logs/{upload_id}** | GET | ✅ | Processing logs (protected) |
| **/queue/submit** | POST | ✅ | Submit job (protected) |
| **/queue/jobs** | GET | ✅ | List jobs (protected) |
| **/queue/jobs/{id}** | GET | ✅ | Job details (protected) |
| **/queue/jobs/{id}/cancel** | POST | ✅ | Cancel job (protected) |
| **/queue/stats** | GET | ✅ | Queue statistics (protected) |

### Pydantic Models (13 Total)

**Request Models:**
- CleanRequest
- PipelineRunRequest
- JobSubmitRequest

**Response Models:**
- ApiResponse
- FileUploadResponse
- UploadHistoryItem, UploadHistoryResponse
- ProcessingLogItem, ProcessingLogsResponse
- JobResponse, JobListResponse, QueueStatsResponse

### Singleton Patterns (4 Total)

1. **Database Singleton** (db/database.py)
   - SQLite connection pooling
   - ORM-style models (UploadRecord, ProcessingLog)
   - Repository pattern helpers
   - Auto-initialization

2. **APIKeyManager Singleton** (api_modules/security.py)
   - UUID-based key generation
   - Expiration support
   - Persistent JSON storage (api_keys.json)
   - Key validation and rotation

3. **ProcessingQueue Singleton** (api_modules/queue.py)
   - Thread-safe FIFO queue
   - 5-state job lifecycle (PENDING → PROCESSING → COMPLETED/FAILED/CANCELLED)
   - Atomic state transitions with Lock
   - Statistics tracking

4. **StructuredLogger Singleton** (api_modules/logging_service.py)
   - JSON structured logging
   - File logging (logs/api.log, DEBUG level)
   - Console logging (stdout, INFO level)
   - Request/response tracking
   - Error context capture
   - Database operation tracking
   - Job event tracking
   - Pipeline execution tracking

### Dependency Injection

- **verify_api_key()** - FastAPI dependency for protected routes
- **get_pipeline_manager()** - Pipeline manager factory
- **get_database()** - Database singleton accessor

### Middleware & Error Handling

- **Logging Middleware** - All requests/responses logged with timing
- **Global Exception Handler** - Errors logged with context
- **API Key Masking** - Security in logs (first 8 + last 4 chars)

## Database Schema (SQLite)

### Table 1: uploads
```sql
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    file_size INTEGER,
    rows INTEGER,
    columns INTEGER,
    original_shape TEXT,
    uploaded_at TEXT,
    user_agent TEXT,
    status TEXT
)
```

### Table 2: processing_logs
```sql
CREATE TABLE processing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upload_id INTEGER NOT NULL,
    module_name TEXT,
    status TEXT,
    execution_time_ms REAL,
    error_message TEXT,
    processed_at TEXT,
    FOREIGN KEY(upload_id) REFERENCES uploads(id)
)
```

### Table 3: pipeline_results
```sql
CREATE TABLE pipeline_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    upload_id INTEGER NOT NULL,
    modules_applied TEXT,
    original_shape TEXT,
    cleaned_shape TEXT,
    execution_time_ms REAL,
    result_path TEXT,
    created_at TEXT,
    FOREIGN KEY(upload_id) REFERENCES uploads(id)
)
```

## Authentication

### API Key System
- **Type:** UUID-based bearer tokens
- **Storage:** api_keys.json (persistent)
- **Expiration:** Optional (TTL support)
- **Validation:** verify_api_key() FastAPI dependency
- **Header:** X-API-Key

### Test Key
- Auto-created on first run
- Configurable in security.py

## Logging Configuration

### File Logging
- **Path:** logs/api.log
- **Level:** DEBUG
- **Format:** JSON (structured)
- **Mode:** Append

### Console Logging
- **Level:** INFO
- **Format:** JSON (structured)
- **Output:** stdout

### Log Context
- Timestamp (ISO 8601)
- Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Message
- Context (method, path, status, timing)
- Extra fields (database ops, job events, pipeline runs)

## Code Quality Standards

- **Type Hints:** Full type annotations on all functions
- **Documentation:** Docstrings on all modules/classes
- **Error Handling:** Try-catch with logging
- **Testing:** 23/23 unit tests PASS (100%)
- **Line Length:** <120 characters (PEP 8)
- **Naming:** snake_case for functions, CamelCase for classes
- **Imports:** Organized by standard → third-party → local

## Testing Framework

- **Test Runner:** pytest
- **Test Client:** FastAPI TestClient (no server startup)
- **Coverage:** All 14 endpoints tested
- **Test Count:** 23 tests
- **Pass Rate:** 100% (23/23 PASS)

### Test Classes
- TestHealth (1 test)
- TestClean (5 tests: success, operations, auth)
- TestRoot (1 test)
- TestPipeline (3 tests: available, run, auth)
- TestUpload (5 tests: success, validation, auth)
- TestDatabase (3 tests: list, detail, logs)
- TestQueue (6 tests: submit, list, detail, cancel, stats)

## Performance Considerations

- **Database:** SQLite with connection pooling
- **Queue:** In-memory FIFO (Redis alternative for scaling)
- **Logging:** JSON format suitable for log aggregation
- **API:** FastAPI async support (future enhancement)
- **Caching:** To be implemented in Faz 7 Step 7+

## Security

- **API Keys:** UUID-based, expiration support
- **Logging:** API key masking (first 8 + last 4)
- **Database:** SQLite (local only, no remote exposure)
- **Error Messages:** Generic (detailed errors only in logs)
- **CORS:** To be configured in Faz 7 Step 8+
- **Rate Limiting:** To be implemented in Faz 7 Step 8+

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
