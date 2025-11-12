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

- Modüler mimari ve pipeline yönetimi başarıyla uygulandı.
- Her temizlik adımı ayrı modül/fonksiyon olarak `modules/` klasöründe yer alıyor.
- Pipeline yöneticisi ile adımların sırası ve uygulanacak modüller dinamik olarak kontrol edilebiliyor.
- Kullanıcı ve geliştirici, pipeline'ı özelleştirebilir, yeni modül ekleyip çıkarabilir.
- Yeni stratejik odak: Pipeline özelleştirme, modül ekleme/çıkarma örnekleri ve kapsamlı dokümantasyon.

## Bileşenler Arası İlişkiler
- Tüm işlemler pandas DataFrame üzerinde gerçekleşir.
- openpyxl sadece çıktı aşamasında kullanılır.