# Proje Özeti (projectbrief.md)

## Proje Adı
NeatData - CSV Data Cleaner

## Amaç
Karmaşık ve dağınık CSV dosyalarını hızlı, kolay ve güvenilir şekilde temizleyip, standartlaştırılmış ve analiz için hazır hale getirmek. Temizlenen veriler, iyi biçimlendirilmiş bir Excel dosyasına aktarılır. Yeni sürümde, hem komut satırı hem de modern bir grafik arayüz (CustomTkinter tabanlı GUI) ile kullanılabilirlik sağlanacaktır.

## Modülerlik ve Modernleşme Hedefi
Proje, temizlik akışını iki katmanda ele alacak şekilde yeniden tasarlandı:

1. **Core (Çekirdek) Katmanı:** `modules/core/` altında standart veri temizlik görevleri (başlık standartlaştırma, tekrar silme, eksik değer yönetimi, boşluk kırpma, veri tipi düzeltme) tekil modüller halinde tutulur. Her modül `META` ve `process` arayüzünü uygular.
2. **Custom (Özel) Katmanı:** `modules/custom/` klasörüne bırakılan her Python dosyası otomatik olarak plugin olarak yüklenir. PipelineManager bu klasörü tarar, yeni dosyaları dinamik olarak içeri alır ve GUI’de seçim yapılabilir hale getirir.

Pipeline yönetimi merkezi `PipelineManager` sınıfı üzerinden yapılır; config dosyası yerine kullanıcı seçimleri (CLI/GUI) pipeline’ı belirler. Yeni modüller eklendiğinde yalnızca ilgili klasöre dosya koymak yeterli olur; sistem parametreleri ve sıralamayı dinamik olarak yönetir.

Son strateji: GUI, CustomTkinter ile modernleştirilmiş iki panelli bir tasarıma sahip olacak. Sol panelde Core modüller için sabit Switch bileşenleri bulunacak, sağ panel ise custom plugin’leri tarayıp ScrollableFrame üzerinde otomatik CheckBox oluşturacak. Arayüz koyu tema, modern kontroller, log ve ilerleme alanı ile UX’e odaklanır.

## Kapsam
- Komut satırı arayüzü ve modern CustomTkinter tabanlı GUI ile çalışır.
- Farklı ayraç ve encoding ile gelen CSV dosyalarını otomatik algılar ve işler.
- Sütun adlarını ve veri tiplerini normalize eder.
- Eksik/hatalı değerleri (ERROR, UNKNOWN, boşluk, NaN) standart şekilde yönetir.
- Kullanıcıdan parametre alarak esnek temizlik akışı sunar.
- Çoklu veri seti ve farklı formatlar için yeniden kullanılabilir temizlik modülleri içerir.
- Temizlenmiş veriyi Excel veya CSV olarak kaydeder, temizlik raporu üretir.
- Modern GUI ile dosya seçimi, temizlik seçenekleri, ilerleme ve çıktı yönetimi kolaylaştırılır. Koyu tema, modern kontroller ve log alanı ile UX iyileştirilir.
- HR veri setleri için özel temizlik modülleri (maaş para birimi, telefon formatı, tarih standardizasyonu, metin düzeltmeleri) eklenecek.

## Temel Gereksinimler
- Python 3.6+
- pandas
- openpyxl
- customtkinter (modern GUI için)

## Nihai Hedef
Kullanıcıların farklı kaynaklardan gelen bozuk/dağınık CSV dosyalarını otomatik ve esnek şekilde temizleyip, analiz için hazır ve tutarlı veri setleri elde etmelerini sağlamak. Proje büyüdükçe pipeline yönetimi, hata yönetimi, loglama ve modül ekleme/çıkarma merkezi olarak yönetilecek. Modern CustomTkinter GUI ile teknik bilgisi olmayan kullanıcılar için erişilebilirlik, görsel kalite ve kullanım kolaylığı en üst düzeye çıkarılacak. Sektör spesifik veri temizleme desteği (örneğin HR verileri) ile genişletilebilirlik sağlanacak.