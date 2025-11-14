
# Sistem Mimarisi (systemPatterns.md)

## Genel Mimari
- Komut satırı tabanlı Python betiği ve modern CustomTkinter tabanlı GUI
- Girdi: Farklı ayraç ve encoding ile gelen CSV/XLSX dosyaları (CLI veya GUI üzerinden seçilebilir)
- Çıktı: Temizlenmiş Excel veya CSV dosyası, detaylı temizlik raporu

## Temel Akış
1. CLI/GUI giriş: `modules/cli_handler.py` veya `neatdata_gui.py` üzerinden parametreler alınır. CLI `--core-modules` ve `--custom-modules` argümanlarıyla seçim yapar, GUI’de core modüller Switch, custom plugin’ler dinamik Checkbox olarak sunulur.
2. Veri okuma: `modules/data_loader.py` içerisindeki `DataLoader` sınıfı encoding/delimiter tespit eder, CSV/XLSX dosyalarını okur ve kötü satırları `bad_lines.csv` dosyasına kaydeder.
3. Pipeline orchestration: `modules/pipeline_manager.py` core modülleri (`modules/core/*.py`) ve custom plugin’leri (`modules/custom/*.py`) otomatik keşfeder. Her modül `META` bilgisiyle self-describing olur.
4. Kullanıcı seçimlerine göre `PipelineManager.build_pipeline` adımları oluşturulur ve sırayla çalıştırılır.
5. Temizlenmiş veri Excel/CSV olarak kaydedilir (`modules/save_to_excel.py` veya `DataFrame.to_csv`), çıktı dizini GUI/CLI ile seçilebilir.
6. Detaylı rapor `modules/report_generator.py` tarafından üretilir, GUI loguna ve CLI konsoluna yazılır.

## Tasarım Desenleri

- Core/custom plugin ayrımı, `META` + `process` arayüzü ile gevşek bağlılık sağlar.
- `PipelineManager` plugin keşfini `importlib.util` ile yapar, modül başına `ModuleDescriptor` üretir, pipeline adımlarını `PipelineStep` veri sınıfı olarak saklar.
- `DataLoader` sınıfı tek sorumluluk prensibiyle dosya okuma, encoding/delimiter tespiti ve hata kayıtlarını yönetir.
- GUI, CustomTkinter Switch/ScrollableFrame bileşenleriyle modüler seçim sunar, belirli aralıklarla custom klasörünü yeniden tarar.

## Bileşenler Arası İlişkiler
- Tüm işlemler pandas DataFrame üzerinde gerçekleşir.
- openpyxl sadece çıktı aşamasında kullanılır.
- GUI ile CLI arasında entegrasyon modülü olacak (ör. arka planda PipelineManager çağrısı).
- Yeni modüller: data_loader.py (veri yükleme), report_generator.py (detaylı raporlama), cli_handler.py (CLI işleme, modül seçimi ile pipeline).
- HR spesifik modüller: clean_currency.py, clean_phone_format.py, clean_dates.py, standardize_text_column.py (genişletilmiş) - PipelineManager config ile yönetilecek.

## Pipeline Selection Behavior Note

- The pipeline manager previously treated an *empty* module selection as "use all core modules", which caused surprising behavior when users intentionally disabled all core modules via the GUI. This has been corrected: when a caller explicitly passes an empty list for `core_keys` (or the GUI reports no core modules selected), the pipeline will run *no* core modules. If `core_keys` is `None` (unset), the manager will fall back to the default core set.

This ensures that turning all core switches off in the GUI results in no core processing, which is the expected and least-surprising behavior.