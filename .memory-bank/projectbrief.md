# Project Brief: NeatData

## Ne Yaptığı (Scope)
NeatData, **dağınık CSV veri setlerini temizleyen ve standardize eden**, iki ana arayüze (GUI + REST API) sahip bir Python uygulamasıdır.

**İki Interface Stratejisi:**
- **Masaüstü GUI** (CustomTkinter): Teknik olmayan kullanıcılar için sürükle-bırak
- **REST API** (FastAPI + WebSocket): Otomatik sistemler için JSON-based batch processing

## Proje Mimarisi
```
Backend Core (PipelineManager)
├── Core Modules (Pandas-based, 8 plugin)
└── Custom Plugins (User-extensible)

Frontends
├── GUI (CustomTkinter, masaüstü)
└── API (FastAPI, 16 endpoints)

Supporting Systems
├── Database (SQLite, audit trail)
├── Authentication (UUID-based API keys)
├── Queue (Asynchronous job processing)
├── WebSocket (Real-time progress monitoring)
└── Logging (Structured JSON)
```

## Temel Özellikler
1. **Core Logic:** PipelineManager → dinamik plugin keşif ve sırasıyla çalıştırma
2. **Database:** SQLite 3 tablo (uploads, processing_logs, pipeline_results)
3. **Authentication:** UUID-based API keys with expiration support
4. **Batch Queue:** Thread-safe FIFO + 5-state job lifecycle
5. **Logging:** Structured JSON (file + console, security-aware)
6. **Real-time:** WebSocket (job-specific progress + broadcast channel)
7. **Testing:** 28/28 unit tests (100% coverage)

## Proje Hedefleri
- ✅ **Modülerlik:** GUI, API, Core Logic tamamen ayrılmış
- ✅ **Genişletilebilirlik:** Custom plugins otomatik keşif
- ✅ **Production-Ready:** Auth, logging, error handling, monitoring
- ✅ **User-Friendly:** Modern GUI, comprehensive API docs (Swagger)
- ⏳ **Performance:** Caching, async optimization (Faz 7 Step 9)
- ⏳ **Security:** Rate limiting, CORS (Faz 7 Step 10)

## Proje Durumu
**Faz 7 Step 7 TAMAMLANDI (25.11.2025)**
- 16 API Endpoints (14 REST + 2 WebSocket)
- 4 Singleton Instances
- 100% Test Coverage (28/28 PASS)
- Production-Ready API
