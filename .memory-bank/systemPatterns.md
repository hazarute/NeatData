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

Yeni mimaride hibrit modül çağrıları kaldırılmıştır. Tüm CLI argümanları pipeline'a adım olarak eklenir ve temizlik akışı PipelineManager üzerinden merkezi şekilde yönetilir. Hata loglama ile atlanan satırlar bad_lines.csv dosyasına kaydedilir. Kod temizliği ve sürdürülebilirlik ön plandadır.

## Bileşenler Arası İlişkiler
- Tüm işlemler pandas DataFrame üzerinde gerçekleşir.
- openpyxl sadece çıktı aşamasında kullanılır.