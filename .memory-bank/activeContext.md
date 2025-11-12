# Aktif Bağlam (activeContext.md)

## Mevcut Çalışma Odağı
Mevcut odak: Pipeline ve modüler temizlik sistemi artık config dosyasından adım ve parametreleri dinamik olarak yükleyip çalıştırıyor. Tüm modüller (özellikle replace_error_values ve handle_missing_values) tam etki gösteriyor ve çıktı dosyalarında temizlik etkisi net şekilde gözüküyor. Mimari sürdürülebilir, genişletilebilir ve testlerle doğrulandı.

## Aktif Kararlar ve Gerekçeler
- PipelineManager artık config dosyasından adımları otomatik yüklüyor ve çalıştırıyor.
- Tüm temizlik modülleri process(df, **kwargs) arayüzüne sahip ve testlerle doğrulandı.
- replace_error_values ve handle_missing_values modülleri, tüm hata/eksik değerleri temizleyip dolduruyor.
- Pipeline adımları ve parametreleri config dosyasından dinamik olarak yönetiliyor.
- Kodun sürdürülebilirliği, test edilebilirliği ve özelleştirilebilirliği en üst seviyeye çıkarıldı.

## Öğrenilenler ve İçgörüler
- Modüler mimari ve config tabanlı pipeline, kodun bakımını ve test edilebilirliğini kolaylaştırır.
- PipelineManager ile temizlik akışı tamamen özelleştirilebilir ve merkezi olarak yönetilebilir.
- Her temizlik adımı bağımsız olarak geliştirilebilir, test edilebilir ve config ile parametre alabilir.
- Tüm hata/eksik değerler artık güvenilir şekilde temizleniyor ve dolduruluyor.


## Stratejik Sonraki Yön
- Bellek Bankası ve dokümantasyonu güncellendi.
- Kullanıcı ve geliştirici için pipeline özelleştirme ve modül ekleme/çıkarma örnekleriyle kapsamlı dokümantasyon hazırlanacak.