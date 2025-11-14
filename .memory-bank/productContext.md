# Ürün Bağlamı (productContext.md)

## Neden Var?
Kullanıcıların, analiz öncesi dağınık ve tutarsız CSV veri setlerini hızlıca temizleyip, güvenilir ve standart bir formata dönüştürmelerini sağlamak için geliştirilmiştir. Son strateji: Kullanıcıya modern, koyu temalı ve ferah bir arayüz sunmak.

## Çözülen Problemler
- Tekrarlanan satırlar nedeniyle veri bütünlüğünün bozulması
- Eksik (NaN) değerlerin analizleri zorlaştırması
- Farklı formatlarda girilmiş metinlerin tutarsızlık yaratması
- Eski tip, karmaşık ve göz yoran arayüzlerin kullanıcıyı zorlaması
- HR veri setlerinde yaygın olan para birimi, telefon ve tarih format tutarsızlıkları


## İdeal Kullanıcı Deneyimi
- Kolay dosya seçimi (sürükle-bırak veya dosya gezgini)
- Temizlik seçeneklerinin görsel olarak yapılandırılması
- Gerçek zamanlı ilerleme ve hata mesajları
- Temizlik raporunun ve logların görüntülenmesi
- Çıktı formatı ve dizini seçimi
- Son kullanılan ayarların hatırlanması
- Hem CLI hem GUI ile çalışabilme
- Modern, koyu temalı, yuvarlatılmış köşeli ve ferah bir arayüz
- Sektör spesifik temizlik seçenekleri GUI'de kolayca seçilebilir

- Dosya okuma sırasında ayraç ve encoding otomatik tespit edilir veya kullanıcıdan alınır.
- Sütun adları ve veri tipleri core modüller ile normalize edilir.
- Eksik/hatalı değerler PipelineManager üzerinden seçilen strateji ile işlenir.
- Kullanıcı core modülleri Switch ile, custom plugin’leri dinamik Checkbox ile açıp kapatır (GUI) veya CLI argümanlarıyla belirtir.
- Sonuç yeni bir Excel veya CSV dosyasına kaydedilir, temizlik raporu üretilir.
- Modern GUI CustomTkinter tabanlıdır; log, ilerleme ve otomatik plugin keşfi sunar.