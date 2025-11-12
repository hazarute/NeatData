import pandas as pd

def auto_convert_types(df):
    """Sütunların veri tiplerini otomatik algılar ve dönüştürür."""
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"{col} sütunu sayısal olarak algılandı.")
        except Exception:
            pass
    return df
