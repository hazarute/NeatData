import pandas as pd

def handle_missing_values(df, method="drop", fill_value=None):
    """Eksik (NaN) değerleri siler veya doldurur.
    method: 'drop' veya 'fill'
    fill_value: doldurma için kullanılacak değer (method='fill' ise)
    """
    if method == "drop":
        before = len(df)
        df_clean = df.dropna()
        after = len(df_clean)
        print(f"{before - after} satır eksik değer nedeniyle silindi.")
        return df_clean
    elif method == "fill":
        df_filled = df.fillna(fill_value)
        print(f"Eksik değerler '{fill_value}' ile dolduruldu.")
        return df_filled
    else:
        print("Geçersiz method. 'drop' veya 'fill' olmalı.")
        return df
