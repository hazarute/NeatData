## Şu Anki Odak
View katmanı tamamen modüler mimariye taşındı; `neatdata_gui.py` artık `gui_helpers`, `UIState` ve `PipelineRunner` üzerinden widget düzeni ve olay yönetişimi sağlıyor ve I/O mantığı tamamen utils modüllerine devredildi.

## Son Yapılanlar
1.  `PipelineManager` güncellendi: Artık GUI'den gelen listeyi (`selected_modules_list`) işleyebiliyor.
2.  Plugin Protokolü (`__init__.py`) güncellendi: `run` yerine `process` ve `META` verisi standartlaştırıldı.
3.  `gui_io.py` oluşturuldu: "4 satır okuma hatası" (Delimiter bug) çözüldü.
4.  `neatdata_gui.py` tamamen GUI yardımcılarına devredildi; view katmanı artık `GuiHelpers`, `UiState`, `PipelineRunner` ile çalışıyor.
5.  `GuiLogger` artık `section`, `step`, `success`, vb. gibi styled metodlarla GUI loglarını temiz, terminalde zaman damgalı bir hikâye haline getiriyor; `PipelineRunner` da bu anlatıyı kullanarak okuma, pipeline, kayıt ve temizlik raporunu adım adım logluyor.

## Aktif Görevler
* GUI’den pipeline tetikleyip `PipelineRunner` akışının logging ve progress davranışını manuel olarak doğrulamak (`python neatdata_gui.py`).
* `Hepsiburada` ve `Akakçe` pluginlerinin yeni `PipelineRunner` düzeninde sorunsuz çalıştığını yeniden teyit etmek.
* Yeni log formatının GUI log kutusunda ve terminalde beklendiği gibi göründüğünü test etmek (adımlar, başarı/bilgi simgeleri, rapor başlığı).