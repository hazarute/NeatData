# NeatData GUI Kullanım Kılavuzu

## Başlatma
- GUI'yi başlatmak için terminalde aşağıdaki komutu çalıştırın:
  ```bash
  python clean_data.py --gui
  ```
- Alternatif olarak doğrudan GUI dosyasını çalıştırabilirsiniz:
  ```bash
  python neatdata_gui.py
  ```

## Temel Özellikler
- **Dosya Seçimi:** 'Dosya Seç' butonuna tıklayarak temizlemek istediğiniz CSV dosyasını seçin.
- **Temizleme Seçenekleri:**
  - Eksik satırları silmek için 'Eksik Satırları Sil (--dropna)' kutusunu işaretleyin.
  - Eksik değerleri doldurmak için 'Eksik Değerleri Doldur (--fillna)' kutusunu işaretleyin ve doldurulacak değeri girin.
  - Metin standartlaştırmak için ilgili sütun adını girin.
- **Çıktı Ayarları:**
  - Çıktı formatını (Excel/CSV) seçin.
  - Çıktı dizinini belirleyin.
- **İlerleme ve Log:**
  - Temizleme işlemi sırasında ilerleme çubuğu ve log alanı güncellenir.
  - Hata ve işlem mesajları log alanında görüntülenir.
- **Başlat/Durdur:**
  - 'Temizlemeyi Başlat' ile işlemi başlatın.
  - 'Durdur' ile işlemi iptal edebilirsiniz.

## Notlar
- Tüm temizlik adımları arka planda PipelineManager ile yürütülür.
- Hem CLI hem GUI modunda çalışabilir.
- Büyük dosyalarda işlem süresi uzayabilir, ilerleme çubuğu ve log alanı ile takip edebilirsiniz.

## Gereksinimler
- Python 3.6+
- Gerekli paketler için `requirements.txt` dosyasını inceleyin ve kurulum yapın:
  ```bash
  pip install -r requirements.txt
  ```
- Tkinter Python ile birlikte gelir. PySimpleGUI opsiyoneldir.
