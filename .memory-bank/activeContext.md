# Aktif Bağlam (activeContext.md)

## Mevcut Çalışma Odağı
Mevcut odak: PipelineManager'ın merkezi yönetimi güçlendiriliyor. Tüm CLI argümanları ve temizlik adımları PipelineManager'a adım olarak ekleniyor. Hibrit yapı kaldırılıyor, akış tamamen PipelineManager üzerinden yönetilecek. Hata loglama ve atlanan satırların bad_lines.csv dosyasına kaydedilmesi ekleniyor. Kod temizliği ve tekrarlanan fonksiyonların kaldırılması odakta.

## Aktif Kararlar ve Gerekçeler
* PipelineManager artık hem config dosyasından hem de CLI argümanlarından gelen adımları merkezi olarak yönetiyor.
* Hibrit modül çağrıları kaldırılıyor, tüm akış tek merkezden yönetiliyor.
* Hata yönetimi: on_bad_lines ile atlanan satırlar bad_lines.csv dosyasına loglanacak.
* Kod temizliği: pipeline_manager.py'deki tekrarlanan set_steps fonksiyonu kaldırılacak.
* Mimari sürdürülebilirlik ve test edilebilirlik güçlendiriliyor.

## Öğrenilenler ve İçgörüler

Yeni mimariyle birlikte, CLI argümanlarının da pipeline'a adım olarak eklenmesiyle kullanıcı esnekliği ve merkezi yönetim sağlanacak. Hata loglama ile veri kaybı şeffaf şekilde izlenebilecek.


Refactoring adımları tamamlandıktan sonra, pipeline özelleştirme ve hata loglama örnekleriyle kapsamlı dokümantasyon hazırlanacak. Bellek Bankası ve kod tabanı yeni mimariye göre güncellenecek.
- Kullanıcı ve geliştirici için pipeline özelleştirme ve modül ekleme/çıkarma örnekleriyle kapsamlı dokümantasyon hazırlanacak.