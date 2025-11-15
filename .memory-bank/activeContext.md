

# Aktif Bağlam (activeContext.md)

## Mevcut Çalışma Odağı
Modüler mimari yeniden kuruldu: core ve custom modüller ayrıldı, dinamik plugin sistemi devrede. Son geliştirme adımı olarak proje içine genel amaçlı metin normalizasyonu eklendi; şu an core yardımcı fonksiyonların (mojibake, NBSP, quote normalization) stabil hale getirilmesi ve test edilmesi aşamasındayız.

## Kararlar
- `modules/core/` altında beş temel modül (standardize_headers, drop_duplicates, handle_missing, trim_spaces, convert_types) sıfırdan yazıldı ve META+process arayüzünü takip ediyor.
- `modules/custom/` plugin klasörü tanımlandı; PipelineManager bu klasörü dinamik olarak tarıyor.
- PipelineManager yeniden yazıldı; ModuleDescriptor/PipelineStep veri sınıfları ve `build_pipeline` akışı ile core/custom seçimleri destekleniyor.
- DataLoader sınıfı CSV/XLSX okuma, encoding/delimiter tespiti ve bad_lines loglamasını yönetiyor.
- CLI yeni argümanlarla plugin mimarisine bağlandı.
- GUI tamamen yenilendi: sol panelde core Switch'ler, sağ panelde otomatik yenilenen custom ScrollableFrame yer alıyor; CustomTkinter arayüz pipeline seçimini PipelineManager’a iletiyor.

## Stratejik Sonraki Yön
- Kurumsal ekiplerden gelecek özel plugin ihtiyaçlarını toplamak.
- Core seti genişletme ve plugin metadata/parametre yapılandırmasını esnekleştirme.
- Core: `text_normalize.py` için ek testler ve opsiyonel işlevler eklemek (emoji remover, currency normalizer, locale aware numeric parsing).

## Son Yapılan Değişiklikler
- PipelineManager: `build_pipeline` davranışı düzeltildi; boş seçim artık hiçbir core modülünün çalışmamasını sağlar.
- `handle_missing` modülü varsayılan olarak no-op olacak şekilde güncellendi; bir işlem yapılması için `columns` parametresi gerekmektedir.
- `fix_cafe_business_logic` modülü güvenli hale getirildi; hatalı kayıtlar `deleted_records_log.csv` ile loglanıyor ve `process` alias'ı eklendi.
 - `text_normalize` eklendi: NBSP/zero-width temizleme, akıllı tırnak normalize etme, mojibake düzeltme (opsiyonel `ftfy`), `unidecode` transliteration opsiyonu. `process()` ve `META` sağlanarak core modül haline getirildi.
 - `clean_hepsiburada_scrape` custom plugin'i core `clean_text_pipeline` kullanacak şekilde refactor edildi; plugin özel iş kuralları custom modülde kalır.
 - `requirements.txt` opsiyonel bağımlılıklar için güncellendi (`ftfy`, `Unidecode` notları eklendi).
 - `tests/test_text_normalize.py` eklendi (temel durumlar, NBSP, tırnaklar, mojibake fallback testleri).
- `modules/custom/clean_hepsiburada_scrape.py` güncellendi: artık ayrı `Clean_*` sütunları üretmiyor; orijinal sütunları doğrudan temizleyip aynı isimle kaydediyor. Fiyat parsing daha sağlam hale getirildi (Avrupa/US/mixed heuristikleri), `extra` alanı güvenli şekilde parse edilip JSON-string olarak saklanabiliyor ve hatalı fiyat dönüşümleri `deleted_records_log.csv` içine `Orig_Price_Text` ve `Row_Index` ile loglanıyor.
- `modules/pipeline_manager.py` içerisinde GUI'den gelen seçime göre çalıştırma desteklendi (`selected_modules_list` ve `run_pipeline`). Boş seçim durumunda core modüller çalıştırılmıyor.
- `neatdata_gui.py` güncellendi: GUI seçimleri (`core` ve `custom`) `selected_modules` olarak toplanıyor ve `pipeline_manager.run_pipeline` çağrılıyor; CSV seçiliyse artık otomatik .xlsx kopyası oluşturulmuyor.
- `modules/data_loader.py` için delimiter fallback eklendi: tek sütunlu okuma tespit edilirse `sep=','` ile yeniden deneniyor.
- Birim testler eklendi/çalıştırıldı: `tests/test_clean_hepsiburada_scrape.py` plugin için fiyat formatları, review parsing ve `extra` parse güvenliği testleri içeriyor.
- Uygulama çalıştırıldı; `bad_lines.csv` içinde şu oturumda 1 hatalı satır (Lenovo row) loglandı — kaynak CSV'deki tırnak/escaping problemine işaret ediyor.

## Kısa Not
- Bu oturumda yapılan değişiklikler doğrudan kod seviyesinde uygulandı ve sözdizimi kontrolü başarıyla geçti. Bir sonraki adım: değişiklikleri Git'e commit ve push, ardından bellek dosyalarını (`progress.md`) güncellemek.