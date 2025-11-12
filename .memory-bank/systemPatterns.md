
# Sistem Mimarisi (systemPatterns.md)

## Genel Mimari
- Komut satırı tabanlı Python betiği ve basit GUI
- Girdi: Farklı ayraç ve encoding ile gelen CSV dosyaları (CLI veya GUI üzerinden seçilebilir)
- Çıktı: Temizlenmiş Excel veya CSV dosyası, temizlik raporu



## Temel Akış
1. Dosya okuma: Ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır (CLI veya GUI)
2. Sütun adları ve veri tipleri normalize edilir
3. Eksik/hatalı değerler (ERROR, UNKNOWN, boşluk, NaN) standart şekilde işlenir
4. Kullanıcıdan alınan tercihlere göre temizlik adımları uygulanır (GUI paneli veya CLI argümanları)
5. Temizlenmiş veri Excel veya CSV olarak kaydedilir, çıktı dizini ve formatı GUI/CLI ile seçilebilir
6. Temizlik raporu üretilir ve GUI'de görüntülenebilir




## Tasarım Desenleri

Yeni mimaride hibrit modül çağrıları kaldırılmıştır. Tüm CLI argümanları pipeline'a adım olarak eklenir ve temizlik akışı PipelineManager üzerinden merkezi şekilde yönetilir. Hata loglama ile atlanan satırlar bad_lines.csv dosyasına kaydedilir. Kod temizliği ve sürdürülebilirlik ön plandadır.
GUI entegrasyonu ile dosya seçimi, temizlik seçenekleri ve çıktı ayarları görsel olarak sunulacak. GUI dosyası kök dizinde (`gui.py` veya `neatdata_gui.py`) yer alacak ve arka planda PipelineManager'ı çağıracak.


## Bileşenler Arası İlişkiler
- Tüm işlemler pandas DataFrame üzerinde gerçekleşir.
- openpyxl sadece çıktı aşamasında kullanılır.
- GUI ile CLI arasında entegrasyon modülü olacak (ör. arka planda PipelineManager çağrısı).