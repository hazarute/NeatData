# Ürün Bağlamı (productContext.md)

## Neden Var?
Kullanıcıların ve **diğer sistemlerin**, analiz öncesi dağınık ve tutarsız CSV veri setlerini hızlıca temizleyip, güvenilir ve standart bir formata dönüştürmelerini sağlamak için geliştirilmiştir. 

**Çift Interface Stratejisi:** 
- **GUI (CustomTkinter):** İnsan kullanıcılar için modern, koyu temalı ve ferah bir masaüstü arayüzü.
- **REST API (FastAPI):** Otomatik sistemler ve uygulamalar için, JSON tabanlı veri temizleme servisi.

## Çözülen Problemler
- Tekrarlanan satırlar nedeniyle veri bütünlüğünün bozulması
- Eksik (NaN) değerlerin analizleri zorlaştırması
- Farklı formatlarda girilmiş metinlerin tutarsızlık yaratması
- Eski tip, karmaşık ve göz yoran arayüzlerin kullanıcıyı zorlaması
- HR veri setlerinde yaygın olan para birimi, telefon ve tarih format tutarsızlıkları


## İdeal Kullanıcı Deneyimi
- Kolay dosya seçimi (sürükle-bırak veya dosya gezgini)
- Temizlik seçeneklerinin görsel olarak yapılandırılması
- Gerçek zamanlı ilerleme ve hata mesajları
- Temizlik raporunun ve logların görüntülenmesi
- Çıktı formatı ve dizini seçimi
- Son kullanılan ayarların hatırlanması
- Hem CLI hem GUI ile çalışabilme
- Modern, koyu temalı, yuvarlatılmış köşeli ve ferah bir arayüz
- Sektör spesifik temizlik seçenekleri GUI'de kolayca seçilebilir

- Dosya okuma sırasında ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır.
- Sütun adları ve veri tipleri core modüller ile normalize edilir.
- Eksik/hatalı değerler PipelineManager üzerinden seçilen strateji ile işlenir.
- **GUI'de:** Kullanıcı core modülleri Switch ile, custom plugin'leri dinamik Checkbox ile açıp kapatır. Sonuç yeni bir Excel veya CSV dosyasına kaydedilir.
- **API'de:** JSON payload gönderilen endpoint'ler, temizlenmiş veriyi JSON ile döner. Sonuç seçilerek CSV/Excel olarak da kaydedilebilir.
- Modern GUI CustomTkinter tabanlıdır; log, ilerleme ve otomatik plugin keşfi sunar.
- REST API FastAPI tabanlıdır; Swagger UI (/docs) otomatik dokümantasyon sunar.