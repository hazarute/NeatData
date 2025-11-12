import pandas as pd


def process(df, column=None, **kwargs):
    """Belirtilen sütundaki tüm metinleri küçük harfe çevirir."""
    if column and column in df.columns:
        df[column] = df[column].astype(str).str.lower()
        print(f"'{column}' sütunundaki metinler küçük harfe çevrildi.")
    elif column:
        print(f"Uyarı: '{column}' sütunu bulunamadı.")
    return df
