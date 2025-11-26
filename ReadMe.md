# NeatData - CSV Data Cleaner & API 🧹

[![Python Version](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.3-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

A powerful, modular Python application to clean and standardize messy CSV files. 

**Now featuring a Triple Interface Strategy:**
1.  **Desktop GUI:** A modern, drag-and-drop interface for non-technical users.
2.  **Web Interface:** A database-driven Streamlit app for easy access and visualization.
3.  **REST API:** A robust FastAPI-based backend with WebSocket support for automated, batch processing systems.

Türkçe açıklama için [aşağıya inin](#-neatdata---csv-veri-temizleyici--api-).

---

## 🌟 About The Project

NeatData has evolved into a comprehensive data cleaning solution. It provides a robust, extensible, and fully modular architecture that serves a desktop application, a web interface, and a high-performance REST API.

### Key Features
*   **Triple Interface:** Choose between CustomTkinter GUI, Streamlit Web App, or full-featured REST API.
*   **Modular Architecture:** Core cleaning logic is decoupled from interfaces, allowing consistent behavior across all platforms.
*   **Dynamic Pipeline:** Configure cleaning steps (modules) dynamically.
*   **Database-Driven Workflow:**
    *   **Upload & ID System:** Files are uploaded once, stored securely, and referenced by ID.
    *   **Audit Trail:** SQLite-based tracking of all uploads and operations.
*   **Advanced API:**
    *   **FastAPI & WebSockets:** Real-time progress monitoring.
    *   **Asynchronous Queue:** Thread-safe job processing for heavy workloads.
    *   **Authentication:** UUID-based API key security.
*   **Shared Infrastructure:** Unified `UIState`, `PipelineRunner`, and `GuiLogger` ensure consistency.
*   **Automatic Detection:** Smart detection of CSV delimiters and encoding.

### Built With
*   [Python 3.13](https://www.python.org/)
*   [FastAPI](https://fastapi.tiangolo.com/) (REST + WebSocket)
*   [Streamlit](https://streamlit.io/) (Web Interface)
*   [Pandas](https://pandas.pydata.org/) (Data Processing)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (Desktop GUI)
*   [SQLite](https://www.sqlite.org/index.html) (Database)

## 🚀 Features

*   **Modular Cleaning Pipeline:** Steps like `standardize_headers`, `drop_duplicates`, `handle_missing`, `convert_types`, and `text_normalize` are separate, configurable modules.
*   **Real-time Monitoring:** Watch cleaning progress via GUI progress bars or API WebSockets.
*   **Job Queue System:** Submit multiple files to the API; they are processed asynchronously in a FIFO queue.
*   **Comprehensive Logging:** Structured JSON logging for all operations.
*   **Extensible:** Easily add custom plugins in `modules/custom/`.

## 📦 Installation

### Prerequisites
*   Python 3.8+ (Python 3.13 recommended)
*   pip

### Steps
1.  Clone the repository:
    ```bash
    git clone https://github.com/hazarute/NeatData.git
    cd NeatData
    ```

2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

### 1. Web Mode (Streamlit)
Launch the web interface (requires API running):
```bash
# Terminal 1: Start API
uvicorn api:app --reload

# Terminal 2: Start Streamlit
streamlit run streamlit_app.py
```
*   **Features:** Modern dashboard, secure login, file upload history, visual configuration.

### 2. GUI Mode (Desktop)
Launch the standalone desktop interface:
```bash
python neatdata_gui.py
```
*   **Features:** Drag-and-drop files, toggle modules, real-time logs, export to Excel/CSV.

### 3. API Mode (Server)
Start the FastAPI server:
```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```
*   **Documentation:** Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
*   **Authentication:** Manage keys via `api_keys.json` or the `APIKeyManager`.

### 4. CLI Mode (Command Line)
Run the pipeline directly from the terminal:
```bash
python -m modules.cli_handler --input data.csv --output-dir ./cleaned
```

## 🏗️ Architecture

The project follows a **Layered Architecture**:

```
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
```

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Info & Routes |
| `GET` | `/health` | System Health Check |
| `POST` | `/clean` | Simple Text Cleaning |
| `POST` | `/pipeline/run` | Run Full Pipeline (Sync) |
| `POST` | `/upload/csv` | Upload CSV File |
| `POST` | `/queue/submit` | Submit Job to Async Queue |
| `GET` | `/queue/jobs/{id}` | Check Job Status |
| `WS` | `/ws/{job_id}` | Real-time Job Progress |

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Hazar Ute - hazarute@gmail.com
Project Link: [https://github.com/hazarute/NeatData](https://github.com/hazarute/NeatData)

---

# 🧹 NeatData - CSV Veri Temizleyici & API 🧹

[![Python Version](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Durum](https://img.shields.io/badge/durum-aktif-başarılı.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.3-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

Dağınık CSV dosyalarını temizlemek ve standartlaştırmak için geliştirilmiş güçlü, modüler bir Python uygulaması.

**Artık Üçlü Arayüz Stratejisi ile:**
1.  **Masaüstü GUI:** Teknik olmayan kullanıcılar için modern, sürükle-bırak arayüzü.
2.  **Web Arayüzü:** Kolay erişim ve görselleştirme için veritabanı destekli Streamlit uygulaması.
3.  **REST API:** Otomasyon ve toplu işlemler için FastAPI tabanlı, WebSocket destekli güçlü bir backend.

---

## 🌟 Proje Hakkında

NeatData, basit bir script olmaktan çıkıp kapsamlı bir veri temizleme çözümüne dönüştü. Masaüstü uygulaması, web arayüzü ve yüksek performanslı bir REST API sunan modüler bir mimariye sahiptir.

### Temel Özellikler
*   **Üçlü Arayüz:** CustomTkinter GUI, Streamlit Web Uygulaması veya tam özellikli REST API arasında seçim yapın.
*   **Modüler Mimari:** Temel temizleme mantığı arayüzlerden ayrılmıştır; tüm platformlarda tutarlı çalışır.
*   **Dinamik Pipeline:** Temizlik adımlarını (modülleri) dinamik olarak yapılandırın.
*   **Veritabanı Odaklı İş Akışı:**
    *   **Yükleme & ID Sistemi:** Dosyalar bir kez yüklenir, güvenli bir şekilde saklanır ve ID ile referans verilir.
    *   **Denetim İzi:** Tüm yüklemelerin ve işlemlerin SQLite tabanlı takibi.
*   **Gelişmiş API:**
    *   **FastAPI & WebSocket:** Gerçek zamanlı ilerleme takibi.
    *   **Asenkron Kuyruk:** Yoğun iş yükleri için thread-safe iş kuyruğu.
    *   **Kimlik Doğrulama:** UUID tabanlı API anahtarı güvenliği.
*   **Ortak Altyapı:** Birleştirilmiş `UIState`, `PipelineRunner` ve `GuiLogger`.
*   **Otomatik Algılama:** CSV ayraçlarını ve kodlamasını (encoding) akıllıca algılar.

### Kullanılan Teknolojiler
*   [Python 3.13](https://www.python.org/)
*   [FastAPI](https://fastapi.tiangolo.com/) (REST + WebSocket)
*   [Streamlit](https://streamlit.io/) (Web Arayüzü)
*   [Pandas](https://pandas.pydata.org/) (Veri İşleme)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (GUI)
*   [SQLite](https://www.sqlite.org/index.html) (Veritabanı)

## 🚀 Özellikler

*   **Modüler Temizlik Hattı:** `standardize_headers`, `drop_duplicates`, `handle_missing` gibi adımlar ayrı modüllerdir.
*   **Gerçek Zamanlı İzleme:** GUI ilerleme çubukları veya API WebSocket üzerinden temizlik sürecini izleyin.
*   **İş Kuyruk Sistemi:** API'ye birden fazla dosya gönderin; FIFO kuyruğunda asenkron olarak işlensin.
*   **Kapsamlı Loglama:** Tüm işlemler için yapılandırılmış JSON logları.
*   **Genişletilebilir:** `modules/custom/` altına kendi eklentilerinizi kolayca ekleyin.

## 📦 Kurulum

### Gereksinimler
*   Python 3.8+ (Python 3.13 önerilir)
*   pip

### Adımlar
1.  Depoyu klonlayın:
    ```bash
    git clone https://github.com/hazarute/NeatData.git
    cd NeatData
    ```

2.  Sanal ortam oluşturun (önerilir):
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  Bağımlılıkları yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Kullanım

### 1. Web Modu (Streamlit)
Web arayüzünü başlatın (API'nin çalışıyor olması gerekir):
```bash
# Terminal 1: API'yi Başlat
uvicorn api:app --reload

# Terminal 2: Streamlit'i Başlat
streamlit run streamlit_app.py
```
*   **Özellikler:** Modern dashboard, güvenli giriş, dosya yükleme geçmişi, görsel konfigürasyon.

### 2. GUI Modu (Masaüstü)
Modern koyu temalı arayüzü başlatın:
```bash
python neatdata_gui.py
```
*   **Özellikler:** Sürükle-bırak dosya yükleme, modül seçimi, canlı loglar, Excel/CSV çıktısı.

### 3. API Modu (Sunucu)
FastAPI sunucusunu başlatın:
```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```
*   **Dokümantasyon:** İnteraktif Swagger UI için `http://127.0.0.1:8000/docs` adresine gidin.
*   **Kimlik Doğrulama:** `api_keys.json` veya `APIKeyManager` üzerinden anahtarları yönetin.

### 4. CLI Modu (Komut Satırı)
Pipeline'ı doğrudan terminalden çalıştırın:
```bash
python -m modules.cli_handler --input veri.csv --output-dir ./temizlenenler
```

## 🏗️ Mimari

Proje **Katmanlı Mimari (Layered Architecture)** izler:

```
┌───────────────────────────────────────────────────────────┐
│ Arayüz Katmanı (Çoklu Frontend Stratejisi)                │
│ 1. Desktop: neatdata_gui.py (Doğrudan Çekirdek Erişim)    │
│ 2. Web: streamlit_app.py (HTTP/Requests ile)              │
│ 3. API: api.py + api_modules/routes/*.py (Gateway)        │
├───────────────────────────────────────────────────────────┤
│ Orkestrasyon Katmanı (Singleton'lar)                      │
│ Database (SQLite) | APIKeyManager (Auth)                  │
│ ProcessingQueue (Async) | WebSocketManager (Real-time)    │
├───────────────────────────────────────────────────────────┤
│ Çekirdek İş Mantığı                                       │
│ PipelineManager (Dinamik Plugin Yükleme & Çalıştırma)     │
├───────────────────────────────────────────────────────────┤
│ Eklenti Katmanı (Modüler İşleme)                          │
│ modules/core/* (Dahili) + modules/custom/* (Kullanıcı)    │
├───────────────────────────────────────────────────────────┤
│ Veri Katmanı (Kalıcılık)                                  │
│ SQLite (Metadata/Loglar) + Dosya Sistemi (CSV Depolama)   │
└───────────────────────────────────────────────────────────┘
```

## 📡 API Endpoint Özeti

| Metot | Endpoint | Açıklama |
| :--- | :--- | :--- |
| `GET` | `/` | API Bilgisi & Rotalar |
| `GET` | `/health` | Sistem Sağlık Kontrolü |
| `POST` | `/clean` | Basit Metin Temizleme |
| `POST` | `/pipeline/run` | Tam Pipeline Çalıştırma (Senkron) |
| `POST` | `/upload/csv` | CSV Dosyası Yükleme |
| `POST` | `/queue/submit` | Asenkron Kuyruğa İş Gönderme |
| `GET` | `/queue/jobs/{id}` | İş Durumu Sorgulama |
| `WS` | `/ws/{job_id}` | Gerçek Zamanlı İlerleme (WebSocket) |

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen depoyu fork'layın ve bir Pull Request gönderin.

## 📝 Lisans

MIT Lisansı altında dağıtılmaktadır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## 📞 İletişim

Hazar Ute - hazarute@gmail.com
Proje Linki: [https://github.com/hazarute/NeatData](https://github.com/hazarute/NeatData)
