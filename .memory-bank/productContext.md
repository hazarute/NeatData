# Ürün Bağlamı (Product Context)

## Neden Var? (Problem Çözdüğü)
Kullanıcılar ve otomatik sistemler CSV verilerinde yaygın sorunlarla karşılaşır:
- Duplikat satırlar (veri bütünlüğü kaybı)
- Eksik/boş değerler (NaN, analiz zorlukları)
- Tutarsız ayraç ve encoding
- Tutarsız format (boşluk, büyük/küçük harf)

**NeatData çözümü:** Hızlı, güvenilir ve otomasyona uygun veri temizleme

## Hedef Kullanıcılar
1. **İnsan Kullanıcılar:** Teknik olmayan kişiler
   - Modern, koyu temalı GUI arayüzü
   - Sürükle-bırak dosya seçimi
   - Basit checkbox/switch seçenekleri

2. **Yazılım Sistemleri:** Otomatik veri işleme
   - REST API with JSON input/output
   - Asynchronous batch queue
   - Real-time progress monitoring (WebSocket)
   - Production-ready (auth, logging, error handling)

## Kullanıcı Deneyimi Hedefleri

### GUI Path
1. Dosya seç (sürükle-bırak)
2. Core modülleri seç (checkbox/switch)
3. Custom plugins seç (dinamik list)
4. Çalıştır ve ilerleme izle (progress bar)
5. Çıktıyı indir (CSV/Excel)
6. Logs görüntüle

### API Path
1. CSV dosyası upload (multipart/form-data)
2. Pipeline seç (JSON modules list)
3. Job submit (async queue)
4. Real-time progress (WebSocket)
5. Results download (JSON/CSV)
6. Audit trail (database logs)

## Teknik İmplementasyon

### Core Logic (Shared by Both Interfaces)
- **PipelineManager:** Modülleri dinamik keşfet ve sırasıyla çalıştır
- **Core Modules:** Trim, drop_duplicates, handle_missing, standardize_headers, text_normalize, convert_types
- **Custom Plugins:** User-defined (modules/custom/*.py)
- **Database:** Audit trail, upload history, processing logs

### API Stack
- **Framework:** FastAPI (fast, async, self-documenting)
- **Database:** SQLite (lightweight, no setup)
- **Auth:** UUID-based API keys (stateless)
- **Queue:** In-memory FIFO (thread-safe)
- **WebSocket:** Real-time job progress
- **Logging:** Structured JSON (CloudWatch/ELK compatible)

## Success Metrics
- ✅ 28/28 unit tests PASS (100% coverage)
- ✅ API response time < 200ms (queue jobs < 5s)
- ✅ User can submit 100+ jobs/hour without blocking
- ✅ Real-time progress updates every 100ms (WebSocket)
- ✅ No data loss on error (atomic database operations)
- ✅ Easy plugin extension (< 50 lines for new plugin)
