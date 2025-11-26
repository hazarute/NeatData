# Project Brief: NeatData

## Proje Tanımı
NeatData, dağınık CSV/Excel veri setlerini temizleyen, standardize eden ve analize hazır hale getiren profesyonel bir veri işleme platformudur.

**Çoklu Arayüz Stratejisi:**
1.  **Masaüstü (Desktop):** CustomTkinter ile yerel çalışan güvenli uygulama.
2.  **Web (SaaS):** Streamlit ve FastAPI ile çalışan, veritabanı destekli bulut çözümü.

## Temel Mimarisi
```

[Frontend: Streamlit] \<---\> [API: FastAPI] \<---\> [Core: PipelineManager] | [Database: SQLite]

```

## Temel Özellikler
- **Core Logic:** Modüler plugin mimarisi (Trim, Deduplicate, Standardize).
- **Veritabanı:** Yüklenen dosyaların ve işlem geçmişinin tutulduğu kalıcı hafıza.
- **API:** RESTful mimari, API Key güvenliği ve yapılandırılmış loglama.
- **Arayüzler:** Hem teknik olmayan kullanıcılar (GUI/Web) hem de geliştiriciler (API) için uygun.

## Proje Durumu
- **Faz 1-7 (Tamamlandı):** Core Logic, Desktop GUI, FastAPI Backend, Auth, Logging, WebSocket.
- **Faz 8 (Aktif):** Streamlit Web Arayüzü ve Veritabanı Odaklı İş Akışı entegrasyonu.
