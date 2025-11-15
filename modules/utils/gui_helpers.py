"""GUI Helpers: Reusable component factories and builders."""

import customtkinter as ctk
from typing import Dict, Callable, Optional, Any, Union
from dataclasses import dataclass


@dataclass
class ModuleDescriptor:
    """Represents a module for display and control."""
    key: str
    name: str
    description: str = ""


class GuiHelpers:
    """Factory and builder methods for common GUI components."""
    
    @staticmethod
    def create_file_picker_frame(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        title: str,
        placeholder: str,
        on_browse: Callable[[], None],
        row: int = 0,
    ) -> tuple[ctk.CTkEntry, ctk.CTkButton]:
        """
        Create a file picker component (entry + browse button).
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            title: Label text
            placeholder: Entry placeholder text
            on_browse: Callback for browse button
            row: Grid row (default: 0)
            
        Returns:
            Tuple of (entry_widget, browse_button)
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=15, weight="bold"))
        label.grid(row=0, column=0, padx=15, pady=(15, 4), sticky="w")
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        browse_btn = ctk.CTkButton(frame, text="Seç", command=on_browse, width=90)
        browse_btn.grid(row=1, column=1, padx=15, pady=(0, 15))
        
        return entry, browse_btn
    
    @staticmethod
    def create_output_settings_frame(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        on_dir_browse: Callable[[], None],
        row: int = 0,
    ) -> tuple[ctk.CTkSegmentedButton, ctk.CTkEntry, ctk.CTkButton]:
        """
        Create output settings component (format + directory selection).
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            on_dir_browse: Callback for directory browse button
            row: Grid row (default: 0)
            
        Returns:
            Tuple of (format_button, dir_entry, browse_btn)
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, padx=20, pady=5, sticky="ew")
        frame.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(frame, text="Çıktı Ayarları", font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        format_btn = ctk.CTkSegmentedButton(frame, values=["Excel (.xlsx)", "CSV (.csv)"])
        format_btn.set("Excel (.xlsx)")
        format_btn.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        dir_entry = ctk.CTkEntry(frame, placeholder_text="Çıktı Klasörü (opsiyonel)")
        dir_entry.grid(row=2, column=0, padx=15, pady=(5, 10), sticky="ew")
        
        dir_btn = ctk.CTkButton(frame, text="Klasör Seç", command=on_dir_browse)
        dir_btn.grid(row=2, column=1, padx=15, pady=(5, 10))
        
        return format_btn, dir_entry, dir_btn
    
    @staticmethod
    def create_core_module_panel(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        descriptors: Dict[str, Any],
    ) -> Dict[str, ctk.BooleanVar]:
        """
        Create core modules panel with Switch controls.
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            descriptors: Dict of module descriptors with 'name' and 'key' fields
            
        Returns:
            Dict mapping module keys to BooleanVar controls
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        
        label = ctk.CTkLabel(frame, text="Core Modüller", font=ctk.CTkFont(weight="bold"))
        label.pack(anchor="w", padx=12, pady=(12, 6))
        
        vars_dict = {}
        for key, descriptor in descriptors.items():
            var = ctk.BooleanVar(value=True)
            switch = ctk.CTkSwitch(frame, text=descriptor.name, variable=var)
            switch.pack(anchor="w", padx=16, pady=4)
            vars_dict[key] = var
        
        return vars_dict
    
    @staticmethod
    def create_custom_module_panel(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        descriptors: Dict[str, Any],
        on_refresh: Callable[[], None],
    ) -> tuple[ctk.CTkScrollableFrame, Dict[str, ctk.BooleanVar]]:
        """
        Create custom modules panel with CheckBox controls.
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            descriptors: Dict of module descriptors with 'name' and 'key' fields
            on_refresh: Callback for refresh button
            
        Returns:
            Tuple of (scrollable_frame, variables_dict)
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))
        
        label = ctk.CTkLabel(header, text="Custom Plugin'ler", font=ctk.CTkFont(weight="bold"))
        label.pack(side="left")
        
        refresh_btn = ctk.CTkButton(header, text="Yenile", command=on_refresh, width=70)
        refresh_btn.pack(side="right")
        
        scroll_frame = ctk.CTkScrollableFrame(frame, label_text="plugins", height=260)
        scroll_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        vars_dict = GuiHelpers._populate_custom_modules(scroll_frame, descriptors)
        
        return scroll_frame, vars_dict
    
    @staticmethod
    def _populate_custom_modules(
        scroll_frame: ctk.CTkScrollableFrame,
        descriptors: Dict[str, Any],
    ) -> Dict[str, ctk.BooleanVar]:
        """Helper to populate custom modules in a scrollable frame."""
        # Clear existing widgets
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        
        vars_dict = {}
        
        if not descriptors:
            empty_label = ctk.CTkLabel(scroll_frame, text="Henüz eklenti yok.", text_color="gray")
            empty_label.pack(anchor="w", padx=10, pady=6)
            return vars_dict
        
        for key, descriptor in descriptors.items():
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(scroll_frame, text=descriptor.name, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=4)
            vars_dict[key] = var
        
        return vars_dict
    
    @staticmethod
    def refresh_custom_module_panel(
        scroll_frame: ctk.CTkScrollableFrame,
        descriptors: Dict[str, Any],
        vars_dict: Dict[str, ctk.BooleanVar],
    ) -> Dict[str, ctk.BooleanVar]:
        """
        Refresh custom modules panel.
        
        Args:
            scroll_frame: Scrollable frame widget
            descriptors: Updated descriptors
            vars_dict: Current variables dict
            
        Returns:
            Updated variables dict
        """
        current_keys = set(vars_dict.keys())
        new_keys = set(descriptors.keys())
        
        if current_keys == new_keys:
            return vars_dict
        
        return GuiHelpers._populate_custom_modules(scroll_frame, descriptors)
    
    @staticmethod
    def create_header(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        title: str = "NeatData 🧹",
        subtitle: str = "Dinamik Plugin Pipeline",
        row: int = 0,
    ) -> None:
        """
        Create header frame with title and subtitle.
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            title: Title text
            subtitle: Subtitle text
            row: Grid row
        """
        header = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        header.grid(row=row, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title_label = ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=26, weight="bold"))
        title_label.pack(side="left")
        
        subtitle_label = ctk.CTkLabel(header, text=subtitle, text_color="gray")
        subtitle_label.pack(side="left", padx=12)
    
    @staticmethod
    def create_action_buttons(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        on_start: Callable[[], None],
        on_stop: Callable[[], None],
        row: int = 0,
    ) -> tuple[ctk.CTkProgressBar, ctk.CTkButton, ctk.CTkButton]:
        """
        Create action buttons (Start/Stop) with progress bar.
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            on_start: Callback for start button
            on_stop: Callback for stop button
            row: Grid row
            
        Returns:
            Tuple of (progress_bar, start_btn, stop_btn)
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        
        progress = ctk.CTkProgressBar(frame)
        progress.pack(fill="x", pady=(0, 8))
        progress.set(0)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        stop_btn = ctk.CTkButton(
            btn_frame, text="Durdur", command=on_stop,
            width=90, fg_color="#D32F2F", hover_color="#B71C1C"
        )
        stop_btn.pack(side="right", padx=(0, 10))
        
        start_btn = ctk.CTkButton(
            btn_frame, text="TEMİZLEMEYİ BAŞLAT",
            command=on_start, height=40
        )
        start_btn.pack(side="right")
        
        return progress, start_btn, stop_btn
    
    @staticmethod
    def create_log_box(
        parent: Union[ctk.CTk, ctk.CTkFrame],
        row: int = 0,
    ) -> ctk.CTkTextbox:
        """
        Create log/text output box.
        
        Args:
            parent: Parent widget (CTk or CTkFrame)
            row: Grid row
            
        Returns:
            Textbox widget
        """
        log_box = ctk.CTkTextbox(parent, state="disabled", font=("Consolas", 12))
        log_box.grid(row=row, column=0, padx=20, pady=(0, 20), sticky="nsew")
        return log_box
