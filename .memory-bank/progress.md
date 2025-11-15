## Yapılacaklar (Faz 4 — Sonraki Aşama):
 - [X] CLI handler güncelle (UIState ve PipelineRunner ile uyumluluk). ✅ TAMAMLANDI
 - [ ] Web UI prototype (FastAPI + Streamlit) — veri temizleme web servisi.
 - [ ] Batch processing mod — çoklu dosya işleme.
 - [ ] Advanced logging ve audit trail — temizlik işlemlerinin kayıtları.
 - [ ] Kurumsal ekiplerden feedback topla ve yeni plugin taleplerini önceliklendir.

## Yeni Bitenler (Faz 4.1 — CLI Refactoring Tamamlandı):
[X] `cli_handler.py` tamamen refactor edildi: UIState + PipelineRunner kullanıyor.
[X] Argümanlar modernize edildi: --output-dir, --output-format, all/none/liste seçenekleri.
[X] Help mesajları ve örnekler eklendi.
[X] CLI test başarılı: 10000 satırlı dosya temizlendi, Excel çıktısı oluşturuldu.
[X] GUI ve CLI artık ortak infrastructure kullanıyor (UIState, PipelineRunner, GuiLogger).
[X] `modules/utils/ui_state.py` oluşturuldu: UIState dataclass + helper metotlar.
[X] `modules/utils/gui_logger.py` oluşturuldu: GuiLogger sınıfı (GUI + logging integration).
[X] `modules/utils/gui_helpers.py` oluşturuldu: GuiHelpers bileşen fabrikası.
[X] `modules/utils/gui_io.py` oluşturuldu: File/directory operations.
[X] `modules/utils/pipeline_runner.py` oluşturuldu: Pipeline orchestration.
[X] `neatdata_gui.py` refactor edildi: Utils modüllerine geçişi tamamlandı.
[X] Refactored GUI test edildi: Başarılı başlangıç ve loglama doğrulandı.
[X] Hatalar çözüldü: self.state vs Tkinter.state() çakışması; type hints uyumluluğu.
[X] PipelineManager `build_pipeline` empty-selection bug fixed (explicit empty list no longer runs all core modules).
[X] `handle_missing` default strategy changed to `noop` and requires explicit `columns` to operate (prevents accidental mass drop).
[X] `fix_cafe_business_logic` updated: safer duplicate removal, deleted_records_log.csv with `Reason`, flexible date parsing, and `process` alias added for backwards compatibility.
[X] `text_normalize` core helper eklendi: NBSP, smart quotes normalization, mojibake fix (opsiyonel ftfy), transliteration (Unidecode opsiyonel). `process()` ve `META` eklendi.
[X] `clean_hepsiburada_scrape` custom plugin refactor edildi: `clean_text_pipeline` kullanılarak ortak normalizasyon uygulanıyor.
[X] `requirements.txt` öneri ile opsiyonel paketler `ftfy` ve `Unidecode` eklendi.
[X] `tests/test_text_normalize.py` birim testleri eklendi (temel test vakaları).
[X] `modules/custom/clean_hepsiburada_scrape.py` güncellendi: in-place temizleme (orijinal sütunların üzerine yazma), sağlam fiyat parsing, güvenli extra parsing, ve `deleted_records_log.csv` için zenginleştirilmiş logging eklendi.
[X] `modules/pipeline_manager.py` eklendi/ayrıştırıldı: `selected_modules_list` desteği ve `run_pipeline` metodu ile GUI seçimlerine göre modül çalıştırma sağlandı.
[X] `neatdata_gui.py` güncellendi: GUI seçimleri pipeline'a aktarılıyor; CSV-only seçilince .xlsx kopyası oluşturulmuyor.
[X] `modules/data_loader.py` için delimiter-fallback eklendi (tek sütunlu okuma tespit edilirse `sep=','` ile tekrar deniyor).
[X] `tests/test_clean_hepsiburada_scrape.py` eklendi ve lokal test runner ile çalıştırıldı (geçti).

## Bitenler:
[X] CLI'ye --modules argümanı ekle (cli_handler.py).
[X] clean_currency.py modülü yaz (Salary sütunu için).
[X] clean_phone_format.py modülü yaz (Phone sütunu için).
[X] clean_dates.py modülü yaz (Join Date sütunu için).
[X] standardize_text_column.py'yi metin düzeltmeleri için genişlet (First Name, Last Name, Department).
[X] Yeni modülleri PipelineManager config'ine ekle.
[X] pipeline_config.toml'u güncelle.
[X] GUI'ye yeni modül seçenekleri ekle (checkbox'lar).
[X] Yeni modülleri test et (messy_HR_data.csv ile).
[X] Geliştirilmiş sistemi test et.
[X] CLI modları belirle ve dokümantasyon hazırla.
[X] report_generator.py'yi detaylandır (modül bazlı değişiklikler, özet).
[X] GUI'ye modül seçimi ekle (checkbox'lar).
[X] GUI raporlamasını iyileştir (detaylı log).
[X] clean_currency.py modülü yaz (Salary sütunu için).
[X] clean_phone_format.py modülü yaz (Phone sütunu için).
[X] clean_dates.py modülü yaz (Join Date sütunu için).
[X] standardize_text_column.py'yi metin düzeltmeleri için genişlet (First Name, Last Name, Department).
[X] Yeni modülleri PipelineManager config'ine ekle.
[X] pipeline_config.toml'u güncelle.
[X] GUI'ye yeni modül seçenekleri ekle (checkbox'lar).
[X] Yeni modülleri test et (messy_HR_data.csv ile).
[X] Geliştirilmiş sistemi test et.
[X] Core/custom plugin mimarisi kuruldu; PipelineManager yeniden yazıldı.
[X] Core modüller standardize_headers, drop_duplicates, handle_missing, trim_spaces, convert_types sıfırdan yazıldı.
[X] DataLoader sınıfı yeniden tasarlandı (encoding/delimiter tespiti + bad_lines loglama).
[X] CLI yeni argümanlarla dinamik pipeline'a bağlandı.
[X] CustomTkinter GUI çekirdek/dinamik plugin panelleriyle yenilendi.

## Hatalar:
- [ ] Henüz raporlanmış hata yok.