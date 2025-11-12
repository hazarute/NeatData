# Ürün Bağlamı (productContext.md)

## Neden Var?
Kullanıcıların, analiz öncesi dağınık ve tutarsız CSV veri setlerini hızlıca temizleyip, güvenilir ve standart bir formata dönüştürmelerini sağlamak için geliştirilmiştir.

## Çözülen Problemler
- Tekrarlanan satırlar nedeniyle veri bütünlüğünün bozulması
- Eksik (NaN) değerlerin analizleri zorlaştırması
- Farklı formatlarda girilmiş metinlerin tutarsızlık yaratması


## İdeal Kullanıcı Deneyimi
 Kolay dosya seçimi (sürükle-bırak veya dosya gezgini)
 Temizlik seçeneklerinin görsel olarak yapılandırılması
 Gerçek zamanlı ilerleme ve hata mesajları
 Temizlik raporunun ve logların görüntülenmesi
 Çıktı formatı ve dizini seçimi
 Son kullanılan ayarların hatırlanması
 Hem CLI hem GUI ile çalışabilme

## Ürünün Nasıl Çalışması Gerekir?
- Dosya okuma sırasında ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır.
- Sütun adları ve veri tipleri normalize edilir.
- Eksik/hatalı değerler standart şekilde işlenir.
- Kullanıcıdan alınan tercihlere göre temizlik adımları uygulanır.
- Sonuç yeni bir Excel veya CSV dosyasına kaydedilir, temizlik raporu üretilir.