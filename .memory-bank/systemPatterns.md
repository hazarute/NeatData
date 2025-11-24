# Sistem Desenleri ve Mimarı

## Katmanlı Mimari (Layered Architecture)
```
┌─────────────────────────────────────────┐
│ Interface Layer (GUI + API)             │
│ neatdata_gui.py (CustomTkinter)         │
│ api.py + api_modules/routes/*.py (8)    │
├─────────────────────────────────────────┤
│ Orchestration Layer (Singletons)        │
│ Database | APIKeyManager                │
│ ProcessingQueue | WebSocketManager      │
│ StructuredLogger                        │
├─────────────────────────────────────────┤
│ Core Business Logic                     │
│ PipelineManager (dynamic plugin loader) │
├─────────────────────────────────────────┤
│ Plugin Layer (Core + Custom)            │
│ modules/core/* + modules/custom/*       │
├─────────────────────────────────────────┤
│ Data Layer                              │
│ SQLite Database + JSON storage          │
└─────────────────────────────────────────┘
```

## Folder Yapısı
```
NeatData/
├── neatdata_gui.py           # GUI entry point
├── api.py                    # API entry point + middleware
├── api_modules/              # API layer (Blueprint pattern)
│   ├── models.py             # 13 Pydantic schemas
│   ├── security.py           # APIKeyManager singleton
│   ├── queue.py              # ProcessingQueue singleton
│   ├── websocket_manager.py  # WebSocketManager singleton
│   ├── logging_service.py    # StructuredLogger singleton
│   ├── routes/               # 8 APIRouters (REST + WebSocket)
│   │   ├── health.py, clean.py, pipeline.py, info.py
│   │   ├── upload.py, database.py, queue.py, websocket.py
│   └── utils/                # Helpers, validators
├── db/
│   └── database.py           # Database singleton
├── modules/
│   ├── pipeline_manager.py
│   ├── core/                 # Built-in plugins (8)
│   ├── custom/               # User plugins
│   └── utils/                # GUI utilities
├── tests/                    # Unit tests (28/28 PASS)
│   ├── test_api_unit.py
│   ├── test_api.py
│   └── other test files
└── .memory-bank/             # AI assistant memory (this dir)
```

## Tasarım Desenleri

### 1. **Blueprint Pattern** (API modularization)
FastAPI `APIRouter` with separate route files:
- Each endpoint in its own file (~100-200 lines)
- Single responsibility principle
- Centralized registration in api.py

### 2. **Singleton Pattern**
4 critical singletons (instance per process):
- **Database:** SQLite connection + ORM models
- **APIKeyManager:** UUID-based key storage (api_keys.json)
- **ProcessingQueue:** Thread-safe FIFO job queue (in-memory)
- **WebSocketManager:** Connection pool + pub/sub (in-memory)

### 3. **Dependency Injection** (FastAPI style)
```python
@router.post("/queue/submit")
async def submit(queue: ProcessingQueue = Depends(get_queue)):
    ...
```

### 4. **Plugin/Eklenti Deseni**
Dynamic module discovery. Each plugin implements:
```python
META = {"key": "trim_spaces", "name": "Trim Spaces", ...}
def process(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    return df  # cleaned
```

### 5. **Pub/Sub Pattern** (WebSocket)
WebSocketManager manages subscriptions:
- Job-specific: Client → get updates for specific job only
- Broadcast: Client → get updates for all jobs

### 6. **Middleware Pattern**
API middleware for:
- Request/response logging with timing
- Global exception handling with context

## Protokoller

### API Response Format
```json
{
  "status": "success|error",
  "data": {...},
  "timestamp": "2025-11-25T14:30:00Z"
}
```

### WebSocket Message Format
```json
{
  "job_id": "uuid",
  "status": "pending|processing|completed|failed|error",
  "progress_percent": 0-100,
  "current_step": "step_name",
  "message": "human-readable message",
  "timestamp": "ISO8601"
}
```

## Kod Standartları
- **Type Hints:** Mandatory for all functions
- **Docstrings:** Module, class, method level
- **Error Handling:** Try-except + logging with context
- **Testing:** pytest + TestClient (no server startup)
- **Logging:** Structured JSON for observability
- **Security:** API key masking in logs, stateless auth
