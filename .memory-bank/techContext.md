
# Teknik Detaylar (techContext.md)

## Kullanılan Teknolojiler
- Python 3.8+
- pandas
- openpyxl
- chardet (encoding tespiti için)
- python-dateutil (tarih algılama için)
- CustomTkinter (modern GUI)

## Notlar
- Minimum Python sürümü proje içinde 3.8+ olarak kullanılmaktadır; README dosyası ve kurulum adımları bu sürüme göre güncellendi.
- `customtkinter` GUI için gereklidir — requirements listesinde opsiyonel olarak belirtildi.


## Geliştirme Ortamı Kurulumu
1. Python 3.6 veya üzeri kurulu olmalı.
2. Gerekli paketler: `pip install pandas openpyxl chardet python-dateutil customtkinter`


## Bağımlılıklar
- pandas: Veri işleme ve temizleme
- openpyxl: Excel dosyası oluşturma
- chardet: Dosya encoding tespiti
- python-dateutil: Tarih sütunlarını algılama ve dönüştürme
- CustomTkinter: Modern GUI için (pip ile kurulur)


## Teknik Kısıtlamalar
- Farklı ayraç ve encoding ile gelen dosyalar için otomatik tespit modülü gereklidir.
- Hem komut satırı hem modern GUI üzerinden çalışır.
- Büyük veri setlerinde bellek kullanımı pandas'a bağlıdır.



## Modüller Dosya/Fonksiyon Yapısı
- Core temizlik adımları `modules/core/*.py` altında yer alır; her dosya `META` (key, name, description, defaults) ve `process(df, **kwargs)` fonksiyonunu expose eder.
- Custom plugin’ler `modules/custom/*.py` klasörüne bırakılır; PipelineManager bu dosyaları otomatik keşfeder.
- `modules/pipeline_manager.py` dinamik import ile core/custom modülleri `ModuleDescriptor` objelerine dönüştürür, pipeline adımlarını `PipelineStep` ile yönetir.
- `modules/data_loader.py` içindeki `DataLoader` sınıfı encoding/delimiter tespiti yapar, CSV/XLSX okur, hatalı satırları `bad_lines.csv` dosyasına yazar.
- CLI (`modules/cli_handler.py`) yeni argümanlarla ( `--core-modules`, `--custom-modules`, `--handle-missing-strategy`, `--convert-columns`) pipeline’ı kurar.
- GUI (`neatdata_gui.py`) CustomTkinter tabanlı modern arayüz sağlar, core Switch + custom ScrollableFrame bileşenleriyle plugin seçimi yapar ve her 5 saniyede custom klasörünü yeniden tarar.