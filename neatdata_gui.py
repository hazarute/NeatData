"""NeatData GUI: Thin view layer delegating to utility modules."""

import threading
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from modules.pipeline_manager import PipelineManager
from modules.utils import UIState, GuiLogger, PipelineRunner
from modules.utils import gui_helpers


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class NeatDataApp(ctk.CTk):
    """Main GUI application acting as a thin view layer."""

    def __init__(self):
        super().__init__()
        self.title("NeatData - Veri Temizleme Asistanı")
        self.geometry("820x900")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.pipeline_manager = PipelineManager()
        self.logger = GuiLogger(gui_callback=self._on_log_message)
        self.pipeline_runner = PipelineRunner(logger=self.logger)
        self.custom_refresh_job = None

        gui_helpers.GuiHelpers.create_header(self, row=0)
        self.input_entry, _ = gui_helpers.GuiHelpers.create_file_picker_frame(
            self, "Girdi Dosyası", "Henüz dosya seçilmedi...", self.select_file, row=1
        )

        panel_container = ctk.CTkFrame(self, fg_color="transparent")
        panel_container.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        panel_container.grid_columnconfigure((0, 1), weight=1)

        core_descriptors = self.pipeline_manager.available_core_modules()
        self.core_module_vars = gui_helpers.GuiHelpers.create_core_module_panel(
            panel_container, core_descriptors
        )

        custom_descriptors = self.pipeline_manager.available_custom_modules(refresh=True)
        self.custom_scroll, self.custom_module_vars = gui_helpers.GuiHelpers.create_custom_module_panel(
            panel_container, custom_descriptors, self.refresh_custom_modules
        )

        self.output_type_selector, self.output_dir_entry, _ = gui_helpers.GuiHelpers.create_output_settings_frame(
            self, self.select_output_dir, row=3
        )

        self.progress_bar, self.start_btn, self.stop_btn = gui_helpers.GuiHelpers.create_action_buttons(
            self, self.start_processing, self.stop_processing, row=4
        )
        self.stop_btn.configure(state="disabled")

        self.log_box = gui_helpers.GuiHelpers.create_log_box(self, row=5)

        self.logger.info("NeatData hazır. Lütfen bir dosya seçin.")
        self._schedule_custom_refresh()

    # ==================== File Selection ====================

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            filetypes=[("Veri Dosyaları", "*.csv *.xlsx *.xlsm *.xls")]
        )
        if not file_path:
            return
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)
        self.logger.info(f"Dosya seçildi: {file_path}")

    def select_output_dir(self) -> None:
        dir_path = filedialog.askdirectory()
        if not dir_path:
            return
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, dir_path)

    # ==================== Module Management ====================

    def refresh_custom_modules(self) -> None:
        descriptors = self.pipeline_manager.available_custom_modules(refresh=True)
        self.custom_module_vars = gui_helpers.GuiHelpers.refresh_custom_module_panel(
            self.custom_scroll, descriptors, self.custom_module_vars
        )

    def _schedule_custom_refresh(self) -> None:
        self.refresh_custom_modules()
        self.custom_refresh_job = self.after(5000, self._schedule_custom_refresh)

    # ==================== State Collection ====================

    def collect_ui_state(self) -> UIState:
        return UIState(
            selected_core_keys=[
                key for key, var in self.core_module_vars.items() if self._safe_get_var(var)
            ],
            selected_custom_keys=[
                key for key, var in self.custom_module_vars.items() if self._safe_get_var(var)
            ],
            output_type="xlsx" if "Excel" in self.output_type_selector.get() else "csv",
            output_dir=self.output_dir_entry.get() or None,
            file_path=self.input_entry.get() or None,
        )

    @staticmethod
    def _safe_get_var(var: ctk.BooleanVar) -> bool:
        try:
            return bool(var.get())
        except Exception:
            return False

    # ==================== Pipeline Execution ====================

    def start_processing(self) -> None:
        state = self.collect_ui_state()
        if not state.file_path:
            self.logger.error("Lütfen önce bir veri dosyası seçin.")
            return

        self._set_processing_state(True)
        thread = threading.Thread(target=self._run_pipeline_thread, args=(state,), daemon=True)
        thread.start()

    def _run_pipeline_thread(self, state: UIState) -> None:
        self.progress_bar.set(0)
        success = self.pipeline_runner.run_file(state, progress_callback=self._update_progress)
        if not success:
            self.progress_bar.set(0)
        self._set_processing_state(False)

    def stop_processing(self) -> None:
        self.progress_bar.set(0)
        self.logger.info(
            "İşlem durduruldu. Yeniden başlatmak için TEMİZLEMEYİ BAŞLAT butonuna basın."
        )
        self._set_processing_state(False)

    def _set_processing_state(self, running: bool) -> None:
        self.start_btn.configure(state="disabled" if running else "normal")
        self.stop_btn.configure(state="normal" if running else "disabled")

    def _update_progress(self, value: float) -> None:
        try:
            self.progress_bar.set(value)
        except Exception:
            pass

    # ==================== Logging ====================

    def _on_log_message(self, message: str) -> None:
        try:
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"{message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        except Exception:  # pragma: no cover - best effort logging
            pass


if __name__ == "__main__":
    app = NeatDataApp()
    app.mainloop()

