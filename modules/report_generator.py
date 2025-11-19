"""Report Generator: Generates cleaning reports for GUI, CLI, and logging.

Integrated with GuiLogger for unified logging across all environments.
"""

from typing import Optional, Dict, Any, List, Callable
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
        
        # Calculate totals from the before/after counts (most reliable).
        total_removed = max(0, int(initial_rows) - int(final_rows))

        # If caller provided a per-module breakdown, prefer that for reporting
        # but keep total_removed derived from counts as the source of truth.
        # We'll also detect mismatches between the derived total and the
        # provided module sums and log a warning if they differ.
        module_sum = 0
        try:
            module_sum = sum(int(v) for v in module_changes.values()) if module_changes else 0
        except Exception:
            module_sum = 0
        
        # Log report sections
        self.logger.info("")  # Blank line for readability
        self.logger.info("--- Detaylı Temizlik Raporu ---")
        self.logger.info(f"Dosya: {input_file}")
        self.logger.info(f"İlk satır sayısı: {initial_rows}")
        self.logger.info(f"Son satır sayısı: {final_rows}")
        self.logger.info(f"Toplam silinen satır: {total_removed}")
        # Prefer to show per-module counts when available.
        displayed_duplicates = duplicates_removed
        if module_changes and "drop_duplicates" in module_changes:
            try:
                displayed_duplicates = int(module_changes.get("drop_duplicates", duplicates_removed))
            except Exception:
                displayed_duplicates = duplicates_removed

        self.logger.info(f"Tekrar eden satır silinen: {displayed_duplicates}")
        self.logger.info(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")

        # Show module breakdown if provided
        if module_changes:
            self.logger.info("")
            self.logger.info("Modül Bazlı Değişiklikler (satır sayısı):")
            for module_name, change_count in module_changes.items():
                self.logger.info(f"  - {module_name}: {change_count}")

        # If the sum of module changes doesn't equal the derived total, warn the user.
        if module_changes and module_sum != total_removed:
            self.logger.warning(
                "UYARI: Modüller tarafından bildirilen değişikliklerin toplamı "
                f"({module_sum}) ile baştan/sonra sayılarından türetilen toplam ({total_removed}) uyuşmuyor."
            )
        
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
    log_callback: Optional[Callable[[str], None]] = None,
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
    
    # Derive totals from provided before/after counts when possible
    duplicates_removed = rapor.get('tekrar_silinen', 0)
    missing_handled = rapor.get('eksik_silinen', 'Pipeline tarafından yönetildi')
    try:
        initial = int(rapor.get('satir_sayisi_ilk', 0))
        final = int(rapor.get('satir_sayisi_son', 0))
        total_removed = max(0, initial - final)
    except Exception:
        total_removed = duplicates_removed
    
    # Log report sections
    log_callback("")  # Blank line
    log_callback("--- Detaylı Temizlik Raporu ---")
    log_callback(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
    log_callback(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
    log_callback(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")
    log_callback(f"Toplam silinen satır: {total_removed}")
    # prefer module-provided drop_duplicates count when present
    displayed_duplicates = duplicates_removed
    if module_changes and 'drop_duplicates' in module_changes:
        displayed_duplicates = module_changes.get('drop_duplicates', duplicates_removed)

    log_callback(f"Tekrar eden satır silinen: {displayed_duplicates}")
    log_callback(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")

    # Module changes
    if module_changes:
        log_callback("")
        log_callback("Modül Bazlı Değişiklikler:")
        for mod, change in module_changes.items():
            log_callback(f"  - {mod}: {change} değişiklik")

        # simple consistency check
        try:
            module_sum = sum(int(v) for v in module_changes.values())
            if module_sum != total_removed:
                log_callback("")
                log_callback(
                    f"UYARI: Modüller tarafından bildirilen değişikliklerin toplamı ({module_sum}) "
                    f"başlangıç/son sayılarından türetilen toplam ({total_removed}) ile uyuşmuyor."
                )
        except Exception:
            pass
    
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
    try:
        initial = int(rapor.get('satir_sayisi_ilk', 0))
        final = int(rapor.get('satir_sayisi_son', 0))
        total_removed = max(0, initial - final)
    except Exception:
        total_removed = duplicates_removed
    
    print("\n--- Detaylı Temizlik Raporu ---")
    print(f"Dosya: {rapor.get('dosya', 'Bilinmiyor')}")
    print(f"İlk satır sayısı: {rapor.get('satir_sayisi_ilk', '-')}")
    print(f"Son satır sayısı: {rapor.get('satir_sayisi_son', '-')}")

    print(f"Toplam silinen satır: {total_removed}")
    displayed_duplicates = duplicates_removed
    if module_changes and 'drop_duplicates' in module_changes:
        displayed_duplicates = module_changes.get('drop_duplicates', duplicates_removed)

    print(f"Tekrar eden satır silinen: {displayed_duplicates}")
    print(f"Eksik değer nedeniyle silinen/doldurulan: {missing_handled}")

    if module_changes:
        print("\nModül Bazlı Değişiklikler:")
        for mod, change in module_changes.items():
            print(f"  - {mod}: {change} değişiklik")

        try:
            module_sum = sum(int(v) for v in module_changes.values())
            if module_sum != total_removed:
                print("")
                print(
                    f"UYARI: Modüller tarafından bildirilen değişikliklerin toplamı ({module_sum}) "
                    f"başlangıç/son sayılarından türetilen toplam ({total_removed}) ile uyuşmuyor."
                )
        except Exception:
            pass
    
    print("\nHata Özeti:")
    if errors:
        for hata in errors:
            print(f"  - {hata}")
    else:
        print("  - Hiç hata yok.")
    
    print("--------------------------------\n")
