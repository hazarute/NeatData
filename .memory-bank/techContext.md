
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



## Modüller Dosya/Fonksiyon Yapısı (Faz 4)

### **Utils Tabakası (`modules/utils/`)**
Faz 3'te oluşturulan shared infrastructure, GUI ve CLI tarafından kullanılır:

1. **ui_state.py** (UIState dataclass)
   - Alanlar: selected_core_keys, selected_custom_keys, output_type, output_dir, file_path
   - Metotlar: get_all_selected_modules(), clear()
   - Kullanım: GUI/CLI state management, PipelineRunner'a iletme

2. **gui_logger.py** (GuiLogger sınıfı)
   - GUI callback desteği (log message alıcısı)
   - Python logging adapter (file/stream handler)
   - Metotlar: log(), info(), warning(), error(), debug()
   - Kullanım: GUI textbox + CLI stdout + logging

3. **gui_helpers.py** (GuiHelpers statik sınıfı)
   - Component factories: create_file_picker_frame(), create_output_settings_frame()
   - Module panels: create_core_module_panel(), create_custom_module_panel()
   - Action & log: create_action_buttons(), create_log_box()
   - Türü: Union[CTk, CTkFrame] parent desteği

4. **gui_io.py** (GuiIO statik sınıfı)
   - Path ops: normalize_path(), ensure_output_dir()
   - File naming: get_output_filename(), get_full_output_path()
   - Checks: check_file_exists(), check_dir_writable()
   - Kullanım: CLI/GUI path normalizasyonu ve validasyonu

5. **pipeline_runner.py** (PipelineRunner sınıfı)
   - Metotlar: run_file(state, progress_callback=None)
   - İç metotlar: _execute_pipeline(), _save_output(), _generate_report()
   - Threading: progress_callback'i background'da günceller
   - Kullanım: GUI/CLI pipeline orchestration

### **Core Modules (`modules/core/`)**
- Her dosya: `META` dict + `process(df, **kwargs)` fonksiyon
- Core set: standardize_headers, drop_duplicates, handle_missing, convert_types, text_normalize, trim_spaces
- `META` içerir: key, name, description, parameters, defaults

### **Custom Plugins (`modules/custom/`)**
- Dosya yapısı: core modules gibi `META` + `process`
- Örnekler: clean_hepsiburada_scrape, fix_cafe_business_logic
- HR spesifik: clean_currency, clean_phone_format, clean_dates (v2'de eklenecek)
- PipelineManager: otomatik keşif, UIState seçimleri ile yönetim

### **Pipeline Management**
- **pipeline_manager.py**: ModuleDescriptor, PipelineStep, build_pipeline()
- **data_loader.py**: DataLoader sınıfı (encoding, delimiter, CSV/XLSX okuma, bad_lines)

### **IO & Reporting**
- **save_output.py**: SaveOutput sınıfı (Excel/CSV kaydı, sep_preamble, encoding)
- **report_generator.py**: ReportGenerator sınıfı (temizlik raporu, modül istatistikleri)

### **Entry Points**
- **cli_handler.py**: `main()` argparse-based, UIState oluştur, PipelineRunner loop
- **neatdata_gui.py**: CustomTkinter app, UIState + GuiHelpers, PipelineRunner threading