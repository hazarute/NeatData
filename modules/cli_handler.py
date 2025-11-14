import argparse
from pathlib import Path
from typing import Dict, List, Optional

from modules.data_loader import DataLoader
from modules.pipeline_manager import PipelineManager
from modules.report_generator import print_report


def _parse_list_argument(value: Optional[str], *, default_behavior: str) -> Optional[List[str]]:
    if not value:
        return None if default_behavior == "all" else []
    lowered = value.lower()
    if lowered == "all":
        return None
    if lowered == "none":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _build_overrides(args) -> Dict[str, Dict]:
    overrides: Dict[str, Dict] = {}
    if args.handle_missing_strategy or args.handle_missing_fill is not None:
        overrides["handle_missing"] = {}
        if args.handle_missing_strategy:
            overrides["handle_missing"]["strategy"] = args.handle_missing_strategy
        if args.handle_missing_fill is not None:
            overrides["handle_missing"]["fill_value"] = args.handle_missing_fill
    if args.convert_columns:
        overrides["convert_types"] = {"columns": [col.strip() for col in args.convert_columns.split(",") if col.strip()]}
    return overrides


def run_pipeline_for_file(input_file: str, args, manager: PipelineManager, loader: DataLoader, *, multi_input: bool) -> None:
    try:
        df = loader.load(input_file)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Dosya yüklenemedi ({input_file}): {exc}")
        return
    report_payload = {"dosya": input_file, "satir_sayisi_ilk": len(df)}
    overrides = _build_overrides(args)
    if "handle_missing" in overrides:
        report_payload["eksik_silinen"] = overrides["handle_missing"].get("strategy", "custom")
    else:
        report_payload["eksik_silinen"] = "varsayılan"

    core_keys = _parse_list_argument(args.core_modules, default_behavior="all")
    custom_keys = _parse_list_argument(args.custom_modules, default_behavior="none")
    if custom_keys is None and args.custom_modules:
        custom_keys = list(manager.available_custom_modules().keys()) or []

    manager.build_pipeline(
        core_keys=core_keys,
        custom_keys=custom_keys,
        param_overrides=overrides,
    )

    cleaned_df = manager.run(df)
    report_payload["satir_sayisi_son"] = len(cleaned_df)
    report_payload["tekrar_silinen"] = report_payload["satir_sayisi_ilk"] - len(cleaned_df)
    output_path = _resolve_output_path(input_file, args.output, multi_input)

    if output_path.suffix.lower() == ".xlsx":
        from modules.save_to_excel import process as save_to_excel_process

        save_to_excel_process(cleaned_df, output_file=str(output_path))
    elif output_path.suffix.lower() == ".csv":
        # Save CSV using BOM to keep headers/columns consistent when opened in Excel
        cleaned_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    else:
        raise ValueError("Çıktı sadece .xlsx veya .csv olabilir")

    print(f"Temizlenmiş veri '{output_path}' dosyasına kaydedildi.")
    print_report(report_payload)


def _resolve_output_path(input_file: str, output_argument: Optional[str], multi_input: bool) -> Path:
    input_base = Path(input_file)
    if not output_argument:
        return input_base.with_name(f"cleaned_{input_base.stem}.xlsx")

    output_path = Path(output_argument)
    if multi_input:
        suffix = output_path.suffix or ".xlsx"
        stem = output_path.stem
        return output_path.with_name(f"{stem}_{input_base.stem}{suffix}")

    if output_path.suffix:
        return output_path
    return output_path.with_suffix(".xlsx")


def main():
    parser = argparse.ArgumentParser(description="NeatData - CSV Veri Temizleyici")
    parser.add_argument("--input", type=str, nargs="+", required=True, help="Bir veya birden fazla girdi dosyası")
    parser.add_argument("--output", type=str, default=None, help="Çıktı dosya adı (varsayılan cleaned_<ad>.xlsx)")
    parser.add_argument("--core-modules", dest="core_modules", type=str, default="all", help="Çalıştırılacak core modüller (virgülle ayrılmış) veya 'all'")
    parser.add_argument("--custom-modules", dest="custom_modules", type=str, default=None, help="Çalıştırılacak custom plugin anahtarları")
    parser.add_argument("--handle-missing-strategy", choices=["drop", "fill", "ffill", "bfill"], default=None, help="handle_missing stratejisi")
    parser.add_argument("--handle-missing-fill", dest="handle_missing_fill", default=None, help="fill stratejisi seçildiğinde kullanılacak değer")
    parser.add_argument("--convert-columns", type=str, default=None, help="convert_types modülüne aktarılacak sütun listesi")
    args = parser.parse_args()

    manager = PipelineManager()
    loader = DataLoader()

    multi_input = len(args.input) > 1
    for input_file in args.input:
        print(f"\n--- {input_file} dosyası işleniyor ---")
        run_pipeline_for_file(input_file, args, manager, loader, multi_input=multi_input)