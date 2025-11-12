import pandas as pd


def process(df, **kwargs):
    """DataFrame'deki tekrar eden satırları siler ve kaç satır silindiğini döndürür."""
    before = len(df)
    df_clean = df.drop_duplicates()
    after = len(df_clean)
    print(f"{before - after} tekrar eden satır silindi.")
    # Sadece temizlenmiş DataFrame döndürülür
    return df_clean
