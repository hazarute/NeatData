import pandas as pd


def process(df, method="drop", fill_value=None, **kwargs):
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
        import numpy as np
        error_values = ["ERROR", "UNKNOWN", "N/A", "null", "NAN", "NaN", "-", "?", "", " ", None]
        error_values_lower = set([str(e).strip().lower() for e in error_values if e is not None])
        filled_count = 0
        def fill_cell(val):
            sval = str(val).strip().lower() if not pd.isna(val) else ""
            if pd.isna(val) or sval in error_values_lower or sval == "":
                nonlocal filled_count
                filled_count += 1
                return fill_value
            return val
        df_filled = df.applymap(fill_cell)
        print(f"handle_missing_values: {filled_count} hücre '{fill_value}' ile dolduruldu. Parametreler: {error_values}")
        return df_filled
    else:
        print("Geçersiz method. 'drop' veya 'fill' olmalı.")
        return df
