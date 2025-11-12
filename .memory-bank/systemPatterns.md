# Sistem Mimarisi (systemPatterns.md)

## Genel Mimari
- Komut satırı tabanlı Python betiği
- Girdi: Farklı ayraç ve encoding ile gelen CSV dosyaları
- Çıktı: Temizlenmiş Excel veya CSV dosyası, temizlik raporu

## Temel Akış
1. Dosya okuma: Ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır
2. Sütun adları ve veri tipleri normalize edilir
3. Eksik/hatalı değerler (ERROR, UNKNOWN, boşluk, NaN) standart şekilde işlenir
4. Kullanıcıdan alınan tercihlere göre temizlik adımları uygulanır
5. Temizlenmiş veri Excel veya CSV olarak kaydedilir
6. Temizlik raporu üretilir


## Tasarım Desenleri
- Pipeline yönetimi PipelineManager sınıfı ile merkezi ve büyüyebilir bir yapıda sağlanır.
- Her temizlik modülü process(df, **kwargs) arayüzüne sahiptir.
- Pipeline adımları ve parametreleri config dosyası ile dinamik olarak yönetilir.
- Hata yönetimi ve loglama PipelineManager üzerinden merkezi olarak yapılır.
- Modül ekleme/çıkarma ve pipeline özelleştirme dokümantasyon ile desteklenir.
- Bellek Bankası ve dokümantasyon yeni mimariye göre güncellenmiştir.

## Bileşenler Arası İlişkiler
- Tüm işlemler pandas DataFrame üzerinde gerçekleşir.
- openpyxl sadece çıktı aşamasında kullanılır.