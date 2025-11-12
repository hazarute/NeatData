
import pandas as pd
import openpyxl
import chardet
import csv
import argparse

# Temel script yapısı

def main():
    parser = argparse.ArgumentParser(description="NeatData - CSV Veri Temizleyici")
    parser.add_argument("--input", type=str, nargs='+', required=True, help="Bir veya birden fazla girdi CSV dosya yolu")
    parser.add_argument("--output", type=str, default=None, help="Çıktı dosya adı (xlsx/csv). Çoklu dosyada otomatik adlandırılır.")
    parser.add_argument("--dropna", action="store_true", help="Eksik değerleri sil (varsayılan: doldurma yok)")
    parser.add_argument("--fillna", type=str, default=None, help="Eksik değerleri bu değerle doldur")
    parser.add_argument("--textcol", type=str, default=None, help="Metin standartlaştırılacak sütun adı")
    args = parser.parse_args()

    import os
    for input_csv in args.input:
        print(f"\n--- {input_csv} dosyası işleniyor ---")
        encoding, delimiter = detect_encoding_and_delimiter(input_csv)
        print(f"Tespit edilen encoding: {encoding}, delimiter: {delimiter}")
        df = read_csv(input_csv, encoding=encoding, delimiter=delimiter)
        if df is not None:
            rapor = {}
            rapor['dosya'] = input_csv
            rapor['satir_sayisi_ilk'] = len(df)
            df = temizlik_pipeline(df, args, rapor)
            # Çıktı dosya adı belirle
            input_base = os.path.splitext(os.path.basename(input_csv))[0].replace(' ', '_')
            if args.output:
                ext = args.output.split('.')[-1]
                base = args.output[:-(len(ext)+1)] if len(args.output.split('.')) > 1 else args.output
                if len(args.input) > 1:
                    output_file = f"{base}_{input_base}.{ext}"
                else:
                    output_file = args.output
            else:
                output_file = f"cleaned_{input_base}.xlsx"
            # Çıktı al
            if output_file.endswith(".xlsx"):
                save_to_excel(df, output_file=output_file)
            elif output_file.endswith(".csv"):
                df.to_csv(output_file, index=False)
                print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")
            else:
                print("Desteklenmeyen çıktı formatı. Sadece .xlsx veya .csv kullanın.")
            rapor['satir_sayisi_son'] = len(df)
            print_report(rapor)
        else:
            print(f"{input_csv} dosyası yüklenemedi.")

# Esnek temizlik pipeline fonksiyonu
def temizlik_pipeline(df, args, rapor):
    df = normalize_column_names(df)
    df = replace_error_values(df)
    df = auto_convert_types(df)
    df, tekrar_silinen = remove_duplicates_report(df)
    rapor['tekrar_silinen'] = tekrar_silinen
    # Eksik değerleri yönet
    eksik_silinen = 0
    if args.dropna:
        before = len(df)
        df = handle_missing_values(df, method="drop")
        eksik_silinen = before - len(df)
    elif args.fillna is not None:
        df = handle_missing_values(df, method="fill", fill_value=args.fillna)
    rapor['eksik_silinen'] = eksik_silinen
    # Metin standartlaştırma
    if args.textcol:
        df = standardize_text_column(df, column=args.textcol)
    return df

def print_report(rapor):
    print("\n--- Temizlik Raporu ---")
    print(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk','-')}")
    print(f"Tekrar eden satır silinen: {rapor.get('tekrar_silinen','-')}")
    print(f"Eksik değer nedeniyle silinen: {rapor.get('eksik_silinen','-')}")
    print(f"Son satır sayısı: {rapor.get('satir_sayisi_son','-')}")
    print("----------------------\n")
# Eksik fonksiyonlar
def replace_error_values(df):
    """ERROR, UNKNOWN, boşluk, NaN gibi değerleri standart NaN'a çevirir."""
    error_values = ["ERROR", "UNKNOWN", "", " ", "NAN", "NaN", None]
    df = df.replace(error_values, pd.NA)
    print("Hatalı/eksik değerler standart NaN olarak işaretlendi.")
    return df

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

def normalize_column_names(df):
    """Sütun adlarını küçük harfe çevirir, boşluk ve özel karakterleri alt çizgiye dönüştürür."""
    import re
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

def save_to_excel(df, output_file="clean_data.xlsx"):
    """DataFrame'i Excel dosyasına kaydeder."""
    try:
        df.to_excel(output_file, index=False)
        print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Excel'e kaydetme hatası: {e}")

def standardize_text_column(df, column):
    """Belirtilen sütundaki tüm metinleri küçük harfe çevirir."""
    if column in df.columns:
        df[column] = df[column].astype(str).str.lower()
        print(f"'{column}' sütunundaki metinler küçük harfe çevrildi.")
    else:
        print(f"Uyarı: '{column}' sütunu bulunamadı.")
    return df

def handle_missing_values(df, method="drop", fill_value=None):
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
        df_filled = df.fillna(fill_value)
        print(f"Eksik değerler '{fill_value}' ile dolduruldu.")
        return df_filled
    else:
        print("Geçersiz method. 'drop' veya 'fill' olmalı.")
        return df


def remove_duplicates_report(df):
    """DataFrame'deki tekrar eden satırları siler ve kaç satır silindiğini döndürür."""
    before = len(df)
    df_clean = df.drop_duplicates()
    after = len(df_clean)
    print(f"{before - after} tekrar eden satır silindi.")
    return df_clean, before - after


def read_csv(filename, encoding=None, delimiter=None):
    """CSV dosyasını okur ve DataFrame döndürür."""
    try:
        df = pd.read_csv(filename, encoding=encoding, sep=delimiter)
        print(f"{filename} başarıyla okundu. Satır sayısı: {len(df)}")
        return df
    except Exception as e:
        print(f"CSV okuma hatası: {e}")
        return None

def detect_encoding_and_delimiter(filename, sample_size=4096):
    """Dosyanın encoding ve delimiter bilgisini otomatik tespit eder."""
    # Encoding tespiti
    with open(filename, 'rb') as f:
        raw = f.read(sample_size)
        result = chardet.detect(raw)
        encoding = result['encoding']
    # Delimiter tespiti
    with open(filename, 'r', encoding=encoding, errors='replace') as f:
        sample = f.read(sample_size)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter
        except Exception:
            delimiter = ','  # Varsayılan olarak virgül
    return encoding, delimiter

if __name__ == "__main__":
    main()
