 
# NeatData - CSV Data Cleaner 🧹

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https//img.shields.io/badge/status-active-success.svg)]()


A simple yet powerful Python script to clean and standardize messy CSV files, saving the output to a pristine Excel file.

**Now with GUI support!**
NeatData is not only a command-line tool, but also offers a simple graphical user interface (GUI) for non-technical users. Easily select files, configure cleaning options, and start cleaning with a click. All CLI and GUI options are managed centrally by the PipelineManager for full control and flexibility.

Türkçe açıklama için [aşağıya inin](#-neatdata---csv-veri-temizleyici-).

---

## 🌟 About The Project


This project provides a robust, extensible, and fully modular command-line tool for cleaning and standardizing messy CSV files. Key features and recent updates:
- **Modular architecture**: Each cleaning step is implemented as a separate module in the `modules/` folder. The pipeline manager orchestrates the execution order, making it easy to add, remove, or customize steps.
- **Dynamic pipeline management**: Users and developers can control which cleaning modules are applied, their order, and parameters via configuration or CLI.
- **Multiple file cleaning**: Clean any number of CSV files in a single run.
- **Automatic delimiter and encoding detection**: No need to guess file format.
- **Comprehensive cleaning report**: Summarizes all changes for each file.
- **User parameterization**: Choose cleaning options via command line.
It automates tedious tasks like removing duplicates, handling missing values, standardizing text, and more. The modular design makes it easy to extend the tool with new cleaning steps or custom workflows.

### Built With
*   [Python](https://www.python.org/) (minimum supported: 3.8+)
*   [Pandas](https://pandas.pydata.org/)
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (for modern GUI)
*   Optional: `ftfy` (better mojibake fixes) and `Unidecode` (ASCII transliteration)

## 🚀 Features


- **Modular cleaning pipeline**: Each cleaning step (column normalization, type inference, error value handling, duplicate removal, missing value handling, text standardization, export) is a separate module. Easily add, remove, or customize steps.
- **Pipeline manager**: Orchestrates the execution order of modules. Users can configure which steps to run and in what order.
- **Multi-file support**: Clean one or many CSV files in a single command.
- **Automatic delimiter & encoding detection**: No manual format guessing.
- **Column normalization**: Cleans and standardizes column names.
- **Type inference**: Automatically detects and converts column types.
- **Error/missing value handling**: Standardizes error values (ERROR, UNKNOWN, blank, NaN) and manages missing data.
- **Remove duplicates**: Ensures data integrity by dropping duplicate rows.
- **Text standardization**: Lowercases all text in a specified column.
- **User parameterization**: Choose cleaning options (drop/fill missing, text column, etc.) via CLI.
- **Flexible output**: Save cleaned data as Excel or CSV, with automatic output naming for batch jobs.
- **Cleaning report**: For each file, a summary of all cleaning actions and changes is printed.

**New in latest version:**
- All CLI and GUI cleaning options (e.g. --dropna, --fillna, --textcol) are now added as pipeline steps and managed centrally by PipelineManager. No hybrid/manual calls.
- Modern GUI with CustomTkinter: Dark theme, modern controls (switches, segmented buttons), rounded corners, spacious layout for better UX.
- Skipped/bad lines during CSV reading are logged to bad_lines.csv for transparency.
- PipelineManager orchestrates all cleaning steps; config, CLI, and GUI options are merged for full control.
- Codebase refactored for maintainability (duplicate functions removed).
 - `text_normalize` core helper added (NBSP, zero-width, smart quotes, mojibake fixes - `ftfy` optional; transliteration via `Unidecode` optional).
 - `clean_hepsiburada_scrape` plugin refactored to call `text_normalize` for general normalization.
 - Unit tests added for `text_normalize` (see `tests/test_text_normalize.py`). Run with `pytest -q`.

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
    
    Opsiyonel (dağınık scrape metinleri için önerilir):

    ```powershell
    pip install ftfy unidecode
    ```

Optional (recommended for messy scraped text normalization):

```powershell
pip install ftfy unidecode
```

Optional: for running unit tests in the repo
```powershell
pip install pytest
pytest -q
```

## 💻 Usage

Features:
- Modern dark theme with rounded corners and spacious layout
 
- Start/Stop buttons
- Console-like log area with detailed reports and error messages

**Basic single file cleaning:**
```bash
python clean_data.py --input data.csv
```

**Batch cleaning multiple files:**
```bash
python clean_data.py --input data1.csv data2.csv data3.csv
```

**Custom output name (single file):**
```bash
python clean_data.py --input data.csv --output my_cleaned.xlsx
```

**Custom options:**
- Run only selected modules:
    ```bash
    python clean_data.py --input data.csv --modules "standardize_headers,handle_missing"
    ```
- Drop rows with missing values:
    ```bash
    python clean_data.py --input data.csv --dropna
    ```
- Fill missing values with a default:
    ```bash
    python clean_data.py --input data.csv --fillna 0
    ```
- Standardize a text column:
    ```bash
    python clean_data.py --input data.csv --textcol name
    ```

**Note:** All CLI and GUI options above are now added as pipeline steps and executed in order by PipelineManager. No hybrid/manual calls.

**Error Handling:**
Any skipped/bad lines during CSV reading are automatically logged to bad_lines.csv for review.

- **Advanced pipeline customization:**
- **Available Modules (core module keys / files):**
    - `standardize_headers` — `modules/core/standardize_headers.py`
    - `drop_duplicates` — `modules/core/drop_duplicates.py`
    - `handle_missing` — `modules/core/handle_missing.py`
    - `trim_spaces` — `modules/core/trim_spaces.py`
    - `convert_types` — `modules/core/convert_types.py`
    - `text_normalize` — `modules/core/text_normalize.py` (general text normalization: NBSP removal, smart quotes, zero-width removal; optional mojibake fixes with `ftfy`; optional ASCII transliteration with `Unidecode`)
  
    Note: When using `--modules` or the GUI module selection, provide the module *keys* above (for example: `--modules "standardize_headers,handle_missing"`). Some documentation and examples may use friendly names; the pipeline resolves modules by their `META['key']` value.
- To run only selected modules: Use --modules "module1,module2" (e.g., --modules "standardize_headers,handle_missing")
- To add a new cleaning step, create a new module in the `modules/` folder and register it in the pipeline manager or config file.
- To change the order or remove steps, edit the pipeline manager configuration or use CLI options; all steps are orchestrated centrally.

**Output:**
- For each input file, a cleaned Excel or CSV file is created (default: `cleaned_<filename>.xlsx`).
- A cleaning report is printed for each file, summarizing all changes.
- In GUI mode, cleaning status and errors are shown in the log area, and progress bar updates in real time.

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

Proje Linki: [https://github.com/hazarute/NeatData](https://github.com/hazarute/NeatData)

## 🙏 Acknowledgments

*   [Pandas Library](https://pandas.pydata.org/) for its powerful data manipulation capabilities.
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) for making Excel file generation seamless.

---

# 🧹 NeatData - CSV Veri Temizleyici 🧹

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Durum](https//img.shields.io/badge/durum-aktif-başarılı.svg)]()


Dağınık CSV dosyalarını temizleyen, standartlaştıran ve çıktıyı temiz bir Excel/CSV dosyası olarak kaydeden, çoklu dosya desteği ve otomatik ayraç/encoding tespiti içeren güçlü bir Python betiği. Artık hem komut satırı hem de basit bir grafik arayüz (GUI) ile kullanılabilir.

**Son güncellemeler:**
- Tüm CLI ve GUI temizlik seçenekleri pipeline adımı olarak merkezi şekilde ekleniyor ve yönetiliyor.
- CustomTkinter ile modern GUI: Koyu tema, modern kontroller (anahtarlar, bölümlü butonlar), yuvarlatılmış köşeler, ferah düzen ile daha iyi UX.
- Hibrit/manuel modül çağrıları kaldırıldı; tüm akış PipelineManager üzerinden.
- CSV okuma sırasında atlanan satırlar bad_lines.csv dosyasına loglanıyor.
- Kod tabanı sürdürülebilirlik için temizlendi (tekrarlanan fonksiyonlar kaldırıldı).
 - `text_normalize` core helper eklendi: NBSP, zero-width, akıllı tırnak normalizasyonu, opsiyonel `ftfy` mojibake düzeltme ve isteğe bağlı ASCII transliteration (`Unidecode`).
 - `clean_hepsiburada_scrape` eklenti `text_normalize` ile normalize edecek şekilde refactor edildi (site-özgü temizleme kuraları plugin içinde kalır).
 - `text_normalize` için birim testleri eklendi (`tests/test_text_normalize.py`). Testleri çalıştırmak için `pytest -q`.

---

## 🌟 Proje Hakkında


Bu proje, dağınık CSV dosyalarını temizlemek ve standartlaştırmak için tamamen modüler, genişletilebilir ve dinamik bir komut satırı aracı sunar. Son güncellemeler ve ana özellikler:
- **Modüler mimari**: Her temizlik adımı `modules/` klasöründe ayrı bir modül olarak uygulanır. Pipeline yöneticisi, adımların sırasını ve uygulanacak modülleri kolayca kontrol etmenizi sağlar.
- **Dinamik pipeline yönetimi**: Kullanıcı ve geliştirici, hangi temizlik modüllerinin uygulanacağını, sırasını ve parametrelerini CLI veya yapılandırma ile belirleyebilir.
- **Çoklu dosya temizleme**: Birden fazla CSV dosyasını tek seferde temizleyin.
- **Otomatik ayraç ve encoding tespiti**: Dosya formatını manuel seçmeye gerek yok.
- **Kapsamlı temizlik raporu**: Her dosya için yapılan tüm değişikliklerin özetini sunar.
- **Kullanıcıdan parametre alma**: Temizlik seçeneklerini komut satırından belirleyin.
Tekrarlananları kaldırma, eksik değerleri yönetme, metinleri standartlaştırma gibi işlemleri otomatikleştirir. Modüler tasarım sayesinde yeni temizlik adımları veya özel iş akışları kolayca eklenebilir.

### Kullanılan Teknolojiler
*   [Python](https://www.python.org/)
*   [Pandas](https://pandas.pydata.org/)
*   [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
*   [CustomTkinter](https://customtkinter.tomschimansky.com/) (modern GUI için)
*   Opsiyonel: `ftfy` (mojibake düzeltmeleri için) ve `Unidecode` (ASCII transliteration için)


## 🚀 Özellikler

- **Modüler temizlik pipeline'ı**: Her temizlik adımı (sütun adı normalizasyonu, veri tipi algılama, hatalı değer yönetimi, tekrarları silme, eksik değer yönetimi, metin standardizasyonu, çıktı) ayrı bir modüldür. Adımları kolayca ekleyin, çıkarın veya özelleştirin.
- **Pipeline yöneticisi**: Modüllerin sırasını ve uygulanacak adımları yönetir. Kullanıcılar hangi adımların çalışacağını ve sırasını belirleyebilir.
- **Çoklu dosya desteği**: Birden fazla CSV dosyasını tek komutla veya GUI ile temizleyin.
- **Otomatik ayraç ve encoding tespiti**: Dosya formatını elle seçmeye gerek yok.
- **Sütun adı normalizasyonu**: Sütun adlarını temizler ve standartlaştırır.
- **Veri tipi algılama**: Sütun tiplerini otomatik algılar ve dönüştürür.
- **Hatalı/eksik değer yönetimi**: ERROR, UNKNOWN, boşluk, NaN gibi değerleri standartlaştırır ve eksik verileri yönetir.
- **Tekrarlananları silme**: Veri bütünlüğü için tekrar eden satırları kaldırır.
- **Metin standardizasyonu**: Belirtilen sütundaki tüm metinleri küçük harfe çevirir.
- **Kullanıcıdan parametre alma**: Temizlik seçeneklerini komut satırından veya GUI üzerinden belirleyin.
- **Esnek çıktı**: Temizlenmiş veriyi Excel veya CSV olarak kaydedin, toplu işlerde otomatik çıktı adı.
- **Temizlik raporu**: Her dosya için yapılan işlemlerin özet raporu ekrana veya GUI log alanına yazdırılır.
- **Modern GUI**: CustomTkinter ile koyu tema, yuvarlatılmış köşeler, ferah düzen, modern kontroller (anahtarlar, bölümlü butonlar), sürükle-bırak dosya seçimi, gerçek zamanlı ilerleme çubuğu, log alanı ile teknik bilgi gerektirmeden temizlik işlemi yapılabilir.

**Yeni:**
- Tüm CLI temizlik seçenekleri pipeline adımı olarak merkezi şekilde ekleniyor ve yönetiliyor.
- Hibrit/manuel modül çağrıları kaldırıldı; tüm akış PipelineManager üzerinden.
- CSV okuma sırasında atlanan satırlar bad_lines.csv dosyasına loglanıyor.
- Kod tabanı sürdürülebilirlik için temizlendi (tekrarlanan fonksiyonlar kaldırıldı).

## 📦 Kurulum

### Ön Gereksinimler
*   Python 3.8 veya üzeri
*   `pip` (Python paket yükleyici)

### Adımlar
1.  Depoyu klonlayın (veya betiği indirin)
    ```bash
    git clone https://github.com/kullanici_adiniz/NeatData.git
    cd NeatData
    ```

2.  Gerekli paketleri yükleyin
    ```bash
    pip install pandas openpyxl chardet python-dateutil customtkinter
    ```

## 💻 Kullanım



Betik komut satırından çalıştırılır ve artık birden fazla dosyayı aynı anda temizleyebilir. Tüm CLI temizlik seçenekleri pipeline adımı olarak merkezi şekilde ekleniyor ve yönetiliyor—hibrit/manuel modül çağrısı yok. Temel kullanım için betiği düzenlemenize gerek yoktur. Gelişmiş kullanıcılar ve geliştiriciler, `modules/` klasörüne yeni modüller ekleyerek ve pipeline yöneticisini veya config dosyasını yapılandırarak temizlik akışını özelleştirebilir.

**Tek dosya temizleme:**
```bash
python clean_data.py --input veri.csv
```

**Çoklu dosya temizleme:**
```bash
python clean_data.py --input veri1.csv veri2.csv veri3.csv
```

**Çıktı dosya adı belirleme (tek dosya):**
```bash
python clean_data.py --input veri.csv --output temizim.xlsx
```


**Ek seçenekler:**
- Sadece seçili modülleri çalıştır:
    ```bash
    python clean_data.py --input veri.csv --modules "standardize_headers,handle_missing"
    ```
- Eksik satırları sil:
    ```bash
    python clean_data.py --input veri.csv --dropna
    ```
- Eksik değerleri varsayılanla doldur:
    ```bash
    python clean_data.py --input veri.csv --fillna 0
    ```
- Bir metin sütununu standartlaştır:
    ```bash
    python clean_data.py --input veri.csv --textcol isim
    ```
- GUI ile temizlik işlemi başlatmak için:
    ```bash
    python clean_data.py --gui
    ```
    Özellikler:
    - Modern koyu tema ile yuvarlatılmış köşeler ve ferah düzen
    - Sürükle-bırak ile dosya seçimi (tekli/çoklu)
    - Modül seçimi paneli (çalıştırılacak adımları seçmek için checkbox'lar)
    - Temizlik seçenekleri paneli (modern kontroller ile dropna/fillna, textcol vb.)
    - Gerçek zamanlı ilerleme çubuğu ve durum göstergesi
    - Çıktı ayarları (Excel/CSV, çıktı dizini)
    - Başlat/Durdur butonları
    - Konsol benzeri log alanı için detaylı raporlar ve hata mesajları

**Not:** Tüm CLI seçenekleri pipeline adımı olarak eklenir ve PipelineManager tarafından sıralı şekilde çalıştırılır. Hibrit/manuel çağrı yok.

**Hata Yönetimi:**
CSV okuma sırasında atlanan satırlar otomatik olarak bad_lines.csv dosyasına loglanır.

**Gelişmiş pipeline özelleştirme:**
- **Mevcut Modüller (core module keys / dosyalar):**
    - `standardize_headers` — `modules/core/standardize_headers.py`
    - `drop_duplicates` — `modules/core/drop_duplicates.py`
    - `handle_missing` — `modules/core/handle_missing.py`
    - `trim_spaces` — `modules/core/trim_spaces.py`
    - `convert_types` — `modules/core/convert_types.py`

    Not: `--modules` veya GUI modül seçimlerinde yukarıdaki *module key* değerlerini kullanın (ör. `--modules "standardize_headers,handle_missing"`). Bazı belgelerde dostane isimler görülebilir; pipeline modülleri `META['key']` ile çözülür.
- Yeni bir temizlik adımı eklemek için `modules/` klasörüne yeni bir modül oluşturun ve pipeline yöneticisine veya config dosyasına kaydedin.
- Adım sırasını değiştirmek veya adım çıkarmak için pipeline yöneticisi veya config dosyasını düzenleyin; tüm adımlar merkezi olarak yönetilir.

**Çıktı:**
- Her girdi dosyası için temizlenmiş bir Excel veya CSV dosyası oluşturulur (varsayılan: `cleaned_<dosyaadı>.xlsx`).
- Her dosya için yapılan işlemlerin özet raporu ekrana yazdırılır.

## 🤝 Katkıda Bulunma

Katkılarınız, açık kaynak topluluğunu öğrenmek, ilham vermek ve yaratmak için harika bir yer haline getiren şeydir. Yaptığınız her katkı **büyük bir takdirle karşılanır**.

1.  Projeyi Fork'layın
2.  Özellik Dalınızı Oluşturun (`git checkout -b feature/HarikaOzellik`)
3.  Değişikliklerinizi Commit'leyin (`git commit -m 'Harika bir özellik ekle'`)
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
