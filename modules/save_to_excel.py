import pandas as pd

def save_to_excel(df, output_file="clean_data.xlsx"):
    """DataFrame'i Excel dosyasına kaydeder."""
    try:
        df.to_excel(output_file, index=False)
        print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Excel'e kaydetme hatası: {e}")
