# System Patterns

## Mimari Tasarım (Modular & Layered)

Proje, sorumlulukların ayrıldığı katmanlı bir mimari izler:

1.  **View (Görünüm - `neatdata_gui.py`):**
    * "Aptal" (Dumb) katmandır. İş mantığı içermez.
    * `modules/utils/gui_helpers.py` kullanarak arayüzü çizer.
    * Kullanıcı seçimlerini `UIState` objesinde toplar.
    * İşlemi `PipelineRunner`'a devreder ve sadece logları gösterir.

2.  **Controller / Orchestrator (`modules/utils/pipeline_runner.py`):**
    * Süreci yönetir. GUI ve Backend arasındaki köprüdür.
    * `gui_io.py` ile dosyayı okutur (Smart Delimiter Detection).
    * `PipelineManager` ile temizlik adımlarını çalıştırır.
    * Sonucu diske kaydettirir ve hataları yakalar.

3.  **Core Logic (`modules/pipeline_manager.py`):**
    * Dinamik modül yükleyicisidir.
    * `modules/core/` ve `modules/custom/` klasörlerini tarar.
    * Seçilen modülleri sırasıyla çalıştırır (`run_pipeline`).

4.  **Plugins (Core & Custom):**
    * Tüm temizlik işlemleri bağımsız `.py` dosyalarıdır.

## Tasarım Desenleri

### 1. Plugin (Eklenti) Deseni
Custom modüller dinamik olarak keşfedilir. Her plugin şu protokolü (Protocol) uygulamalıdır:
* **Fonksiyon:** `process(df: pd.DataFrame, **kwargs) -> pd.DataFrame` isminde olmalıdır.
* **Metadata:** `META` isminde bir sözlük içermelidir (key, name, description, defaults).

### 2. Helper / Utility Ayrımı (`modules/utils/`)
* **`gui_helpers.py`:** Widget oluşturma kodları (Builder Pattern).
* **`gui_io.py`:** Dosya okuma/yazma (Strategy Pattern - farklı delimiter denemeleri).
* **`ui_state.py`:** Veri taşıyıcı (Data Transfer Object).
* **`gui_logger.py`:** Loglama adaptörü (Adapter Pattern).

### 3. Threading
GUI'nin donmaması için tüm temizlik işlemi (`PipelineRunner.run`) ayrı bir `threading.Thread` içinde çalıştırılır.

## Kod Standartları
* **Type Hinting:** Tüm fonksiyonlarda tip tanımlamaları kullanılmalı.
* **Protocol:** `NeatDataPlugin` protokolüne sadık kalınmalı.
* **Docstrings:** Modüllerin ne yaptığı açıklanmalı.