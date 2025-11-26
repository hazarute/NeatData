# Tech Context

## Teknoloji Stack
**Frontend:**
- **Streamlit:** Web arayüzü ve etkileşim.
- **CustomTkinter:** Masaüstü arayüzü.

**Backend:**
- **Python 3.13:** Çekirdek dil.
- **FastAPI:** REST API framework.
- **Pandas:** Veri manipülasyonu.
- **SQLite:** Veritabanı.

**İletişim:**
- **Requests:** Streamlit'in API ile konuşması için HTTP istemcisi.
- **Multipart/Form-Data:** Dosya yükleme protokolü.

## Kritik API Endpointleri (Faz 8 Odaklı)

| Method | Endpoint | Açıklama | Durum |
|--------|----------|----------|-------|
| POST | `/v1/upload/csv` | Dosyayı yükler ve DB'ye kaydeder. | ✅ Hazır |
| POST | `/v1/pipeline/run` | `upload_id` alır, DB'den okur, işler. | ✅ Revize Edildi |
| POST | `/v1/upload/csv` (dosya saklama) | Dosyayı diske kaydeder (`uploads/`), metadata olarak DB'ye `file_path` ekler. | ✅ Uygulandı |
| GET | `/v1/pipeline/available` | Modülleri listeler. | ✅ Hazır |

## Geliştirme Ortamı
- `uvicorn api:app --reload` (Backend'i başlatır)
- `streamlit run streamlit_app.py` (Frontend'i başlatır)

## Notlar - Bellek Senkronizasyonu
- `api_modules/utils/storage.py` eklendi; büyük dosyalar stream edilerek `uploads/` altına UUID ile kaydediliyor.
- `/v1/upload/csv` endpoint'i artık fiziksel dosya saklıyor ve `upload_id` ile `file_path` döndürüyor.
- `/v1/pipeline/run` endpoint'i JSON payload yerine `upload_id` alacak şekilde revize edildi ve dosya DB'deki `file_path` üzerinden pandas ile okunuyor.