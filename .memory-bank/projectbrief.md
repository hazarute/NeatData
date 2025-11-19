# Project Brief: NeatData

## Vizyon
NeatData, veri temizleme süreçlerini standartlaştıran ancak özel iş mantıklarına (Business Logic) izin veren, modüler ve genişletilebilir bir masaüstü uygulamasıdır. Dağınık CSV/Excel verilerini temizlemek için hem hazır "Çekirdek" (Core) araçları sunar hem de kullanıcıların kendi Python scriptlerini sürükle-bırak mantığıyla ekleyebileceği bir "Plugin" (Eklenti) mimarisi sağlar.

## Temel Hedefler
1.  **Modülerlik:** GUI, İş Mantığı ve I/O işlemlerinin birbirinden tamamen ayrılması.
2.  **Genişletilebilirlik:** `modules/custom/` klasörüne atılan her Python dosyasının otomatik olarak sisteme dahil edilmesi.
3.  **Kullanıcı Dostu:** Teknik olmayan kullanıcılar için modern (CustomTkinter) bir arayüz.
4.  **Güvenilirlik:** Hatalı veri okuma (delimiter sorunları) ve veri kaybı (yanlış dropna) gibi durumların önüne geçen sağlam bir altyapı.