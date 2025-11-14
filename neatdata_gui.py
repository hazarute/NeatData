import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import threading

from modules.data_loader import DataLoader
from modules.pipeline_manager import PipelineManager
from modules.report_generator import generate_gui_report


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class NeatDataGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NeatData - Veri Temizleme Asistanı")
        self.geometry("820x900")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.pipeline_manager = PipelineManager()
        self.data_loader = DataLoader()
        self.core_module_vars = {}
        self.custom_module_vars = {}
        self.custom_refresh_job = None

        self._build_header()
        self._build_file_picker()
        self._build_module_panels()
        self._build_output_panel()
        self._build_actions()
        self._build_log_box()

        self.log_message("NeatData Hazır. Lütfen bir dosya seçin.")
        self._schedule_custom_refresh()

    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title = ctk.CTkLabel(header, text="NeatData 🧹", font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(side="left")
        subtitle = ctk.CTkLabel(header, text="Dinamik Plugin Pipeline", text_color="gray")
        subtitle.pack(side="left", padx=12)

    def _build_file_picker(self):
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)
        label = ctk.CTkLabel(file_frame, text="Girdi Dosyası", font=ctk.CTkFont(size=15, weight="bold"))
        label.grid(row=0, column=0, padx=15, pady=(15, 4), sticky="w")
        self.entry_file = ctk.CTkEntry(file_frame, placeholder_text="Henüz dosya seçilmedi...")
        self.entry_file.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        browse = ctk.CTkButton(file_frame, text="Dosya Seç", command=self.select_file, width=120)
        browse.grid(row=1, column=1, padx=15, pady=(0, 15))

    def _build_module_panels(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        container.grid_columnconfigure((0, 1), weight=1)

        # Core panel
        core_frame = ctk.CTkFrame(container)
        core_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        core_label = ctk.CTkLabel(core_frame, text="Core Modüller", font=ctk.CTkFont(weight="bold"))
        core_label.pack(anchor="w", padx=12, pady=(12, 6))
        for descriptor in self.pipeline_manager.available_core_modules().values():
            var = ctk.BooleanVar(value=True)
            switch = ctk.CTkSwitch(core_frame, text=descriptor.name, variable=var)
            switch.pack(anchor="w", padx=16, pady=4)
            self.core_module_vars[descriptor.key] = var

        # Custom panel
        custom_frame = ctk.CTkFrame(container)
        custom_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        header = ctk.CTkFrame(custom_frame, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))
        label = ctk.CTkLabel(header, text="Custom Plugin'ler", font=ctk.CTkFont(weight="bold"))
        label.pack(side="left")
        refresh_btn = ctk.CTkButton(header, text="Yenile", command=lambda: self.refresh_custom_modules(force=True), width=70)
        refresh_btn.pack(side="right")
        self.custom_scroll = ctk.CTkScrollableFrame(custom_frame, label_text="plugins", height=260)
        self.custom_scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.refresh_custom_modules(force=True)

    def _build_output_panel(self):
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        output_frame.grid_columnconfigure(0, weight=1)
        label = ctk.CTkLabel(output_frame, text="Çıktı Ayarları", font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        self.seg_output_type = ctk.CTkSegmentedButton(output_frame, values=["Excel (.xlsx)", "CSV (.csv)"])
        self.seg_output_type.set("Excel (.xlsx)")
        self.seg_output_type.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.entry_output_dir = ctk.CTkEntry(output_frame, placeholder_text="Çıktı Klasörü (opsiyonel)")
        self.entry_output_dir.grid(row=2, column=0, padx=15, pady=(5, 10), sticky="ew")
        select_dir = ctk.CTkButton(output_frame, text="Klasör Seç", command=self.select_output_dir)
        select_dir.grid(row=2, column=1, padx=15, pady=(5, 10))

    def _build_actions(self):
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(action_frame)
        self.progress_bar.pack(fill="x", pady=(0, 8))
        self.progress_bar.set(0)
        btn_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        stop_btn = ctk.CTkButton(btn_frame, text="Durdur", command=self.stop_cleaning, width=90, fg_color="#D32F2F", hover_color="#B71C1C")
        stop_btn.pack(side="right", padx=(0, 10))
        start_btn = ctk.CTkButton(btn_frame, text="TEMİZLEMEYİ BAŞLAT", command=self.start_cleaning, height=40)
        start_btn.pack(side="right")

    def _build_log_box(self):
        self.log_box = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 12))
        self.log_box.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Veri Dosyaları", "*.csv *.xlsx *.xlsm *.xls")])
        if file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)
            self.log_message(f"Dosya seçildi: {file_path}")

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.entry_output_dir.delete(0, tk.END)
            self.entry_output_dir.insert(0, dir_path)

    def log_message(self, message: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f">> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def refresh_custom_modules(self, force: bool = False):
        modules = self.pipeline_manager.available_custom_modules(refresh=force)
        current_keys = set(self.custom_module_vars.keys())
        if not force and set(modules.keys()) == current_keys:
            return
        for widget in self.custom_scroll.winfo_children():
            widget.destroy()
        self.custom_module_vars.clear()
        if not modules:
            empty_label = ctk.CTkLabel(self.custom_scroll, text="Henüz eklenti yok.", text_color="gray")
            empty_label.pack(anchor="w", padx=10, pady=6)
            return
        for descriptor in modules.values():
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.custom_scroll, text=descriptor.name, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=4)
            self.custom_module_vars[descriptor.key] = var

    def _schedule_custom_refresh(self):
        self.refresh_custom_modules()
        self.custom_refresh_job = self.after(5000, self._schedule_custom_refresh)

    def start_cleaning(self):
        thread = threading.Thread(target=self._run_pipeline, daemon=True)
        thread.start()

    def _run_pipeline(self):
        self.progress_bar.set(0)
        file_path = self.entry_file.get()
        if not file_path:
            self.log_message("Lütfen bir veri dosyası seçin.")
            return
        try:
            dataframe = self.data_loader.load(file_path)
        except Exception as exc:  # pylint: disable=broad-except
            self.log_message(f"Dosya okunamadı: {exc}")
            return

        self.log_message(f"{file_path} okundu (satır: {len(dataframe)}).")

        core_selection = [key for key, var in self.core_module_vars.items() if var.get()]
        custom_selection = [key for key, var in self.custom_module_vars.items() if var.get()]
        self.pipeline_manager.build_pipeline(core_keys=core_selection or None, custom_keys=custom_selection or None)

        try:
            cleaned = self.pipeline_manager.run(dataframe)
        except Exception as exc:  # pylint: disable=broad-except
            self.log_message(f"Pipeline hatası: {exc}")
            return

        self.progress_bar.set(0.7)
        output_dir = Path(self.entry_output_dir.get() or Path(file_path).parent)
        output_dir.mkdir(parents=True, exist_ok=True)
        suffix = ".xlsx" if "Excel" in self.seg_output_type.get() else ".csv"
        output_path = output_dir / f"cleaned_{Path(file_path).stem}{suffix}"

        if suffix == ".xlsx":
            from modules.save_to_excel import process as save_to_excel_process

            save_to_excel_process(cleaned, output_file=str(output_path))
        else:
            # Save CSV using UTF-8 with BOM so Excel (Windows) opens columns reliably
            cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

        self.progress_bar.set(1)
        self.log_message(f"Çıktı kaydedildi: {output_path}")

        report = {
            "dosya": file_path,
            "satir_sayisi_ilk": len(dataframe),
            "satir_sayisi_son": len(cleaned),
            "tekrar_silinen": len(dataframe) - len(cleaned),
            "eksik_silinen": "Pipeline tarafından yönetildi",
            "hatalar": [],
        }
        generate_gui_report(report, log_callback=self.log_message)

    def stop_cleaning(self):
        self.progress_bar.set(0)
        self.log_message("İşlem durduruldu. Yeniden başlatmak için TEMİZLEMEYİ BAŞLAT butonunu kullanın.")


if __name__ == "__main__":
    app = NeatDataGUI()
    app.mainloop()

