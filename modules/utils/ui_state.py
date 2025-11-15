"""UI State Management: Centralized state for GUI and tests."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UIState:
    """Represents the state of the UI: selected modules, output settings, and file path."""
    
    selected_core_keys: List[str] = field(default_factory=list)
    """List of selected core module keys (e.g., ['standardize_headers', 'drop_duplicates'])."""
    
    selected_custom_keys: List[str] = field(default_factory=list)
    """List of selected custom plugin keys."""
    
    output_type: str = "xlsx"
    """Output format: 'xlsx' or 'csv'."""
    
    output_dir: Optional[str] = None
    """Output directory path. If None, uses input file directory."""
    
    file_path: Optional[str] = None
    """Input file path (CSV/XLSX)."""
    
    def get_all_selected_modules(self) -> List[str]:
        """Return all selected module keys (core + custom)."""
        return self.selected_core_keys + self.selected_custom_keys
    
    def clear(self):
        """Clear all selections."""
        self.selected_core_keys.clear()
        self.selected_custom_keys.clear()
        self.file_path = None
    
    def __repr__(self) -> str:
        return (
            f"UIState(file={self.file_path}, core={self.selected_core_keys}, "
            f"custom={self.selected_custom_keys}, output={self.output_type}, dir={self.output_dir})"
        )
