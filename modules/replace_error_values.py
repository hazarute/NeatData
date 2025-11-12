import pandas as pd

def replace_error_values(df):
    """ERROR, UNKNOWN, boşluk, NaN gibi değerleri standart NaN'a çevirir."""
    error_values = ["ERROR", "UNKNOWN", "", " ", "NAN", "NaN", None]
    df = df.replace(error_values, pd.NA)
    print("Hatalı/eksik değerler standart NaN olarak işaretlendi.")
    return df
