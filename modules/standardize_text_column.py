import pandas as pd

def standardize_text_column(df, column):
    """Belirtilen sütundaki tüm metinleri küçük harfe çevirir."""
    if column in df.columns:
        df[column] = df[column].astype(str).str.lower()
        print(f"'{column}' sütunundaki metinler küçük harfe çevrildi.")
    else:
        print(f"Uyarı: '{column}' sütunu bulunamadı.")
    return df
