# Tech Context

## Teknoloji Yığını
* **Dil:** Python 3.10+
* **GUI:** CustomTkinter (Modern UI)
* **Veri İşleme:** Pandas (Core & Custom modüller için)
* **Sistem:** `importlib` (Dinamik modül yükleme), `threading` (Arka plan işlemleri)

## Klasör Yapısı (Güncel)
```text
NeatData/
├── main.py (veya neatdata_gui.py)
├── modules/
│   ├── core/               # Standart temizlik araçları (dropna, trim vb.)
│   ├── custom/             # Müşteriye özel pluginler (process() + META)
│   ├── utils/
│   │   ├── gui_helpers.py  # UI bileşenleri
│   │   ├── gui_io.py       # Akıllı CSV/Excel okuma-yazma
│   │   ├── gui_logger.py   # Loglama sınıfı
│   │   ├── pipeline_runner.py # İş akışı yöneticisi
│   │   └── ui_state.py     # Veri sınıfı
│   └── pipeline_manager.py # Modül keşif ve yürütme motoru
└── ...