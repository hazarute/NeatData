

import pandas as pd
import argparse
import os
import chardet
import csv
# Modüller import

from modules.pipeline_manager import PipelineManager

def detect_encoding_and_delimiter(filename, sample_size=4096):
    with open(filename, 'rb') as f:
        raw = f.read(sample_size)
        result = chardet.detect(raw)
        encoding = result['encoding']
    with open(filename, 'r', encoding=encoding, errors='replace') as f:
        sample = f.read(sample_size)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            delimiter = dialect.delimiter
        except Exception:
            delimiter = ','
    return encoding, delimiter

    # ...existing code...
def read_data(filename, encoding=None, delimiter=None):
    ext = os.path.splitext(filename)[-1].lower()
    try:
        if ext == ".csv":
            # Otomatik encoding ve delimiter tespiti
            if encoding is None or delimiter is None:
                encoding_auto, delimiter_auto = detect_encoding_and_delimiter(filename)
                encoding = encoding or encoding_auto
                delimiter = delimiter or delimiter_auto
            df = pd.read_csv(filename, encoding=encoding, sep=delimiter, engine="python", on_bad_lines='skip')
            print(f"{filename} başarıyla okundu. Satır sayısı: {len(df)}")
            return df
        elif ext in [".xlsx", ".xlsm", ".xls"]:
            df = pd.read_excel(filename)
            print(f"{filename} başarıyla okundu. Satır sayısı: {len(df)}")
            return df
        else:
            print(f"Desteklenmeyen dosya formatı: {ext}")
            return None
    except Exception as e:
        print(f"Veri okuma hatası: {e}")
        return None

def print_report(rapor):
    print("\n--- Temizlik Raporu ---")
    print(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk','-')}")
    print(f"Tekrar eden satır silinen: {rapor.get('tekrar_silinen','-')}")
    print(f"Eksik değer nedeniyle silinen: {rapor.get('eksik_silinen','-')}")
    print(f"Son satır sayısı: {rapor.get('satir_sayisi_son','-')}")
    print("----------------------\n")

# Pipeline adımları listesi

# PipelineManager ile merkezi pipeline yönetimi
def temizlik_pipeline(df, args, rapor):
    config_path = "modules/pipeline_config.toml"
    manager = PipelineManager(config_path=config_path)
    # Parametreleri pipeline adımlarına ekle
    # Örnek: args.textcol, args.dropna, args.fillna gibi argümanlar config ile birleştirilebilir
    # Şimdilik config dosyasındaki adımlar çalıştırılır
    df = manager.run(df)
    # Tekrar silinen satır sayısı
    # remove_duplicates_report modülü artık process arayüzüne sahip
    tekrar_silinen = None
    try:
        from modules.remove_duplicates_report import process as remove_duplicates_process
        before = len(df)
        df = remove_duplicates_process(df)
        tekrar_silinen = before - len(df)
    except Exception:
        tekrar_silinen = "-"
    rapor['tekrar_silinen'] = tekrar_silinen
    # Eksik değerleri yönet
    eksik_silinen = 0
    if args.dropna:
        before = len(df)
        from modules.handle_missing_values import process as handle_missing_process
        df = handle_missing_process(df, method="drop")
        eksik_silinen = before - len(df)
    elif args.fillna is not None:
        from modules.handle_missing_values import process as handle_missing_process
        df = handle_missing_process(df, method="fill", fill_value=args.fillna)
    rapor['eksik_silinen'] = eksik_silinen
    # Metin standartlaştırma
    if args.textcol:
        from modules.standardize_text_column import process as standardize_text_process
        df = standardize_text_process(df, column=args.textcol)
    return df

def main():
    parser = argparse.ArgumentParser(description="NeatData - CSV Veri Temizleyici")
    parser.add_argument("--input", type=str, nargs='+', required=True, help="Bir veya birden fazla girdi CSV dosya yolu")
    parser.add_argument("--output", type=str, default=None, help="Çıktı dosya adı (xlsx/csv). Çoklu dosyada otomatik adlandırılır.")
    parser.add_argument("--dropna", action="store_true", help="Eksik değerleri sil (varsayılan: doldurma yok)")
    parser.add_argument("--fillna", type=str, default=None, help="Eksik değerleri bu değerle doldur")
    parser.add_argument("--textcol", type=str, default=None, help="Metin standartlaştırılacak sütun adı")
    args = parser.parse_args()

    for input_file in args.input:
        print(f"\n--- {input_file} dosyası işleniyor ---")
        df = read_data(input_file)
        if df is not None:
            rapor = {}
            rapor['dosya'] = input_file
            rapor['satir_sayisi_ilk'] = len(df)
            df = temizlik_pipeline(df, args, rapor)
            # Çıktı dosya adı belirle
            input_base = os.path.splitext(os.path.basename(input_file))[0].replace(' ', '_')
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
                from modules.save_to_excel import process as save_to_excel_process
                save_to_excel_process(df, output_file=output_file)
            elif output_file.endswith(".csv"):
                df.to_csv(output_file, index=False)
                print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")
            else:
                print("Desteklenmeyen çıktı formatı. Sadece .xlsx veya .csv kullanın.")
            rapor['satir_sayisi_son'] = len(df)
            print_report(rapor)
        else:
            print(f"{input_file} dosyası yüklenemedi.")

if __name__ == "__main__":
    main()
