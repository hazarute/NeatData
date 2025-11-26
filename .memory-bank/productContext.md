# Ürün Bağlamı (Product Context)

## Problemi Tanımı
Kullanıcılar dağınık verilerini temizlemek için teknik bilgi gerektirmeyen, hızlı ve güvenilir bir araca ihtiyaç duyarlar.

## Çözüm: NeatData Web (Streamlit)
Kullanıcının herhangi bir kurulum yapmadan (Web üzerinden) verisini temizleyebileceği platform.

## Kullanıcı Akışı (User Journey)
1.  **Giriş:** Kullanıcı Streamlit sayfasını açar.
2.  **Yükleme:** "Dosya Seç" butonuna basar ve CSV yükler.
    * *Sistem:* Dosyayı sunucuya yükler, veritabanına kaydeder, ID oluşturur.
3.  **Konfigürasyon:** Hangi temizlik işlemlerinin yapılacağını seçer (Trim, Deduplicate vb.).
4.  **İşlem:** "Temizle" butonuna basar.
    * *Sistem:* ID ve Ayarları API'ye gönderir. API işlemi yapar.
5.  **Sonuç:** Temizlenmiş veri ekranda tablo olarak belirir.
6.  **Çıktı:** Kullanıcı "İndir" butonuyla temiz dosyayı alır.

## Hedef Kitle
- Veri Analistleri
- E-ticaret Yöneticileri (Ürün listesi temizliği)
- CRM Yöneticileri (Müşteri listesi temizliği)