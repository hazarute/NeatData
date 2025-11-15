# Sistem Mimarisi (systemPatterns.md)

## Genel Mimari
- Komut satırı tabanlı Python (CLI) ve modern CustomTkinter tabanlı GUI
- Girdi: Farklı ayraç ve encoding ile gelen CSV/XLSX dosyaları
- Çıktı: Temizlenmiş Excel veya CSV dosyası, detaylı temizlik raporu
- **Faz 4 İnovasyonu:** CLI ve GUI ortak `UIState` + `PipelineRunner` altyapısı kullanır

## Temel Akış (Faz 4 - UIState + PipelineRunner)
1. **Giriş & State Oluşturma:**
   - CLI: `--input`, `--core-modules`, `--custom-modules`, `--output-dir`, `--output-format` argümanlarıyla `UIState` oluşturur
   - GUI: Switch/Checkbox seçimleriyle `UIState` oluşturur
   - UIState: (selected_core_keys, selected_custom_keys, output_type, output_dir, file_path)

2. **Pipeline Orchestration (`PipelineRunner.run_file`):**
   - DataLoader: encoding/delimiter tespit, CSV/XLSX okuma, hatalı satırları loglama
   - Module seçimi: UIState'den core/custom keys PipelineManager'a verilir
   - Pipeline çalıştırma: Modüller sırayla uygulanır
   - Error handling: İstisnaları GuiLogger'a gönder

3. **Output & Loglama:**
   - Temizlenmiş DataFrame Excel/CSV olarak kaydedilir (GuiIO ile path kontrolü)
   - Detaylı rapor oluşturulur
   - GuiLogger callback ile raporlama (GUI: textbox + logging.Handler, CLI: stdout)

## Tasarım Desenleri (Faz 3-4)

- **Shared Infrastructure (UIState + PipelineRunner):** CLI ve GUI aynı state management, pipeline execution kullanır → kod tekrarı azalır, tutarlılık sağlanır
- **Core/Custom Plugin Pattern:** `META` + `process` arayüzü ile gevşek bağlılık
- **Dynamic Plugin Discovery:** PipelineManager `importlib.util` ile `modules/core/` ve `modules/custom/` tarar
- **Centralized Logging:** GuiLogger callback pattern ile GUI/CLI/tests birleştirilir
- **Component Factories:** GuiHelpers CTkinter bileşen yaratımını merkezileştirir

## Bileşenler Arası İlişkiler (Faz 4 Mimarisi)

- Tüm işlemler pandas DataFrame üzerinde gerçekleşir
- openpyxl sadece çıktı aşamasında kullanılır

### **Utils Tabakası (`modules/utils/`)** - Shared Infrastructure
  - `ui_state.py`: State dataclass (UIState) - both GUI/CLI
  - `gui_logger.py`: Centralized logging (GUI callback + Python logging adapter)
  - `gui_helpers.py`: CTkinter component factories (file picker, output settings, module panels, action buttons)
  - `gui_io.py`: File/path operations (normalization, output naming, permission checks)
  - `pipeline_runner.py`: Pipeline orchestration (run_file, _execute_pipeline, _save_output, _generate_report)

### **Core Modules**
  - `modules/core/*.py`: Standart veri temizlik (standardize_headers, drop_duplicates, handle_missing, convert_types, text_normalize, trim_spaces)
  - Each: `META` + `process(df, **kwargs)`

### **Custom Plugins**
  - `modules/custom/*.py`: Sektör-spesifik (HR: clean_currency, clean_phone_format, clean_dates)
  - PipelineManager otomatik keşfeder, UIState seçimleri ile yönetilir

### **Pipeline Management**
  - `pipeline_manager.py`: `ModuleDescriptor`, `PipelineStep`, `build_pipeline()`
  - `data_loader.py`: Encoding tespit, CSV/XLSX okuma, bad_lines loglama

### **IO & Reporting**
  - `save_output.py`: Excel/CSV kaydı (sep_preamble, encoding options)
  - `report_generator.py`: Temizlik raporu (modül bazlı istatistikler)

### **Entry Points**
  - `cli_handler.py`: CLI (UIState oluştur, PipelineRunner çağır, multi-file loop)
  - `neatdata_gui.py`: GUI (CustomTkinter, UIState + GuiHelpers, threading)

## Pipeline Selection Behavior Note

- Empty module selection = No modules run (not "use all defaults")
- If `core_keys` is `None` (unset), manager falls back to default core set
- Ensures GUI behavior matches user expectations (switching all off → no processing)

## Faz 4 Farkları (Eski vs Yeni)

| Özellik | Faz 2-3 | Faz 4 |
|---------|---------|-------|
| State Management | Inline (GUI/CLI) | UIState dataclass |
| Logging | GUI-specific | GuiLogger (unified) |
| Pipeline Run | GUI thread inline | PipelineRunner class |
| Code Reuse | Min | Max (shared utils) |
| CLI args | `--core-modules`, `--custom-modules` | `--core-modules`, `--custom-modules`, `--output-dir`, `--output-format` |
| Multi-file | Tek dosya | Loop'ta UIState clone |
