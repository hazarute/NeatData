import pandas as pd

def process(df, **kwargs):
    """Tüm hücreleri stringe çevirir."""
    return df.applymap(lambda x: str(x) if not pd.isna(x) else x)
