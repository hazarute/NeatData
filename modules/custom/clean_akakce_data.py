import pandas as pd
import re

META = {
    "key": "clean_akakce_data",
    "name": "Akakçe Verisi Temizleme",
    "description": "Akakçe'den çekilen verilerde fiyat ve ürün isimlerini temizler.",
    "defaults": {}
}

def process(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    df_copy = df.copy()

    # Fiyat sütunundaki '+116 FİYAT' gibi ifadeleri temizle
    df_copy['price'] = df_copy['price'].apply(lambda x: re.sub(r'\+\d+\s*FİYAT', '', x).strip())

    # 'name' sütununu 'marka' ve 'model' olarak ayır
    def split_name(name):
        parts = name.split(' ', 1)  # İlk boşluğa göre böl
        if len(parts) == 2:
            return pd.Series({"brand": parts[0], "model": parts[1]})
        return pd.Series({"brand": name, "model": None})

    name_split = df_copy['name'].apply(split_name)
    df_copy = pd.concat([df_copy, name_split], axis=1)

    # 'name' sütununu kaldır
    df_copy.drop(columns=['name'], inplace=True)

    return df_copy