import pandas as pd

def remove_duplicates_report(df):
    """DataFrame'deki tekrar eden satırları siler ve kaç satır silindiğini döndürür."""
    before = len(df)
    df_clean = df.drop_duplicates()
    after = len(df_clean)
    print(f"{before - after} tekrar eden satır silindi.")
    return df_clean, before - after
