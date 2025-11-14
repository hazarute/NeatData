## Yapılacaklar:
- [ ] Yeni plugin gereksinimlerini mimardan al.

## Yeni Bitenler (son değişiklikler):
[X] PipelineManager `build_pipeline` empty-selection bug fixed (explicit empty list no longer runs all core modules).
[X] `handle_missing` default strategy changed to `noop` and requires explicit `columns` to operate (prevents accidental mass drop).
[X] `fix_cafe_business_logic` updated: safer duplicate removal, deleted_records_log.csv with `Reason`, flexible date parsing, and `process` alias added for backwards compatibility.

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