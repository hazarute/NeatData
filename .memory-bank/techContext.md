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


## Modüller Dosya/Fonksiyon Yapısı
- Her temizlik adımı (ör. sütun normalizasyonu, tip dönüşümü, hata yönetimi) `modules/` klasöründe ayrı Python dosyası olarak yer alır ve process(df, **kwargs) arayüzüne sahiptir.
- Pipeline yönetimi PipelineManager ile merkezi ve büyüyebilir şekilde sağlanır.
- Pipeline adımları ve parametreleri config dosyası ile dinamik olarak yönetilir.
- Hata yönetimi, loglama ve modül ekleme/çıkarma PipelineManager üzerinden yapılır.
- Kullanıcı ve geliştirici için pipeline özelleştirme ve modül ekleme/çıkarma dokümantasyonu hazırlanacaktır.
- Yeni stratejik odak: Bellek Bankası ve dokümantasyonun yeni mimariye göre güncellenmesi.