"""CLI Handler: Command-line interface for NeatData pipeline.

Usage:
    python -m modules.cli_handler --input data.csv
    python -m modules.cli_handler --input file1.csv file2.csv --core-modules standardize_headers,drop_duplicates
"""

import argparse
from typing import List, Optional

from modules.utils import UIState, PipelineRunner, GuiLogger
from modules.pipeline_manager import PipelineManager


def _parse_list_argument(value: Optional[str], *, default_behavior: str) -> Optional[List[str]]:
    """Parse comma-separated module list or 'all'/'none' keywords.
    
    Args:
        value: Input string (e.g., "module1,module2" or "all" or "none")
        default_behavior: "all" or "none" - what to return if value is empty
        
    Returns:
        List of module keys, or None for "all", or [] for "none"
    """
    if not value:
        return None if default_behavior == "all" else []
    
    lowered = value.lower()
    if lowered == "all":
        return None
    if lowered == "none":
        return []
    
    return [item.strip() for item in value.split(",") if item.strip()]


def run_pipeline_for_file(input_file: str, state: UIState, runner: PipelineRunner) -> bool:
    """Execute pipeline for a single file using UIState and PipelineRunner.
    
    Args:
        input_file: Path to input file
        state: UIState with module selection and output settings
        runner: PipelineRunner for orchestration
        
    Returns:
        True if successful, False otherwise
    """
    state.file_path = input_file
    return runner.run_file(state, progress_callback=None)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NeatData - CSV Veri Temizleyici (CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # Tek dosya, tüm core modülleriyle (varsayılan)
  python -m modules.cli_handler --input data.csv
  
  # Birden fazla dosya, belirli modüllerle
  python -m modules.cli_handler --input data1.csv data2.csv \\
    --core-modules standardize_headers,drop_duplicates \\
    --custom-modules fix_cafe,clean_hepsiburada
  
  # Hiç core modülü çalıştırma (sadece custom)
  python -m modules.cli_handler --input data.csv \\
    --core-modules none --custom-modules my_plugin
  
  # CSV çıktısı, özel klasöre
  python -m modules.cli_handler --input data.csv \\
    --output-dir /tmp/cleaned --output-format csv
        """
    )
    
    parser.add_argument(
        "--input",
        type=str,
        nargs="+",
        required=True,
        help="Bir veya birden fazla girdi dosyası (örn: file1.csv file2.csv)"
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        type=str,
        default=None,
        help="Çıktı klasörü (varsayılan: girdinin bulunduğu klasör)"
    )
    parser.add_argument(
        "--core-modules",
        dest="core_modules",
        type=str,
        default="all",
        help="Core modüller: 'all', 'none', veya virgülle ayrılmış liste (varsayılan: all)"
    )
    parser.add_argument(
        "--custom-modules",
        dest="custom_modules",
        type=str,
        default="none",
        help="Custom plugin'ler: 'all', 'none', veya virgülle ayrılmış anahtarlar (varsayılan: none)"
    )
    parser.add_argument(
        "--output-format",
        dest="output_format",
        choices=["xlsx", "csv"],
        default="xlsx",
        help="Çıktı formatı (varsayılan: xlsx)"
    )
    
    args = parser.parse_args()
    
    # Setup logger (no GUI callback for CLI)
    logger = GuiLogger()
    
    # Create pipeline runner
    runner = PipelineRunner(logger=logger)
    
    # Get available modules
    manager = PipelineManager()
    all_core_keys = list(manager.available_core_modules().keys())
    all_custom_keys = list(manager.available_custom_modules().keys())
    
    # Parse module selections
    core_keys = _parse_list_argument(args.core_modules, default_behavior="all")
    if core_keys is None:
        core_keys = all_core_keys  # "all" → use all available
    
    custom_keys = _parse_list_argument(args.custom_modules, default_behavior="none")
    if custom_keys is None:
        custom_keys = all_custom_keys  # "all" → use all available
    
    # Create state template for all files
    template_state = UIState()
    template_state.selected_core_keys = core_keys
    template_state.selected_custom_keys = custom_keys
    template_state.output_type = args.output_format
    template_state.output_dir = args.output_dir
    
    # Process each input file
    logger.info(f"🎯 {len(args.input)} dosya işlenecek")
    logger.info(f"   Core: {core_keys or '(yok)'}")
    logger.info(f"   Custom: {custom_keys or '(yok)'}")
    
    success_count = 0
    
    for input_file in args.input:
        # Clone state for each file
        state = UIState(
            selected_core_keys=template_state.selected_core_keys.copy(),
            selected_custom_keys=template_state.selected_custom_keys.copy(),
            output_type=template_state.output_type,
            output_dir=template_state.output_dir,
            file_path=input_file
        )
        
        if run_pipeline_for_file(input_file, state, runner):
            success_count += 1
    
    # Summary
    logger.info(f"\n{'='*70}")
    logger.info(f"✅ {success_count}/{len(args.input)} dosya başarıyla temizlendi")


if __name__ == "__main__":
    main()
