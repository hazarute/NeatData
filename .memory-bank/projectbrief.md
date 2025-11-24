# Project Brief: NeatData

## Vizyon
NeatData, veri temizleme süreçlerini **Masaüstü (GUI) ve Web Servisi (API) olmak üzere iki interface** üzerinden sunan, modüler ve genişletilebilir bir uygulamadır. **Sistemlerin birbiriyle konuşması (Interoperability)** temel amacıdır. 

Dağınık CSV/Excel verilerini temizlemek için hem hazır "Çekirdek" (Core) araçları hem de kullanıcıların kendi Python scriptlerini ekleyebileceği "Plugin" (Eklenti) mimarisi sağlar. Tüm işler bir **PipelineManager** tarafından yönetilir; GUI veya REST API aracılığıyla tetiklenebilir.

## Temel Hedefler
1.  **Modülerlik:** GUI, API, İş Mantığı ve I/O işlemlerinin birbirinden tamamen ayrılması.
2.  **Genişletilebilirlik:** `modules/custom/` klasörüne atılan her Python dosyasının otomatik olarak sisteme dahil edilmesi.
3.  **Çoklu Interface:** 
    * Masaüstü uygulaması (CustomTkinter GUI) → Teknik olmayan kullanıcılar için.
    * REST API (FastAPI) → Diğer sistemlerin NeatData'yı entegre edebilmesi için.
4.  **Güvenilirlik:** Hatalı veri okuma (delimiter sorunları) ve veri kaybı (yanlış dropna) gibi durumların önüne geçen sağlam bir altyapı.