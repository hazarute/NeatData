"""Pipeline Runner: Orchestrates pipeline execution for GUI, CLI, and tests."""

from time import perf_counter

import pandas as pd
from pathlib import Path
from typing import Callable, Optional, List

from modules.data_loader import DataLoader
from modules.pipeline_manager import PipelineManager
from modules.save_output import save_csv, save_excel
from modules.report_generator import generate_gui_report
from .ui_state import UIState
from .gui_logger import GuiLogger
from .gui_io import GuiIO


class PipelineRunner:
    """
    High-level orchestrator for data cleaning pipeline.
    
    Manages:
    - File loading
    - Module selection
    - Pipeline execution
    - Output saving
    - Report generation
    - Error handling and logging
    """
    
    def __init__(self, logger: Optional[GuiLogger] = None):
        """
        Initialize PipelineRunner.
        
        Args:
            logger: Optional GuiLogger for callbacks (if None, uses default logging)
        """
        self.data_loader = DataLoader()
        self.pipeline_manager = PipelineManager()
        self.logger = logger or GuiLogger()
    
    def run_file(
        self,
        state: UIState,
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> bool:
        """
        Execute pipeline on a file based on UIState.
        
        Args:
            state: UIState containing file path, module selection, and output settings
            progress_callback: Optional callback for progress updates (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        start_time = perf_counter()
        self.logger.section("İşlem Başlatılıyor")
        try:
            if not state.file_path:
                self.logger.error("Lütfen bir veri dosyası seçin.")
                return False

            if not GuiIO.check_file_exists(state.file_path):
                self.logger.error(f"Dosya bulunamadı veya okunamıyor: {state.file_path}")
                return False

            self._update_progress(progress_callback, 0.0)
            self.logger.step("Dosya okunuyor...")

            try:
                dataframe = self.data_loader.load(state.file_path)
            except Exception as exc:
                self.logger.error(f"Dosya okunamadı: {exc}")
                return False

            self.logger.success(f"Dosya yüklendi (Satır: {len(dataframe)})")
            self._update_progress(progress_callback, 0.2)

            selected_modules = state.get_all_selected_modules()
            self.logger.step(
                f"Pipeline Hazırlanıyor... (Seçili modül sayısı: {len(selected_modules)})"
            )

            if not selected_modules:
                self.logger.warning("Hiç modül seçilmedi; temizleme atlandı.")
                cleaned_dataframe = dataframe
            else:
                self.logger.step(f"Seçilen modüller: {selected_modules}")
                try:
                    cleaned_dataframe = self._execute_pipeline(dataframe, selected_modules)
                except Exception as exc:
                    self.logger.error(f"Pipeline hatası: {exc}")
                    return False

                self.logger.success(
                    f"Pipeline tamamlandı ({len(dataframe)} → {len(cleaned_dataframe)} satır)"
                )

            self._update_progress(progress_callback, 0.7)

            self.logger.step("Sonuçlar kaydediliyor...")
            try:
                output_path = self._save_output(state, cleaned_dataframe)
                self.logger.success(f"Kayıt Başarılı: {output_path}")
            except Exception as exc:
                self.logger.error(f"Çıktı kaydedilemedi: {exc}")
                return False

            self._update_progress(progress_callback, 0.9)

            duration = perf_counter() - start_time
            self.logger.section("Temizlik Raporu")
            self.logger.info(f"Satır (Başlangıç): {len(dataframe)}")
            self.logger.info(f"Satır (Son): {len(cleaned_dataframe)}")
            self.logger.info(f"Silinen satır: {len(dataframe) - len(cleaned_dataframe)}")
            self.logger.info(f"Süre: {duration:.2f} saniye")

            try:
                self._generate_report(state.file_path, dataframe, cleaned_dataframe)
            except Exception as exc:
                self.logger.warning(f"Rapor oluşturulamadı: {exc}")

            self._update_progress(progress_callback, 1.0)
            self.logger.success("İşlem başarıyla tamamlandı.")
            return True

        except Exception as exc:  # pylint: disable=broad-except
            self.logger.error(f"Beklenmeyen hata: {exc}")
            return False
    
    def _execute_pipeline(self, dataframe: pd.DataFrame, selected_modules: List[str]) -> pd.DataFrame:
        """
        Execute the pipeline with selected modules.
        
        Args:
            dataframe: Input dataframe
            selected_modules: List of selected module keys
            
        Returns:
            Cleaned dataframe
        """
        self.pipeline_manager.selected_modules_list = selected_modules
        return self.pipeline_manager.run_pipeline(dataframe)
    
    def _save_output(self, state: UIState, dataframe: pd.DataFrame) -> Path:
        """
        Save cleaned dataframe to file.
        
        Args:
            state: UIState with output settings
            dataframe: Dataframe to save
            
        Returns:
            Path to saved file
        """
        if not state.file_path:
            raise ValueError("File path is required to save output")
        
        output_path = GuiIO.get_full_output_path(
            state.file_path,
            state.output_dir,
            state.output_type
        )
        
        if state.output_type.lower() in ["xlsx", "excel"]:
            save_excel(dataframe, output_path)
        else:
            save_csv(dataframe, output_path, sep_preamble=True, encoding="utf-8-sig", create_excel_copy=False)
        
        return output_path
    
    def _generate_report(
        self,
        input_file: str,
        original_df: pd.DataFrame,
        cleaned_df: pd.DataFrame,
    ) -> None:
        """
        Generate cleaning report.
        
        Args:
            input_file: Input file path
            original_df: Original dataframe
            cleaned_df: Cleaned dataframe
        """
        report = {
            "dosya": input_file,
            "satir_sayisi_ilk": len(original_df),
            "satir_sayisi_son": len(cleaned_df),
            "tekrar_silinen": len(original_df) - len(cleaned_df),
            "eksik_silinen": "Pipeline tarafından yönetildi",
            "hatalar": [],
        }
        generate_gui_report(report, log_callback=self.logger.info)
    
    @staticmethod
    def _update_progress(callback: Optional[Callable[[float], None]], value: float) -> None:
        """Update progress if callback is provided."""
        if callback:
            try:
                callback(value)
            except Exception:
                pass  # Silently ignore progress callback errors
