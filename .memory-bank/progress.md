# Progress / Görev Panosu

## Faz 1-7: Temel Altyapı (TAMAMLANDI ✅)
- [x] Core Pipeline Logic
- [x] Desktop GUI
- [x] FastAPI Temel Kurulum
- [x] Database & Auth
- [x] Logging & Tests (%100 Coverage)

## Faz 8: Database-Driven Streamlit Entegrasyonu (AKTİF 🚧)
**Amaç:** Streamlit arayüzünün, API ile "Upload ID" üzerinden konuşmasını sağlamak ve büyük dosyaları JSON payload yerine disk üzerinden işlemek.

### Adım 1: Veritabanı Şeması ve Modellerin Güncellenmesi
*Bu adım, dosyaların diskteki konumunu takip etmek için gereklidir.*
- [x] **Database Schema Update (`db/database.py`):**
    - `uploads` tablosuna `file_path` (TEXT) sütununu ekle.
    - `init_db` fonksiyonunu güncelle.
- [x] **Model Update (`db/database.py` - `UploadRecord`):**
    - `__init__` metoduna `file_path` parametresini ekle.
    - `save` metodundaki `INSERT` sorgusunu `file_path` içerecek şekilde güncelle.
    - `to_dict` metoduna `file_path` ekle.

### Adım 2: Upload Endpoint'inin Dosya Kaydetmesi
*Bu adım, yüklenen dosyanın sadece metadata değil, fiziksel olarak da saklanmasını sağlar.*
 - [x] **Storage Utility (`api_modules/utils/storage.py` - YENİ):**
     - `save_upload_file(file: UploadFile) -> str` fonksiyonu yazıldı.
     - Dosyaları `uploads/` klasörüne benzersiz isimle (UUID) kaydeder.
 - [x] **Upload Endpoint Refactor (`api_modules/routes/v1/upload.py`):**
     - Dosyayı `storage.py` ile diske kaydeder ve `file_path` veritabanına kaydedildi.

### Adım 3: Pipeline Endpoint'inin Refactoring'i (Kritik)
*Bu adım, API'nin JSON veri yerine ID ile çalışmasını sağlar.*
- [x] **Request Model Update (`api_modules/models.py`):**
    - `PipelineRunRequest` modelini değiştir veya yeni `PipelineRunByIdRequest` oluştur.
    - Alanlar: `upload_id: int`, `modules: List[str]`.
- [x] **Pipeline Logic Refactor (`api_modules/routes/v1/pipeline.py`):**
    - `/run` endpoint'ini güncelle:
        1. `upload_id` ile veritabanından kaydı çek (`get_upload_by_id`).
        2. Kayıttaki `file_path` üzerinden dosyayı `pandas` ile oku.
        3. `PipelineManager`'ı çalıştır.
        4. Sonucu (DataFrame) JSON olarak dön (veya geçici dosyaya yazıp link dön).

### Adım 4: Frontend (Streamlit) Altyapısı
- [x] **API Client (`frontend/api_client.py`):**
    - `upload_file(file)` -> Döner: `upload_id`
    - `run_pipeline(upload_id, modules)` -> Döner: `json_result`
    - `get_modules()` -> Döner: `list`
- [x] **Streamlit App (`streamlit_app.py`):**
    - **Sidebar:** API Bağlantı Durumu (Health Check).
    - **Ana Ekran:**
        1. Dosya Yükleme Alanı (`st.file_uploader`).
        2. Modül Seçimi (API'den gelen listeye göre checkboxlar).
        3. "Başlat" butonu (ID ile API çağrısı).
        4. Sonuç Tablosu (`st.dataframe`) ve İndirme Butonu.

### Adım 5: Temizlik ve Test
- [x] `api_modules/routes/v1/clean.py` dosyasını sil (Artık gereksiz).
- [x] Eski testleri (`tests/test_api_unit.py`) yeni `upload_id` mantığına göre güncelle.
- [x] Manuel Test: Streamlit üzerinden 10MB+ bir dosya yükleyip işle.

## Bilinen Sorunlar / Notlar
- Swagger UI son kullanıcı için uygun değil, Streamlit bu boşluğu dolduracak.
- `api_modules\routes\v1\clean.py` şimdilik atıl durumda, odak `api_modules\routes\v1\pipeline.py` üzerinde.