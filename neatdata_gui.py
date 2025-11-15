"""
NeatData GUI - Refactored version using utils modules.

Modern CustomTkinter-based GUI for data cleaning pipeline.
Utilizes modular components from modules.utils for better maintainability.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading

from modules.utils import (
    UIState,
    GuiLogger,
    GuiHelpers,
    GuiIO,
    PipelineRunner,
)
from modules.pipeline_manager import PipelineManager


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class NeatDataGUI(ctk.CTk):
    """Main GUI application for NeatData."""
    
    def __init__(self):
        super().__init__()
        self.title("NeatData - Veri Temizleme Asistanı")
        self.geometry("820x900")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        
        # Initialize components
        self.pipeline_manager = PipelineManager()
        self.ui_state = UIState()  # Renamed from 'state' to avoid conflict with Tkinter.state()
        self.custom_refresh_job = None
        
        # Setup logger with GUI callback
        self.logger = GuiLogger(gui_callback=self._on_log_message)
        
        # Setup pipeline runner
        self.runner = PipelineRunner(logger=self.logger)
        
        # Build UI
        GuiHelpers.create_header(self, row=0)
        self.entry_file, _ = GuiHelpers.create_file_picker_frame(
            self, "Girdi Dosyası", "Henüz dosya seçilmedi...",
            self.select_file, row=1
        )
        
        # Module panels container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        container.grid_columnconfigure((0, 1), weight=1)
        
        # Core modules
        core_descriptors = self.pipeline_manager.available_core_modules()
        self.core_module_vars = GuiHelpers.create_core_module_panel(container, core_descriptors)
        self.ui_state.selected_core_keys = list(core_descriptors.keys())
        
        # Custom modules
        custom_descriptors = self.pipeline_manager.available_custom_modules(refresh=True)
        self.custom_scroll, self.custom_module_vars = GuiHelpers.create_custom_module_panel(
            container, custom_descriptors, lambda: self.refresh_custom_modules(force=True)
        )
        
        # Output settings
        self.seg_output_type, self.entry_output_dir, _ = GuiHelpers.create_output_settings_frame(
            self, self.select_output_dir, row=3
        )
        self.ui_state.output_type = "xlsx"
        
        # Action buttons
        self.progress_bar, self.start_btn, self.stop_btn = GuiHelpers.create_action_buttons(
            self, self.start_cleaning, self.stop_cleaning, row=4
        )
        
        # Log box
        self.log_box = GuiHelpers.create_log_box(self, row=5)
        
        # Initialize
        self.logger.info("NeatData Hazır. Lütfen bir dosya seçin.")
        self._schedule_custom_refresh()
    
    # ==================== File Selection ====================
    
    def select_file(self):
        """Handle file selection."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Veri Dosyaları", "*.csv *.xlsx *.xlsm *.xls")]
        )
        if file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)
            self.ui_state.file_path = file_path
            self.logger.info(f"Dosya seçildi: {file_path}")
    
    def select_output_dir(self):
        """Handle output directory selection."""
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.entry_output_dir.delete(0, tk.END)
            self.entry_output_dir.insert(0, dir_path)
            self.ui_state.output_dir = dir_path
    
    # ==================== Module Management ====================
    
    def refresh_custom_modules(self, force: bool = False):
        """Refresh custom modules list."""
        descriptors = self.pipeline_manager.available_custom_modules(refresh=force)
        self.custom_module_vars = GuiHelpers.refresh_custom_module_panel(
            self.custom_scroll, descriptors, self.custom_module_vars
        )
    
    def _schedule_custom_refresh(self):
        """Schedule periodic refresh of custom modules."""
        self.refresh_custom_modules()
        self.custom_refresh_job = self.after(5000, self._schedule_custom_refresh)
    
    def _update_state_from_ui(self):
        """Update UIState from current UI selections."""
        # Core modules
        self.ui_state.selected_core_keys = [
            key for key, var in self.core_module_vars.items()
            if self._safe_get_var(var, False)
        ]
        
        # Custom modules
        self.ui_state.selected_custom_keys = [
            key for key, var in self.custom_module_vars.items()
            if self._safe_get_var(var, False)
        ]
        
        # Output settings
        self.ui_state.output_type = (
            "xlsx" if "Excel" in self.seg_output_type.get() else "csv"
        )
        self.ui_state.output_dir = self.entry_output_dir.get() or None
        self.ui_state.file_path = self.entry_file.get() or None
    
    @staticmethod
    def _safe_get_var(var: ctk.BooleanVar, default: bool) -> bool:
        """Safely get variable value with fallback."""
        try:
            return var.get()
        except Exception:
            return default
    
    # ==================== Pipeline Execution ====================
    
    def start_cleaning(self):
        """Start cleaning pipeline in background thread."""
        thread = threading.Thread(target=self._run_pipeline_thread, daemon=True)
        thread.start()
    
    def _run_pipeline_thread(self):
        """Background thread for pipeline execution."""
        self.progress_bar.set(0)
        self._update_state_from_ui()
        
        success = self.runner.run_file(
            self.ui_state,
            progress_callback=self._update_progress
        )
        
        if not success:
            self.progress_bar.set(0)
    
    def _update_progress(self, value: float):
        """Update progress bar."""
        try:
            self.progress_bar.set(value)
        except Exception:
            pass
    
    def stop_cleaning(self):
        """Stop pipeline execution."""
        self.progress_bar.set(0)
        self.logger.info(
            "İşlem durduruldu. Yeniden başlatmak için TEMİZLEMEYİ BAŞLAT butonunu kullanın."
        )
    
    # ==================== Logging ====================
    
    def _on_log_message(self, message: str):
        """Callback for logging messages to textbox."""
        try:
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"{message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        except Exception:
            pass  # Silently ignore GUI update errors


if __name__ == "__main__":
    app = NeatDataGUI()
    app.mainloop()

