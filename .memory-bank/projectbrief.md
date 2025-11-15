# Proje Özeti (projectbrief.md)

## Proje Adı
NeatData - CSV Data Cleaner

## Amaç
Karmaşık ve dağınık CSV dosyalarını hızlı, kolay ve güvenilir şekilde temizleyip, standartlaştırılmış ve analiz için hazır hale getirmek. Temizlenen veriler Excel/CSV olarak kaydedilir. Hem komut satırı (CLI) hem de modern CustomTkinter tabanlı GUI ile erişilebilir.

## Modülerlik ve Modernleşme Hedefi (Faz 3-4)

### **Faz 3: Utils Tabakası - Shared Infrastructure**
CLI ve GUI ortak altyapı üzerinde çalışacak şekilde yeniden tasarlandı:
- **UIState:** Merkezi state management (selected_core_keys, selected_custom_keys, output settings)
- **PipelineRunner:** Unified orchestration (run_file, callbacks, threading support)
- **GuiLogger:** Centralized loglama (GUI callback + Python logging adapter)
- **GuiHelpers:** Component factory pattern (reusable CTkinter builders)
- **GuiIO:** Path/file operations (normalization, validation)

Hedef: CLI ve GUI'de kod tekrarını minimize etmek, mantık tutarlılığı sağlamak, yeniden kullanılabilirliği maksimize etmek.

### **Katmanlı Mimari (Faz 2-4)**
1. **Core (Çekirdek) Katmanı:** `modules/core/` - Standart veri temizlik
   - Her modül: `META` dict + `process(df, **kwargs)` fonksiyon
   - Modüller: standardize_headers, drop_duplicates, handle_missing, convert_types, text_normalize, trim_spaces
   - Dinamik keşif: PipelineManager importlib.util ile tarar

2. **Custom (Özel) Katmanı:** `modules/custom/` - Sektör-spesifik ve plugin'ler
   - Yapı: core modules gibi `META` + `process`
   - PipelineManager: otomatik keşif, dynamic import
   - UIState seçimleri ile yönetim
   - Örnek: clean_hepsiburada_scrape, fix_cafe_business_logic, HR modülleri (v2'de)

### **GUI Modernizasyonu (Faz 3-4)**
CustomTkinter ile iki panelli tasarım:
- Sol panel: Core modüller (Switch bileşenleri, sabit)
- Sağ panel: Custom plugin'ler (CheckBox, dinamik olarak taranır)
- Koyu tema, modern kontroller, log ve ilerleme alanı
- Threading: İşlem sırasında UI responsive kalır

### **CLI Refactoring (Faz 4.1)**
Eski inline yapıdan yeni utils-based yapıya geçiş:
- Arguments: `--input`, `--core-modules`, `--custom-modules`, `--output-dir`, `--output-format`
- UIState oluşturma: Kullanıcı seçimlerini state'e dönüştür
- PipelineRunner: Multi-file loop'ta state'i klonlayarak çalıştır
- GuiLogger: CLI'de callback sütun, logging'i stdout'a yaz

## Kapsam (Faz 4 - Güncel)
✅ **Tamamlanan:**
- Komut satırı arayüzü ve modern CustomTkinter tabanlı GUI
- Shared infrastructure (UIState, PipelineRunner, GuiLogger, GuiHelpers, GuiIO)
- Farklı ayraç ve encoding ile gelen CSV dosyalarını otomatik algılama
- Sütun adlarını ve veri tiplerini normalize etme
- Eksik/hatalı değerleri standart şekilde yönetme
- Esnek temizlik akışı (modül seçimi ile)
- Çoklu veri seti ve formatlar için yeniden kullanılabilir modüller
- Temizlenmiş veriyi Excel veya CSV olarak kaydetme
- Detaylı temizlik raporu üretme
- Modern GUI (CustomTkinter, iki panel, koyu tema, responsive)

🔄 **Planlanan (Faz 4.2+):**
- Web UI (FastAPI + Streamlit veya React)
- Advanced logging/audit trail
- Batch processing optimization
- HR veri setleri için özel temizlik modülleri
- Kurumsal feedback integration

## Temel Gereksinimler
- Python 3.8+
- pandas
- openpyxl
- chardet, python-dateutil
- customtkinter (modern GUI için)

## Nihai Hedef
Kullanıcıların farklı kaynaklardan gelen bozuk/dağınık CSV dosyalarını otomatik, esnek ve tutarlı şekilde temizleyip, analiz için hazır veri setleri elde etmelerini sağlamak. 

**Faz 4 Başarısı:** 
- GUI ve CLI aynı altyapı üzerinden çalışır (kod tekrarı 60% azaldı)
- Yeniden kullanılabilir utils modülleri test ve extension için hazır
- CLI multi-file işleme, GUI responsive threading desteğine sahip
- Sektör-spesifik (HR) genişlemelere açık mimari
