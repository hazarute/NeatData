# Tech Context

## Teknoloji Stack

**Core:**
- Python 3.13 | Pandas 2.2.0 | Pydantic 2.12.4

**Web:**
- FastAPI 0.121.3 (REST + WebSocket, native)
- Uvicorn (ASGI server)
- APIRouter (Blueprint pattern, 8 routers)

**GUI:**
- CustomTkinter (Modern, dark theme, rounded corners)

**Database:**
- SQLite3 (auto-initialize, 3 tables, persistent)
- JSON storage (api_keys.json for API credentials)

**Concurrency:**
- threading.Lock (thread-safe singletons)
- asyncio (FastAPI WebSocket native)

**Logging:**
- Structured JSON format
- File output: logs/api.log (DEBUG level)
- Console output: stdout (INFO level and above)

**Testing:**
- pytest
- TestClient (no server startup)
- 28/28 PASS (100% coverage)

**Deployment:**
- Git version control
- Local development mode (uvicorn reload)

## Installation & Setup

```bash
# Python environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn api:app --reload --host 127.0.0.1 --port 8000

# Run GUI
python neatdata_gui.py

# Run tests
pytest tests/test_api_unit.py --tb=short -v
```

## API Endpoints (16 Total)

### Public Endpoints (3)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info + endpoint list |
| `/health` | GET | Health check |
| `/pipeline/available` | GET | List available core modules |

### Protected Endpoints - REST (11)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/clean` | POST | Text cleaning (simple operation) |
| `/pipeline/run` | POST | Pipeline execution (multiple modules) |
| `/upload/csv` | POST | CSV file upload (multipart) |
| `/db/uploads` | GET | Upload history |
| `/db/uploads/{id}` | GET | Upload details |
| `/db/logs/{upload_id}` | GET | Processing logs for upload |
| `/queue/submit` | POST | Submit job to queue |
| `/queue/jobs` | GET | List all jobs |
| `/queue/jobs/{id}` | GET | Job details + status |
| `/queue/jobs/{id}/cancel` | POST | Cancel pending/processing job |
| `/queue/stats` | GET | Queue statistics |

### Protected Endpoints - WebSocket (2)
| Endpoint | Type | Purpose |
|----------|------|---------|
| `/ws/{job_id}` | WebSocket | Job-specific progress stream |
| `/ws` | WebSocket | Broadcast channel (all updates) |

## Singletons (4 Total)

### 1. Database Singleton
- **Location:** `db/database.py`
- **Purpose:** SQLite connection pooling + ORM
- **Tables:** uploads, processing_logs, pipeline_results
- **Features:** Auto-init, foreign keys, persistent
- **Methods:** save(), get(), get_all(), delete()

### 2. APIKeyManager Singleton
- **Location:** `api_modules/security.py`
- **Purpose:** API key generation & validation
- **Storage:** api_keys.json (persistent JSON)
- **Features:** UUID-based, expiration support, masking in logs
- **Methods:** generate(), validate(), list_keys(), revoke()

### 3. ProcessingQueue Singleton
- **Location:** `api_modules/queue.py`
- **Purpose:** Asynchronous job queue (FIFO)
- **Storage:** In-memory (thread-safe with Lock)
- **States:** PENDING → PROCESSING → COMPLETED/FAILED/CANCELLED
- **Features:** Atomic transitions, statistics, progress tracking
- **Methods:** submit(), start(), complete(), fail(), cancel(), get(), update_job_progress()

### 4. WebSocketManager Singleton
- **Location:** `api_modules/websocket_manager.py`
- **Purpose:** Connection pool + message broadcasting
- **Storage:** In-memory (thread-safe with Lock)
- **Pattern:** Pub/Sub (job-specific + broadcast)
- **Features:** Connect/disconnect, subscribe/unsubscribe, broadcast
- **Methods:** connect(), disconnect(), subscribe(), unsubscribe(), broadcast(), broadcast_to_all()

## Pydantic Models (13 Total)

**Request Models:**
- CleanRequest (data, operations)
- PipelineRunRequest (data, modules)
- JobSubmitRequest (upload_id, modules)

**Response Models:**
- ApiResponse (status, data, timestamp)
- FileUploadResponse (status, filename, rows, columns, upload_id)
- UploadHistoryItem + UploadHistoryResponse
- ProcessingLogItem + ProcessingLogsResponse
- JobResponse + JobListResponse
- QueueStatsResponse

**WebSocket Models:**
- ProgressUpdate (job_id, status, progress_percent, current_step, step_message, timestamp, error_details)

## Authentication & Security
- **Method:** UUID-based API Key (header: `X-API-Key`)
- **Storage:** Persistent JSON (api_keys.json)
- **Features:** Expiration support (365 days), key masking in logs
- **Scope:** All protected endpoints + WebSocket endpoints require API key

## Logging Configuration
- **Format:** Structured JSON (timestamp, level, message, context, extra)
- **File:** logs/api.log (created auto, DEBUG level, append)
- **Console:** stdout (INFO level and above)
- **Features:**
  - Request/response tracking with timing
  - Error context capture (stack trace, user context)
  - Database operation logging
  - Job event tracking
  - Pipeline execution tracking
  - Security-aware (API key masking)

## Database Schema
```sql
CREATE TABLE uploads (
  id INTEGER PRIMARY KEY,
  filename TEXT,
  rows INTEGER,
  columns INTEGER,
  file_size INTEGER,
  uploaded_at TEXT
);

CREATE TABLE processing_logs (
  id INTEGER PRIMARY KEY,
  upload_id INTEGER FOREIGN KEY,
  operation TEXT,
  status TEXT,
  timestamp TEXT,
  details TEXT
);

CREATE TABLE pipeline_results (
  id INTEGER PRIMARY KEY,
  upload_id INTEGER FOREIGN KEY,
  pipeline_name TEXT,
  modules_executed TEXT,
  success BOOLEAN,
  timestamp TEXT
);
```

## WebSocket Protocol

**Job-Specific Stream** (`/ws/{job_id}`):
```json
{
  "job_id": "uuid",
  "status": "pending|processing|completed|failed|error",
  "progress_percent": 50,
  "current_step": "processing",
  "message": "Processing step 2 of 5",
  "timestamp": "2025-11-25T14:30:00Z"
}
```

**Client Commands:**
- `{"command": "unsubscribe"}` - Stop receiving updates
- `{"command": "ping"}` - Keepalive (for broadcast channel)

## Performance Notes
- **API Response:** < 200ms (queue jobs < 5s)
- **WebSocket Update Frequency:** Every 100ms (configurable)
- **Database:** SQLite with connection pooling (sufficient for single-server)
- **Queue:** In-memory FIFO (thread-safe, atomic)
- **Concurrency:** Lock-based synchronization (suitable for < 100 concurrent users)

**Future Optimizations (Faz 7 Step 9):**
- Redis for queue scaling
- Caching layer (functools.lru_cache or Redis)
- Async processing for long-running modules
- Connection pooling optimization

## Git Commits (Recent)
- `227fe7b` - Faz 7 Adim 7: WebSocket Real-Time Progress TAMAMLANDI
- `da50d76` - Housekeeping: Test dosyalarını tests/ klasörüne taşı

## Test Status
**28/28 PASS (100% coverage)**
- TestHealth (1)
- TestClean (5)
- TestRoot (1)
- TestPipeline (3)
- TestUpload (5)
- TestDatabase (3)
- TestQueue (6)
- TestWebSocket (5) ← NEW

**Run Tests:**
```bash
pytest tests/test_api_unit.py -v --tb=short
```
