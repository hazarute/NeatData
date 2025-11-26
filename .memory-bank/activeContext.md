# Active Context (Zihinsel Durum)

## Mevcut Odak
**Faz 8: Database-Driven Streamlit UI Geliştirme**
**Durum:** Başlangıç Aşamasında

## Stratejik Değişiklik (Pivot)
Backend optimizasyonları (Caching, Async v2) durduruldu. Odak noktası, ürünü görselleştirmek ve satılabilir hale getirmek için **Streamlit** arayüzünü geliştirmek.

**Mimari Karar (Database-First):**
Streamlit dosyayı doğrudan işlemeyecek.
1.  Dosyayı API'ye yükleyecek (`/upload`).
2.  API, dosyayı veritabanına kaydedip bir `upload_id` dönecek.
3.  Streamlit, bu `upload_id` ile işlem başlatacak (`/pipeline/run`).

## Sıradaki Görevler
1. **Database Schema Update (tamamlandı):** `db/database.py`'ye `file_path` sütunu eklendi ve `UploadRecord` modeli güncellendi.
2. **Storage Utility (tamamlandı):** `api_modules/utils/storage.py` oluşturuldu; `save_upload_file(file: UploadFile) -> str` fonksiyonu dosyaları `uploads/` altında UUID ile kaydeder.
3. **Upload Endpoint Refactor (tamamlandı):** `api_modules/routes/v1/upload.py` dosya diske kaydediliyor, `file_path` veritabanına kaydedildi.
4. **Pipeline Endpoint Refactor (tamamlandı):** `/v1/pipeline/run` endpoint'i `upload_id` alacak şekilde güncellendi.
5. **Frontend Setup (tamamlandı):** `frontend/api_client.py` ve `streamlit_app.py` tamamlandı.
6. **Temizlik ve Test (tamamlandı):** Eski endpoint'ler temizlendi, testler güncellendi ve geçti.
7. **Manuel Test (tamamlandı):** Streamlit API Key entegrasyonu yapıldı ve test edildi.

## Aktif Dosyalar
- `streamlit_app.py` (Tamamlandı)