# NeatData - CSV Data Cleaner 🧹

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https//img.shields.io/badge/status-active-success.svg)]()


A simple yet powerful Python script to clean and standardize messy CSV files, saving the output to a pristine Excel file.

**Now with GUI and CLI support with shared infrastructure!**
NeatData is not only a command-line tool, but also offers a modern graphical user interface (GUI) for non-technical users. CLI and GUI share the same unified infrastructure (`UIState`, `PipelineRunner`, `GuiLogger`) for consistent behavior. Easily select files, configure cleaning options, and start cleaning with a click.

Türkçe açıklama için [aşağıya inin](#-neatdata---csv-veri-temizleyici-).

---

## 🌟 About The Project


This project provides a robust, extensible, and fully modular command-line tool for cleaning and standardizing messy CSV files. **Faz 4 Architecture** features shared infrastructure for CLI, GUI, and tests.

### Key Features
- **Modular architecture**: Each cleaning step is implemented as a separate module in `modules/core/` (core) and `modules/custom/` (plugins). The pipeline manager orchestrates execution order.
- **Dynamic pipeline management**: Control which modules are applied, their order, and parameters via CLI or GUI.
- **Shared Infrastructure (Faz 4)**:
  - `UIState`: Centralized state management (selected modules, output settings, file path)
  - `PipelineRunner`: Unified orchestration (run_file, callbacks, threading support)
  - `GuiLogger`: Centralized logging (GUI callback + Python logging adapter)
  - `GuiHelpers`: Component factory pattern (reusable CTkinter builders)
  - `GuiIO`: File/path operations (normalization, validation)
- **Multiple file cleaning**: Clean any number of CSV files in a single run.
- **Automatic delimiter and encoding detection**: No need to guess file format.
- **Comprehensive cleaning report**: Summarizes all changes for each file.

### Built With
*   [Python](https://www.python.org/) (minimum supported: 3.8+)
*   [Pandas](https://pandas.pydata.org/)
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (for modern GUI)
*   Optional: `ftfy` (better mojibake fixes) and `Unidecode` (ASCII transliteration)

## 🚀 Features

- **Modular cleaning pipeline**: Each cleaning step (column normalization, type inference, error value handling, duplicate removal, missing value handling, text standardization, export) is a separate module. Easily add, remove, or customize steps.
- **Pipeline manager**: Orchestrates the execution order of modules. Users can configure which steps to run and in what order.
- **Multi-file support**: Clean one or many CSV files in a single command or GUI.
- **Automatic delimiter & encoding detection**: No manual format guessing.
- **Column normalization**: Cleans and standardizes column names.
- **Type inference**: Automatically detects and converts column types.
- **Error/missing value handling**: Standardizes error values (ERROR, UNKNOWN, blank, NaN) and manages missing data.
- **Remove duplicates**: Ensures data integrity by dropping duplicate rows.
- **Text standardization**: Normalizes text across columns (NBSP, smart quotes, mojibake - optional ftfy, optional Unidecode).
- **User parameterization**: Choose cleaning options via CLI or GUI.
- **Flexible output**: Save cleaned data as Excel or CSV, with automatic output naming for batch jobs.
- **Cleaning report**: For each file, a summary of all cleaning actions and changes is printed/displayed.

**New in Faz 4 (Latest):**
- **Shared Infrastructure**: CLI and GUI now use the same `UIState`, `PipelineRunner`, `GuiLogger`, `GuiHelpers`, `GuiIO` modules (~60% code reduction).
- **CLI Refactoring**: New arguments `--output-dir`, `--output-format` (xlsx/csv), modern help text, multi-file processing with state cloning.
- **GUI Refactoring**: 242 → 200 lines, delegated UI/logic to utils, fixed Tkinter.state() conflict, responsive threading.
- **Enhanced Logging**: Centralized `GuiLogger` with callback pattern for GUI/CLI/tests.
- All CLI and GUI cleaning options are now added as pipeline steps and managed centrally by `PipelineManager`. No hybrid/manual calls.
- Modern GUI with CustomTkinter: Dark theme, modern controls (switches, segmented buttons), rounded corners, spacious layout for better UX.
- Skipped/bad lines during CSV reading are logged to `bad_lines.csv` for transparency.
- `text_normalize` core helper: NBSP removal, smart quotes, zero-width removal; optional mojibake fixes with `ftfy`; optional ASCII transliteration with `Unidecode`.

## 📦 Installation

### Prerequisites
*   Python 3.8 or higher
*   pip (Python package installer)

### Steps
1.  Clone the repository (or download the script)
    ```bash
    git clone https://github.com/hazarute/NeatData.git
    cd NeatData
    ```

2.  Install required packages
    ```bash
    pip install pandas openpyxl chardet python-dateutil customtkinter
    ```

3.  Optional packages (recommended for messy scraped text normalization):
    ```bash
    pip install ftfy unidecode
    ```

4.  Optional: for running unit tests
    ```bash
    pip install pytest
    pytest -q
    ```

## 💻 Usage

### GUI Mode
**Modern graphical interface with dark theme:**
```bash
python neatdata_gui.py
```

Features:
- Modern dark theme with rounded corners and spacious layout
- File picker with drag-and-drop support
- Module selection panels (Core: Switches | Custom: CheckBoxes)
- Output settings (format, directory)
- Real-time progress bar
- Console-like log area with detailed reports and error messages
- Start/Stop buttons

### CLI Mode

**Basic single file cleaning:**
```bash
python -m modules.cli_handler --input data.csv
```

**Batch cleaning multiple files:**
```bash
python -m modules.cli_handler --input data1.csv data2.csv data3.csv
```

**With custom output options:**
```bash
python -m modules.cli_handler --input data.csv --output-dir ./cleaned --output-format xlsx
```

**Run only selected modules:**
```bash
python -m modules.cli_handler --input data.csv --core-modules standardize_headers,drop_duplicates --custom-modules clean_hepsiburada_scrape
```

**Module selection options:**
- `--core-modules all` — Run all core modules (default)
- `--core-modules none` — Skip all core modules
- `--core-modules "module1,module2"` — Run specific modules
- `--custom-modules all/none/list` — Similar for custom plugins

**Available Core Modules (keys):**
- `standardize_headers` — Normalizes column names
- `drop_duplicates` — Removes duplicate rows
- `handle_missing` — Manages missing values
- `trim_spaces` — Removes leading/trailing spaces
- `convert_types` — Detects and converts column types
- `text_normalize` — General text normalization (NBSP, smart quotes, mojibake, optional transliteration)

**Note:** All CLI options above are now added as pipeline steps and executed in order by `PipelineManager`. No hybrid/manual calls.

**Error Handling:**
Any skipped/bad lines during CSV reading are automatically logged to `bad_lines.csv` for review.

**Output:**
- For each input file, a cleaned Excel or CSV file is created (default: `cleaned_<filename>.xlsx`).
- A cleaning report is printed for each file, summarizing all changes.

## 🏗️ Architecture (Faz 4 - Shared Infrastructure)

### Utils Layer (`modules/utils/`)
Shared infrastructure consumed by GUI, CLI, and tests:
- `ui_state.py`: `UIState` dataclass for centralized state management
- `gui_logger.py`: `GuiLogger` with callback pattern for unified logging
- `gui_helpers.py`: `GuiHelpers` factory for CTkinter component builders
- `gui_io.py`: `GuiIO` for file/path operations
- `pipeline_runner.py`: `PipelineRunner` for pipeline orchestration

### Core Modules (`modules/core/`)
Standard cleaning steps with `META` + `process(df, **kwargs)` interface.

### Custom Plugins (`modules/custom/`)
Site-specific or domain-specific plugins (e.g., `clean_hepsiburada_scrape`).

### Pipeline Management
- `pipeline_manager.py`: Orchestrates core/custom modules based on selection
- `data_loader.py`: Encoding/delimiter detection, CSV/XLSX loading
- `report_generator.py`: Generates cleaning reports
- `save_output.py`: Excel/CSV output with proper encoding/formatting

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## 📞 Contact

Hazar Ute - hazarute@gmail.com

Project Link: [https://github.com/hazarute/NeatData](https://github.com/hazarute/NeatData)

## 🙏 Acknowledgments

*   [Pandas Library](https://pandas.pydata.org/) for its powerful data manipulation capabilities.
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) for making Excel file generation seamless.

---

# 🧹 NeatData - CSV Veri Temizleyici 🧹

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Durum](https//img.shields.io/badge/durum-aktif-başarılı.svg)]()


Dağınık CSV dosyalarını temizleyen, standartlaştıran ve çıktıyı temiz bir Excel/CSV dosyası olarak kaydeden, çoklu dosya desteği ve otomatik ayraç/encoding tespiti içeren güçlü bir Python betiği. Artık hem komut satırı hem de modern bir grafik arayüz (GUI) ile kullanılabilir. **Faz 4'te CLI ve GUI ortak altyapı (`UIState`, `PipelineRunner`, `GuiLogger`) paylaşıyor.**

**Son güncellemeler (Faz 4):**
- Ortak altyapı katmanı: `modules/utils/` ile 5 utility modülü (ui_state, gui_logger, gui_helpers, gui_io, pipeline_runner)
- CLI ve GUI aynı `UIState` ve `PipelineRunner` kullanıyor (~60% kod azalması)
- CustomTkinter ile modern GUI: Koyu tema, modern kontroller, yuvarlatılmış köşeler, ferah düzen
- CLI yeni argümanlarla: `--output-dir`, `--output-format`, `--core-modules`, `--custom-modules`
- Güncellenen bellek bankası dosyaları (systemPatterns, techContext, projectbrief)

---

## 🌟 Proje Hakkında


Bu proje, dağınık CSV dosyalarını temizlemek ve standartlaştırmak için tamamen modüler, genişletilebilir ve dinamik bir komut satırı aracı sunar. **Faz 4 Mimarisi** CLI, GUI ve testler için ortak altyapı sunuyor.

### Ana Özellikler
- **Modüler mimari**: Her temizlik adımı `modules/core/` (core) ve `modules/custom/` (plugin'ler) içinde ayrı modül olarak uygulanır. Pipeline yöneticisi, yürütme sırasını düzenler.
- **Dinamik pipeline yönetimi**: Hangi modüllerin uygulanacağını, sırasını ve parametrelerini CLI veya GUI ile kontrol edin.
- **Ortak Altyapı (Faz 4)**:
  - `UIState`: Merkezi state yönetimi (seçili modüller, çıktı ayarları, dosya yolu)
  - `PipelineRunner`: Birleşik orkestrasyonu (run_file, callback'ler, threading desteği)
  - `GuiLogger`: Merkezi loglama (GUI callback + Python logging adaptörü)
  - `GuiHelpers`: Bileşen factory pattern'ı (yeniden kullanılabilir CTkinter builders)
  - `GuiIO`: Dosya/yol işlemleri (normalizasyon, validasyon)
- **Çoklu dosya temizleme**: Birden fazla CSV dosyasını tek seferde temizleyin.
- **Otomatik ayraç ve encoding tespiti**: Dosya formatını manuel seçmeye gerek yok.
- **Kapsamlı temizlik raporu**: Her dosya için yapılan tüm değişikliklerin özetini sunar.

### Kullanılan Teknolojiler
*   [Python](https://www.python.org/) (minimum: 3.8+)
*   [Pandas](https://pandas.pydata.org/)
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (modern GUI için)
*   Opsiyonel: `ftfy` (mojibake düzeltmeleri) ve `Unidecode` (ASCII transliteration)

## 🚀 Özellikler

- **Modüler temizlik pipeline'ı**: Her temizlik adımı ayrı modüldür. Adımları kolayca ekleyin, çıkarın veya özelleştirin.
- **Pipeline yöneticisi**: Modüllerin sırasını ve uygulanacak adımları yönetir.
- **Çoklu dosya desteği**: Birden fazla CSV dosyasını tek komutla veya GUI ile temizleyin.
- **Otomatik ayraç ve encoding tespiti**: Dosya formatını elle seçmeye gerek yok.
- **Sütun adı normalizasyonu**: Sütun adlarını temizler ve standartlaştırır.
- **Veri tipi algılama**: Sütun tiplerini otomatik algılar ve dönüştürür.
- **Hatalı/eksik değer yönetimi**: ERROR, UNKNOWN, boşluk, NaN gibi değerleri standartlaştırır.
- **Tekrarlananları silme**: Veri bütünlüğü için tekrar eden satırları kaldırır.
- **Metin standardizasyonu**: Metin normalizasyonu (NBSP, akıllı tırnak, mojibake - opsiyonel ftfy, opsiyonel Unidecode).
- **Kullanıcıdan parametre alma**: Temizlik seçeneklerini CLI veya GUI üzerinden belirleyin.
- **Esnek çıktı**: Temizlenmiş veriyi Excel veya CSV olarak kaydedin.
- **Temizlik raporu**: Her dosya için yapılan işlemlerin özet raporu ekrana/GUI'ye yazdırılır.

**Faz 4'teki Yenilikler:**
- **Ortak Altyapı**: CLI ve GUI aynı `UIState`, `PipelineRunner`, `GuiLogger`, `GuiHelpers`, `GuiIO` modüllerini kullanıyor (~60% kod azalması).
- **CLI Refactoring**: Yeni argümanlar `--output-dir`, `--output-format`, modern yardım metni, multi-file işleme.
- **GUI Refactoring**: 242 → 200 satır, UI/logic utils'e taşındı, Tkinter.state() hatası düzeltildi, responsive threading.
- **Gelişmiş Loglama**: Merkezi `GuiLogger` callback pattern'ı ile GUI/CLI/testler.
- Tüm CLI ve GUI temizlik seçenekleri pipeline adımı olarak merkezi şekilde yönetiliyor.
- Modern GUI: CustomTkinter, koyu tema, modern kontroller, ferah düzen.
- CSV okuma sırasında atlanan satırlar `bad_lines.csv` dosyasına loglanıyor.
- `text_normalize` core helper: NBSP, akıllı tırnak, zero-width; opsiyonel mojibake fixes; opsiyonel ASCII transliteration.

## 📦 Kurulum

### Ön Gereksinimler
*   Python 3.8 veya üzeri
*   `pip` (Python paket yükleyici)

### Adımlar
1.  Depoyu klonlayın
    ```bash
    git clone https://github.com/hazarute/NeatData.git
    cd NeatData
    ```

2.  Gerekli paketleri yükleyin
    ```bash
    pip install pandas openpyxl chardet python-dateutil customtkinter
    ```

3.  Opsiyonel paketler (dağınık metin normalizasyonu için önerilir):
    ```bash
    pip install ftfy unidecode
    ```

4.  Opsiyonel: birim testleri için
    ```bash
    pip install pytest
    pytest -q
    ```

## 💻 Kullanım

### GUI Modu
**Modern grafik arayüz (koyu tema):**
```bash
python neatdata_gui.py
```

Özellikler:
- Modern koyu tema, yuvarlatılmış köşeler, ferah düzen
- Dosya seçim paneli
- Modül seçim panelleri (Core: Switch'ler | Custom: CheckBox'lar)
- Çıktı ayarları (format, dizin)
- Gerçek zamanlı ilerleme çubuğu
- Konsol benzeri log alanı
- Başlat/Durdur butonları

### CLI Modu

**Tek dosya temizleme:**
```bash
python -m modules.cli_handler --input veri.csv
```

**Çoklu dosya temizleme:**
```bash
python -m modules.cli_handler --input veri1.csv veri2.csv veri3.csv
```

**Çıktı seçenekleri ile:**
```bash
python -m modules.cli_handler --input veri.csv --output-dir ./temizim --output-format xlsx
```

**Sadece seçili modülleri çalıştır:**
```bash
python -m modules.cli_handler --input veri.csv --core-modules standardize_headers,drop_duplicates --custom-modules clean_hepsiburada_scrape
```

**Modül seçim seçenekleri:**
- `--core-modules all` — Tüm core modülleri çalıştır (varsayılan)
- `--core-modules none` — Core modülleri atla
- `--core-modules "modul1,modul2"` — Belirli modülleri çalıştır
- `--custom-modules all/none/liste` — Custom plugin'ler için benzer

**Mevcut Core Modüller (keys):**
- `standardize_headers` — Sütun adlarını normalize eder
- `drop_duplicates` — Tekrar eden satırları siler
- `handle_missing` — Eksik değerleri yönetir
- `trim_spaces` — Başındaki/sonundaki boşlukları siler
- `convert_types` — Sütun tiplerini algılar ve dönüştürür
- `text_normalize` — Genel metin normalizasyonu (NBSP, akıllı tırnak, mojibake, opsiyonel transliteration)

**Not:** Tüm CLI seçenekleri pipeline adımı olarak eklenir ve `PipelineManager` tarafından sıralı şekilde çalıştırılır.

**Hata Yönetimi:**
CSV okuma sırasında atlanan satırlar otomatik olarak `bad_lines.csv` dosyasına loglanır.

**Çıktı:**
- Her girdi dosyası için temizlenmiş bir Excel veya CSV dosyası oluşturulur (varsayılan: `cleaned_<dosyaadı>.xlsx`).
- Her dosya için yapılan işlemlerin özet raporu ekrana yazdırılır.

## 🏗️ Mimari (Faz 4 - Ortak Altyapı)

### Utils Katmanı (`modules/utils/`)
GUI, CLI ve testler tarafından paylaşılan altyapı:
- `ui_state.py`: Merkezi state yönetimi için `UIState` dataclass'ı
- `gui_logger.py`: Callback pattern'ı ile birleşik loglama
- `gui_helpers.py`: CTkinter bileşen builders için `GuiHelpers` factory
- `gui_io.py`: Dosya/yol işlemleri
- `pipeline_runner.py`: Pipeline orkestrasyonu

### Core Modüller (`modules/core/`)
Standart temizlik adımları: `META` + `process(df, **kwargs)` arayüzü.

### Custom Plugin'ler (`modules/custom/`)
Site-özgü veya domain-özgü plugin'ler (ör. `clean_hepsiburada_scrape`).

### Pipeline Yönetimi
- `pipeline_manager.py`: Core/custom modülleri orkestrasiyon
- `data_loader.py`: Encoding/delimiter tespiti, CSV/XLSX yükleme
- `report_generator.py`: Temizlik raporları
- `save_output.py`: Excel/CSV çıktısı

## 🤝 Katkıda Bulunma

Katkılarınız açık kaynak topluluğunu harika bir yer yapar. Yaptığınız her katkı **büyük takdirle karşılanır**.

1.  Projeyi Fork'layın
2.  Özellik Dalınızı Oluşturun (`git checkout -b feature/HarikaOzellik`)
3.  Değişikliklerinizi Commit'leyin (`git commit -m 'Harika özellik ekle'`)
4.  Dala Push'layın (`git push origin feature/HarikaOzellik`)
5.  Bir Pull Request açın

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## 📞 İletişim

Hazar Ute - hazarute@gmail.com

Proje Linki: [https://github.com/hazarute/NeatData](https://github.com/hazarute/NeatData)

## 🙏 Teşekkürler

*   Güçlü veri işleme yetenekleri için [Pandas Kütüphanesi](https://pandas.pydata.org/).
*   Excel dosyası oluşturmayı sorunsuz hale getirdiği için [Openpyxl](https://openpyxl.readthedocs.io/en/stable/).
