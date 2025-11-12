import pandas as pd


def process(df, output_file="clean_data.xlsx", **kwargs):
    """DataFrame'i Excel dosyasına kaydeder."""
    try:
        df.to_excel(output_file, index=False)
        print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Excel'e kaydetme hatası: {e}")
    return df
