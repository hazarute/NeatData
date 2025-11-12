import pandas as pd


def process(df, error_values=None, **kwargs):
    """ERROR, UNKNOWN, boşluk, NaN gibi değerleri standart NaN'a çevirir."""
    if error_values is None:
        error_values = ["ERROR", "UNKNOWN", "N/A", "null", "NAN", "NaN", "-", "?", "", " ", None]
    error_values_lower = set([str(e).strip().lower() for e in error_values if e is not None])
    cleaned_count = 0
    def clean_cell(val):
        sval = str(val).strip().lower() if not pd.isna(val) else ""
        if sval in error_values_lower or sval == "" or pd.isna(val):
            nonlocal cleaned_count
            cleaned_count += 1
            return pd.NA
        return val
    df = df.applymap(clean_cell)
    print(f"replace_error_values: {cleaned_count} hücre NaN olarak işaretlendi. Parametreler: {error_values}")
    return df
