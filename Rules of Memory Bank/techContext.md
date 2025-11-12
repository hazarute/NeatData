# Teknik Detaylar (techContext.md)

## Kullanılan Teknolojiler
- Python 3.6+
- pandas
- openpyxl
- chardet (encoding tespiti için)
- python-dateutil (tarih algılama için)

## Geliştirme Ortamı Kurulumu
1. Python 3.6 veya üzeri kurulu olmalı.
2. Gerekli paketler: `pip install pandas openpyxl chardet python-dateutil`

## Bağımlılıklar
- pandas: Veri işleme ve temizleme
- openpyxl: Excel dosyası oluşturma
- chardet: Dosya encoding tespiti
- python-dateutil: Tarih sütunlarını algılama ve dönüştürme

## Teknik Kısıtlamalar
- Farklı ayraç ve encoding ile gelen dosyalar için otomatik tespit modülü gereklidir.
- Komut satırı üzerinden çalışır.
- Büyük veri setlerinde bellek kullanımı pandas'a bağlıdır.

## Modüler Dosya/Fonksiyon Yapısı

- Her temizlik adımı (ör. sütun normalizasyonu, tip dönüşümü, hata yönetimi) artık `modules/` klasöründe ayrı Python dosyası olarak yer alıyor.
- Ana script (clean_data.py), pipeline yöneticisi ile hangi modüllerin hangi sırayla çalışacağını dinamik olarak belirliyor.
- Kullanıcı ve geliştirici, pipeline'ı özelleştirebilir, yeni modül ekleyip çıkarabilir.
- Yeni stratejik odak: Pipeline özelleştirme, modül ekleme/çıkarma örnekleri ve kapsamlı dokümantasyon.