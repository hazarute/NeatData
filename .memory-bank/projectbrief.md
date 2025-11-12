# Proje Özeti (projectbrief.md)

## Proje Adı
NeatData - CSV Data Cleaner

## Amaç
Karmaşık ve dağınık CSV dosyalarını hızlı, kolay ve güvenilir şekilde temizleyip, standartlaştırılmış ve analiz için hazır hale getirmek. Temizlenen veriler, iyi biçimlendirilmiş bir Excel dosyasına aktarılır. Yeni sürümde, hem komut satırı hem de basit bir grafik arayüz (GUI) ile kullanılabilirlik sağlanacaktır.

## Modülerlik Hedefi
Proje, tüm temizlik adımlarının ayrı modüller/fonksiyonlar olarak organize edildiği, genişletilebilir ve özelleştirilebilir bir mimariye sahip olmalıdır. Pipeline yönetimi merkezi bir yapı (pipeline_manager.py) üzerinden yapılacak, kullanıcı ve geliştirici pipeline’ı config dosyası veya arayüz ile kolayca değiştirebilecek. Yeni modüller eklenebilecek, adımların sırası ve parametreleri dinamik olarak yönetilebilecek. GUI entegrasyonu ile dosya seçimi, temizlik seçenekleri ve çıktı ayarları görsel olarak sunulacak.

## Kapsam
- Komut satırı arayüzü ve basit GUI ile çalışır.
- Farklı ayraç ve encoding ile gelen CSV dosyalarını otomatik algılar ve işler.
- Sütun adlarını ve veri tiplerini normalize eder.
- Eksik/hatalı değerleri (ERROR, UNKNOWN, boşluk, NaN) standart şekilde yönetir.
- Kullanıcıdan parametre alarak esnek temizlik akışı sunar.
- Çoklu veri seti ve farklı formatlar için yeniden kullanılabilir temizlik modülleri içerir.
- Temizlenmiş veriyi Excel veya CSV olarak kaydeder, temizlik raporu üretir.
- GUI ile dosya seçimi, temizlik seçenekleri, ilerleme ve çıktı yönetimi kolaylaştırılır.

## Temel Gereksinimler
- Python 3.6+
- pandas
- openpyxl
- (GUI için) Tkinter veya PySimpleGUI

## Nihai Hedef
Kullanıcıların farklı kaynaklardan gelen bozuk/dağınık CSV dosyalarını otomatik ve esnek şekilde temizleyip, analiz için hazır ve tutarlı veri setleri elde etmelerini sağlamak. Proje büyüdükçe pipeline yönetimi, hata yönetimi, loglama ve modül ekleme/çıkarma merkezi olarak yönetilecek. GUI ile teknik bilgisi olmayan kullanıcılar için erişilebilirlik ve kullanım kolaylığı artırılacak.