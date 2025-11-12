

## Yapılacaklar (TO-DO)


## Tamamlananlar (DONE)
[X] Hafif ve kolay entegre edilebilen bir GUI kütüphanesi seçildi (Tkinter)
[X] GUI tasarımı ve temel bileşenler planlandı
[X] PipelineManager ile tam uyumlu, modüler bir GUI geliştirildi
[X] Ana script hem CLI hem GUI modunda çalışacak şekilde güncellendi
[X] Ek paketler requirements.txt'ye eklendi
[X] GUI için basit dokümantasyon hazırlandı (docs/neatdata_gui_kullanim.md)

[X] Uygulama test edildi: dirty_cafe_sales.csv, messy_HR_data.csv, messy_IMDB_dataset.csv ve diğer dosyalar başarıyla işlendi. Tüm hata/eksik/boş değerler (ERROR, UNKNOWN, N/A, null, -, ?, boşluk) güvenilir şekilde temizlenip 'TEMIZ' ile dolduruldu. Temizlik raporları ve çıktı dosyaları incelendi, sonuçlar başarılı.


## Tamamlananlar (DONE)
[X] Temel script dosyasını (clean_data.py) oluştur
[X] CSV okuma fonksiyonunu yaz
[X] Tekrarlanan satırları silen fonksiyonu ekle
[X] Eksik değerleri yöneten fonksiyonu ekle
[X] Metin standartlaştırma fonksiyonu ekle
[X] Excel'e çıktı alma fonksiyonu ekle
[X] Otomatik ayraç ve encoding tespiti modülünü ekle
[X] Sütun adlarını normalize eden fonksiyonu yaz
[X] Veri tiplerini otomatik algılayan ve düzelten fonksiyonu ekle
[X] Eksik/hatalı değerleri (ERROR, UNKNOWN, boşluk, NaN) standart şekilde yöneten fonksiyonu ekle
[X] Kullanıcıdan parametre alma ve temizlik seçeneklerini belirleme akışını ekle
[X] Temizlik raporu üreten fonksiyonu ekle
[X] Çoklu dosya ve farklı veri setleri için esnek temizlik akışı oluştur
[X] Bellek Bankası ve dokümantasyonu yeni mimariye göre güncelle
[X] pipeline_manager.py dosyasını geliştirerek merkezi pipeline yönetimi sağla
[X] Pipeline adımlarını config dosyası veya arayüz ile dinamik olarak yönet
[X] Hata yönetimi ve loglama desteği ekle
[X] Modül arayüzü (process(df, **kwargs)) standardını uygula
[X] Uygulama test edildi ve tüm dosyalar başarıyla işlendi. Temizlik raporları ve çıktı dosyaları oluşturuldu.


## Bilinen Sorunlar (BUGS)

## Bilinen Sorunlar (BUGS)

## Tamamlananlar (DONE)

## Bilinen Sorunlar (BUGS)

[ ] Hibrit pipeline yapısını kaldır, tüm akışı PipelineManager üzerinden yönet.
[ ] CLI argümanlarını PipelineManager'a adım olarak ekle.
[ ] pipeline_manager.py dosyasındaki tekrarlanan set_steps fonksiyonunu sil.
[ ] read_data fonksiyonunda atlanan satırları bad_lines.csv dosyasına logla.
