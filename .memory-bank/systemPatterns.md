# Sistem Desenleri ve Mimari

## Katmanlı Mimari (Layered Architecture)
graph TD
    subgraph Interfaces
        A[Desktop GUI]
        B[Streamlit Web App]
        C[REST API Interface]
    end

    subgraph Orchestration
        D[APIKeyManager]
        E[ProcessingQueue]
        F[WebSocketManager]
    end

    subgraph CoreLogic
        G[PipelineManager]
    end

    subgraph DataLayer
        H[SQLite Database]
        I[File System]
    end

    A -- Direct Call --> G
    B -- HTTP Requests --> C
    C -- Controls --> D & E & F
    C -- Uses --> G
    G -- Reads/Writes --> H & I

┌───────────────────────────────────────────────────────────┐
│ Interface Layer (Multi-Frontend Strategy)                 │
│ 1. Desktop: neatdata_gui.py (Direct Core Access)          │
│ 2. Web: streamlit_app.py (Via HTTP/Requests)              │
│ 3. API: api.py + api_modules/routes/*.py (Gateway)        │
├───────────────────────────────────────────────────────────┤
│ Orchestration Layer (Singletons)                          │
│ Database (SQLite) | APIKeyManager (Auth)                  │
│ ProcessingQueue (Async) | WebSocketManager (Real-time)    │
├───────────────────────────────────────────────────────────┤
│ Core Business Logic                                       │
│ PipelineManager (Dynamic Plugin Loader & Execution)       │
├───────────────────────────────────────────────────────────┤
│ Plugin Layer (Modular Processing)                         │
│ modules/core/* (Built-in) + modules/custom/* (User)       │
├───────────────────────────────────────────────────────────┤
│ Data Layer (Persistence)                                  │
│ SQLite (Metadata/Logs) + File System (CSV/Excel Storage)  │
└───────────────────────────────────────────────────────────┘

## Folder Yapısı
```
NeatData/
├── neatdata_gui.py           # GUI entry point
├── api.py                    # API entry point + middleware
├── streamlit_app.py          # Frontend Entry Point
├── frontend/                 # Streamlit Yardımcıları
│   ├── api_client.py         # API İstek Yöneticisi
│   └── components.py         # UI Parçaları
├── api_modules/              # API layer (Blueprint pattern)
│   ├── models.py             # 13 Pydantic schemas
│   ├── security.py           # APIKeyManager singleton
│   ├── queue.py              # ProcessingQueue singleton
│   ├── websocket_manager.py  # WebSocketManager singleton
│   ├── logging_service.py    # StructuredLogger singleton
│   ├── routes/               # 8 APIRouters (REST + WebSocket)  
│   │   ├── v1/
│   │   │   ├── health.py, clean.py, pipeline.py, info.py
│   │   │   ├── upload.py, database.py, queue.py, websocket.py
│   │   ├── v2/
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

## Veri Akış Senaryoları

### 1\. Web Akışı (Database-First Approach) - **(FAZ 8 ODAĞI)**

Bu akış, frontend ve backend'in tamamen ayrık (decoupled) çalışmasını sağlar.

1.  **Upload (Yükleme):**

      * Kullanıcı Streamlit'e dosyayı sürükler.
      * `Streamlit` -\> POST `/upload/csv` -\> `API`.
      * `API`, dosyayı diske kaydeder ve `SQLite`a metadata (satır sayısı, boyut) yazar.
      * `API`, benzersiz bir **`upload_id`** döner.
      * `API` ayrıca dosyayı sunucunun `uploads/` dizinine UUID ile kaydeder ve `uploads` tablosunda `file_path` alanına fiziksel yolu yazar.

2.  **Process (İşleme):**

      * Kullanıcı Streamlit'te modülleri seçer ve "Başlat"a basar.
      * `Streamlit` -\> POST `/pipeline/run` (Payload: `upload_id` + `modules`).
      * `API`, `upload_id` ile veritabanından dosya yolunu bulur.
      * `PipelineManager` dosyayı işler.
      * Sonuç JSON/File olarak `Streamlit`e döner ve kullanıcıya gösterilir.

### 2\. Desktop Akışı (Direct Access)

1.  **Direct:** `neatdata_gui.py`, `PipelineManager` sınıfını doğrudan import eder ve çalıştırır. API katmanını atlar.

## Tasarım Desenleri

  - **Repository Pattern:** Veritabanı erişimi `db/` modülü altında soyutlanmıştır. SQL sorguları iş mantığının içine karışmaz.
  - **Facade Pattern:** `PipelineManager`, karmaşık plugin yükleme ve çalıştırma süreçlerini tek bir `run()` metodu arkasında gizler.
  - **Singleton Pattern:** `Database`, `APIKeyManager`, `ProcessingQueue` ve `WebSocketManager` uygulama boyunca tekil instance olarak yaşar.
- **File Storage:** Yüklenen büyük dosyalar `uploads/` dizininde saklanır; `db/uploads` tablosunda `file_path` ile ilişkilendirilir. Dosya isimleri UUID ile çakışma olmaması için değiştirilir.
  - **Strategy Pattern:** Her temizlik modülü (Core/Custom), ortak bir arayüzü (`process` fonksiyonu) uygulayan değiştirilebilir bir stratejidir.

## Kod Standartları

  - **Type Hints:** Tüm fonksiyonlarda zorunlu.
  - **Docstrings:** Modül, sınıf ve fonksiyon seviyesinde açıklama.
  - **Error Handling:** Try-except blokları ve bağlamsal loglama.
  - **Testing:** `pytest` ile birim testleri (Server başlatmadan `TestClient` kullanımı).
  - **Logging:** Yapılandırılmış JSON loglama (Security-aware).

