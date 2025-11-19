# Progress Status

## Tamamlananlar
- [x] Core ve Custom modül ayrımı.
- [x] Dinamik Plugin Yükleme Sistemi (`PipelineManager`).
- [x] GitHub Copilot için Plugin Protokolü (`modules/custom/__init__.py`).
- [x] Hepsiburada ve Akakçe için örnek Custom Pluginler.
- [x] Yardımcı Modüller (`gui_helpers`, `gui_io`, `ui_state`).
- [x] `neatdata_gui.py` view katmanını `GuiHelpers` + `PipelineRunner` ile tamamen sadeleştirmek.
- [x] `GuiLogger` ve `PipelineRunner` log akışını styled adımlarla (section/step/success) yapılandırmak.

## Devam Edenler
- [ ] Entegrasyon Testleri (GUI -> Runner -> Manager -> Plugin) ve GUI’deki log kutusunda yeni adım/success formatının doğrulanması.

## Bekleyenler
- [ ] EXE formatına paketleme (PyInstaller).
- [ ] Kullanıcı ayarlarının (son kullanılan klasör vb.) kaydedilmesi.