# Pipeline ve Modül Özelleştirme Rehberi

Bu dosya, NeatData projesinde temizlik pipeline'ını ve modülleri nasıl özelleştireceğinizi, yeni modül ekleme/çıkarma işlemlerini ve örnek yapılandırmaları açıklar.

## 1. Pipeline Nedir?
Temizlik pipeline'ı, veri temizleme adımlarının sıralı şekilde uygulanmasını sağlayan bir akıştır. Her adım ayrı bir modül olarak `modules/` klasöründe yer alır.

## 2. Modül Ekleme
Yeni bir temizlik adımı eklemek için:
1. `modules/` klasöründe yeni bir Python dosyası oluşturun. Örnek:
    ```python
    # modules/custom_cleaner.py
    def custom_cleaner(df):
        # Temizlik işlemleri
        return df
    ```
2. Ana scriptte (clean_data.py) pipeline listesine bu modülü ekleyin:
    ```python
    from modules import custom_cleaner
    pipeline = [normalize_column_names, custom_cleaner, ...]
    ```

## 3. Modül Çıkarma veya Sıra Değiştirme
- Bir adımı çıkarmak için pipeline listesinden ilgili modülü silin.
- Sıra değiştirmek için pipeline listesindeki modüllerin sırasını değiştirin.

## 4. Pipeline Özelleştirme Örneği
```python
from modules import normalize_column_names, auto_convert_types, custom_cleaner
pipeline = [normalize_column_names, custom_cleaner, auto_convert_types]
```

## 5. Parametreli Modül Kullanımı
Bazı modüller ek parametre alabilir. Örneğin:
```python
from modules import standardize_text_column
pipeline = [lambda df: standardize_text_column(df, column='isim')]
```

## 6. Sık Sorulan Sorular
- **Yeni modül ekledim, neden çalışmıyor?**
  - Modülün adını pipeline listesine eklediğinizden ve fonksiyonun doğru şekilde tanımlandığından emin olun.
- **Pipeline sırasını değiştirdim, sonuçlar farklı oldu.**
  - Temizlik adımlarının sırası veri üzerinde farklı etki yaratabilir. Deneyerek en iyi akışı bulabilirsiniz.

## 7. Daha Fazla Bilgi
- Kod örnekleri ve güncel pipeline yapısı için `clean_data.py` dosyasını inceleyin.
- Geliştirici dokümantasyonu için ReadMe.md ve Memory Bank dosyalarına bakın.

---
Her türlü özelleştirme ve modül ekleme/çıkarma işlemi için bu rehberi kullanabilirsiniz. Sorularınız için proje sahibine ulaşabilirsiniz.
