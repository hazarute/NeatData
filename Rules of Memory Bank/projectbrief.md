# Proje Özeti (projectbrief.md)

## Proje Adı
NeatData - CSV Data Cleaner

## Amaç
Karmaşık ve dağınık CSV dosyalarını hızlı, kolay ve güvenilir şekilde temizleyip, standartlaştırılmış ve analiz için hazır hale getirmek. Temizlenen veriler, iyi biçimlendirilmiş bir Excel dosyasına aktarılır.

## Modülerlik Hedefi
Proje, tüm temizlik adımlarının ayrı modüller/fonksiyonlar olarak organize edildiği, genişletilebilir ve özelleştirilebilir bir mimariye sahip olmalıdır. Kullanıcı, temizlik pipeline’ına istediği adımları ekleyip çıkarabilir, yeni modüller ekleyebilir.

## Kapsam
- Komut satırı arayüzü ile çalışır.
- Farklı ayraç ve encoding ile gelen CSV dosyalarını otomatik algılar ve işler.
- Sütun adlarını ve veri tiplerini normalize eder.
- Eksik/hatalı değerleri (ERROR, UNKNOWN, boşluk, NaN) standart şekilde yönetir.
- Kullanıcıdan parametre alarak esnek temizlik akışı sunar.
- Çoklu veri seti ve farklı formatlar için yeniden kullanılabilir temizlik modülleri içerir.
- Temizlenmiş veriyi Excel veya CSV olarak kaydeder, temizlik raporu üretir.

## Temel Gereksinimler
- Python 3.6+
- pandas
- openpyxl

## Nihai Hedef
Kullanıcıların farklı kaynaklardan gelen bozuk/dağınık CSV dosyalarını otomatik ve esnek şekilde temizleyip, analiz için hazır ve tutarlı veri setleri elde etmelerini sağlamak.