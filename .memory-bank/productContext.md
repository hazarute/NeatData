# Ürün Bağlamı (productContext.md)
## Neden Var?
Kullanıcıların, analiz öncesi dağınık ve tutarsız CSV veri setlerini hızlıca temizleyip, güvenilir ve standart bir formata dönüştürmelerini sağlamak için geliştirilmiştir.
## Çözülen Problemler
- Tekrarlanan satırlar nedeniyle veri bütünlüğünün bozulması
- Eksik (NaN, N/A, null, ERROR, UNKNOWN, -, ?, boşluk) değerlerin analizleri zorlaştırması
- Farklı formatlarda girilmiş metinlerin tutarsızlık yaratması
## İdeal Kullanıcı Deneyimi
- Kullanıcı, komut satırından veya interaktif olarak kolayca çalıştırır.
- Girdi dosyasını, ayraç ve encoding gibi parametreleri seçebilir veya otomatik algılatabilir.
- Eksik/hatalı değerleri nasıl yöneteceğini seçebilir (sil, doldur, özel değer ata).
- Temizlik pipeline’ındaki adımlar modüller olarak seçilebilir, eklenebilir veya çıkarılabilir.
- PipelineManager ile adımların sırası, parametreleri ve uygulanacak modüller merkezi ve dinamik olarak yönetilir.
- Her temizlik modülü process(df, **kwargs) arayüzüne sahiptir.
- Yeni temizlik modülleri eklenerek ürün özelleştirilebilir, config dosyası ile pipeline kolayca değiştirilebilir.
- Pipeline özelleştirme ve modül ekleme/çıkarma için kapsamlı dokümantasyon ve örnekler sağlanacaktır.
- Temizlenmiş ve biçimlendirilmiş Excel veya CSV dosyası hızlıca elde edilir.
- Temizlik raporu ile yapılan işlemler takip edilebilir.
## Ürünün Nasıl Çalışması Gerekir?
- Dosya okuma sırasında ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır.
- Sütun adları ve veri tipleri normalize edilir.
- Eksik/hatalı değerler standart şekilde işlenir.
- Kullanıcıdan alınan tercihlere göre temizlik adımları uygulanır.
- Sonuç yeni bir Excel veya CSV dosyasına kaydedilir, temizlik raporu üretilir.
# Ürün Bağlamı (productContext.md)

## Neden Var?
Kullanıcıların, analiz öncesi dağınık ve tutarsız CSV veri setlerini hızlıca temizleyip, güvenilir ve standart bir formata dönüştürmelerini sağlamak için geliştirilmiştir.

## Çözülen Problemler
- Tekrarlanan satırlar nedeniyle veri bütünlüğünün bozulması
- Eksik (NaN) değerlerin analizleri zorlaştırması
- Farklı formatlarda girilmiş metinlerin tutarsızlık yaratması


## İdeal Kullanıcı Deneyimi
- Kullanıcı, komut satırından veya interaktif olarak kolayca çalıştırır.
- Girdi dosyasını, ayraç ve encoding gibi parametreleri seçebilir veya otomatik algılatabilir.
- Eksik/hatalı değerleri nasıl yöneteceğini seçebilir (sil, doldur, özel değer ata).


- Temizlik pipeline’ındaki adımlar modüller olarak seçilebilir, eklenebilir veya çıkarılabilir.
- PipelineManager ile adımların sırası, parametreleri ve uygulanacak modüller merkezi ve dinamik olarak yönetilir.
- Her temizlik modülü process(df, **kwargs) arayüzüne sahiptir.
- Yeni temizlik modülleri eklenerek ürün özelleştirilebilir, config dosyası ile pipeline kolayca değiştirilebilir.
- Pipeline özelleştirme ve modül ekleme/çıkarma için kapsamlı dokümantasyon ve örnekler sağlanacaktır.
- Temizlenmiş ve biçimlendirilmiş Excel veya CSV dosyası hızlıca elde edilir.
- Temizlik raporu ile yapılan işlemler takip edilebilir.

## Ürünün Nasıl Çalışması Gerekir?
- Dosya okuma sırasında ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır.
- Sütun adları ve veri tipleri normalize edilir.
- Eksik/hatalı değerler standart şekilde işlenir.
- Kullanıcıdan alınan tercihlere göre temizlik adımları uygulanır.
- Sonuç yeni bir Excel veya CSV dosyasına kaydedilir, temizlik raporu üretilir.