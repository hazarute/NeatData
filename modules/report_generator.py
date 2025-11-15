"""Report Generator: Generates cleaning reports for GUI, CLI, and logging.

Integrated with GuiLogger for unified logging across all environments.
"""

from typing import Optional, Dict, Any, List
from modules.utils.gui_logger import GuiLogger


class ReportGenerator:
    """
    Generates detailed cleaning reports.
    
    Supports both terminal output and GUI logging via GuiLogger.
    """
    
    def __init__(self, logger: Optional[GuiLogger] = None):
        """
        Initialize ReportGenerator.
        
        Args:
            logger: Optional GuiLogger instance (if None, creates default)
        """
        self.logger = logger or GuiLogger()
    
    def generate_report(
        self,
        input_file: str,
        initial_rows: int,
        final_rows: int,
        duplicates_removed: int = 0,
        missing_handled: str = "Pipeline tarafından yönetildi",
        errors: Optional[List[str]] = None,
        module_changes: Optional[Dict[str, int]] = None,
    ) -> None:
        """
        Generate and log a cleaning report.
        
        Args:
            input_file: Input file path
            initial_rows: Number of rows before cleaning
            final_rows: Number of rows after cleaning
            duplicates_removed: Number of duplicate rows removed
            missing_handled: Description of missing value handling
            errors: List of errors encountered
            module_changes: Dict mapping module names to number of changes
        """
        errors = errors or []
        module_changes = module_changes or {}
        
        # Calculate totals
        total_removed = duplicates_removed + (
            int(missing_handled) if isinstance(missing_handled, str) and missing_handled.isdigit() else 0
        )
        
        # Log report sections
        self.logger.info("")  # Blank line for readability
        self.logger.info("--- Detaylı Temizlik Raporu ---")
        self.logger.info(f"Dosya: {input_file}")
        self.logger.info(f"İlk satır sayısı: {initial_rows}")
        self.logger.info(f"Son satır sayısı: {final_rows}")
        self.logger.info(f"Toplam silinen satır: {total_removed}")
        self.logger.info(f"Tekrar eden satır silinen: {duplicates_removed}")
        self.logger.info(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")
        
        # Module-based changes
        if module_changes:
            self.logger.info("")
            self.logger.info("Modül Bazlı Değişiklikler:")
            for module_name, change_count in module_changes.items():
                self.logger.info(f"  - {module_name}: {change_count} değişiklik")
        
        # Error summary
        self.logger.info("")
        self.logger.info("Hata Özeti:")
        if errors:
            for error in errors:
                self.logger.info(f"  - {error}")
        else:
            self.logger.info("  - Hiç hata yok.")
        
        self.logger.info("--------------------------------")
        self.logger.info("")  # Blank line for readability
    
    def generate_batch_summary(
        self,
        processed_files: int,
        successful_files: int,
        failed_files: int,
        total_rows_cleaned: int,
    ) -> None:
        """
        Generate summary for batch processing.
        
        Args:
            processed_files: Total files processed
            successful_files: Files cleaned successfully
            failed_files: Files that failed
            total_rows_cleaned: Total rows cleaned across all files
        """
        self.logger.info("")
        self.logger.info("=== BATCH İŞLEM ÖZETİ ===")
        self.logger.info(f"İşlenen dosya: {processed_files}")
        self.logger.info(f"Başarılı: {successful_files}")
        self.logger.info(f"Başarısız: {failed_files}")
        self.logger.info(f"Toplam temizlenen satır: {total_rows_cleaned}")
        
        if failed_files == 0:
            self.logger.info(f"✅ Tüm {successful_files} dosya başarıyla temizlendi!")
        else:
            self.logger.warning(f"⚠️  {failed_files} dosya temizlenemedi. Lütfen hataları kontrol edin.")
        
        self.logger.info("===========================")
        self.logger.info("")


def generate_gui_report(
    rapor: Dict[str, Any],
    module_changes: Optional[Dict[str, int]] = None,
    log_callback: Optional[callable] = None,
) -> None:
    """
    Legacy function for backward compatibility.
    Generates GUI report using provided callback.
    
    Args:
        rapor: Report dict with keys: dosya, satir_sayisi_ilk, satir_sayisi_son, tekrar_silinen, eksik_silinen, hatalar
        module_changes: Optional dict of module changes
        log_callback: Callback function for logging (e.g., logger.info)
    """
    if not log_callback:
        return
    
    errors = rapor.get('hatalar', [])
    module_changes = module_changes or {}
    
    # Calculate totals
    duplicates_removed = rapor.get('tekrar_silinen', 0)
    missing_handled = rapor.get('eksik_silinen', 'Pipeline tarafından yönetildi')
    
    total_removed = duplicates_removed + (
        int(missing_handled) if isinstance(missing_handled, str) and missing_handled.isdigit() else 0
    )
    
    # Log report sections
    log_callback("")  # Blank line
    log_callback("--- Detaylı Temizlik Raporu ---")
    log_callback(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
    log_callback(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
    log_callback(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")
    log_callback(f"Toplam silinen satır: {total_removed}")
    log_callback(f"Tekrar eden satır silinen: {duplicates_removed}")
    log_callback(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")
    
    # Module changes
    if module_changes:
        log_callback("")
        log_callback("Modül Bazlı Değişiklikler:")
        for mod, change in module_changes.items():
            log_callback(f"  - {mod}: {change} değişiklik")
    
    # Error summary
    log_callback("")
    log_callback("Hata Özeti:")
    if errors:
        for hata in errors:
            log_callback(f"  - {hata}")
    else:
        log_callback("  - Hiç hata yok.")
    
    log_callback("--------------------------------")
    log_callback("")


def print_report(rapor: Dict[str, Any], module_changes: Optional[Dict[str, int]] = None) -> None:
    """
    Legacy function for backward compatibility.
    Prints report to console (terminal).
    
    Args:
        rapor: Report dict
        module_changes: Optional dict of module changes
    """
    errors = rapor.get('hatalar', [])
    module_changes = module_changes or {}
    
    duplicates_removed = rapor.get('tekrar_silinen', 0)
    missing_handled = rapor.get('eksik_silinen', 'Pipeline tarafından yönetildi')
    
    total_removed = duplicates_removed + (
        int(missing_handled) if isinstance(missing_handled, str) and missing_handled.isdigit() else 0
    )
    
    print("\n--- Detaylı Temizlik Raporu ---")
    print(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
    print(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
    print(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")
    print(f"Toplam silinen satır: {total_removed}")
    print(f"Tekrar eden satır silinen: {duplicates_removed}")
    print(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")
    
    if module_changes:
        print("\nModül Bazlı Değişiklikler:")
        for mod, change in module_changes.items():
            print(f"  - {mod}: {change} değişiklik")
    
    print("\nHata Özeti:")
    if errors:
        for hata in errors:
            print(f"  - {hata}")
    else:
        print("  - Hiç hata yok.")
    
    print("--------------------------------\n")
