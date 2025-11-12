import re
import pandas as pd

def normalize_column_names(df):
    """Sütun adlarını küçük harfe çevirir, boşluk ve özel karakterleri alt çizgiye dönüştürür."""
    new_columns = []
    for col in df.columns:
        col_new = col.strip().lower()
        col_new = re.sub(r"[^a-z0-9]+", "_", col_new)
        col_new = re.sub(r"_+", "_", col_new)
        col_new = col_new.strip('_')
        new_columns.append(col_new)
    df.columns = new_columns
    print(f"Sütun adları normalize edildi: {df.columns.tolist()}")
    return df
