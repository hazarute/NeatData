"""GUI IO: File operations helper for input/output management."""

import os
from pathlib import Path
from typing import Optional


class GuiIO:
    """Helper class for file and directory operations."""
    
    @staticmethod
    def normalize_path(path: str) -> Optional[Path]:
        """
        Normalize a path string to a Path object.
        
        Args:
            path: Path string (can be relative or absolute)
            
        Returns:
            Normalized Path object, or None if path is empty
        """
        if not path or not path.strip():
            return None
        return Path(path).expanduser().resolve()
    
    @staticmethod
    def ensure_output_dir(output_dir: Optional[str]) -> Path:
        """
        Ensure output directory exists. If not provided, return current directory.
        
        Args:
            output_dir: Output directory path (optional)
            
        Returns:
            Valid output Path object
            
        Raises:
            PermissionError: If directory cannot be created
        """
        if output_dir:
            path = GuiIO.normalize_path(output_dir)
            if path is None:
                path = Path.cwd()
        else:
            path = Path.cwd()
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path
        except PermissionError as exc:
            raise PermissionError(f"Çıktı klasörü oluşturulamadı: {path}") from exc
    
    @staticmethod
    def get_output_filename(input_file_path: str, output_type: str, custom_suffix: str = "") -> str:
        """
        Generate output filename based on input and format.
        
        Args:
            input_file_path: Path to input file
            output_type: Output format ('xlsx' or 'csv')
            custom_suffix: Custom suffix before extension (optional)
            
        Returns:
            Output filename (without directory path)
        """
        input_path = Path(input_file_path)
        stem = input_path.stem
        
        # Determine suffix
        if custom_suffix:
            filename = f"{stem}_{custom_suffix}"
        else:
            filename = f"cleaned_{stem}"
        
        # Add extension
        ext = ".xlsx" if output_type.lower() in ["xlsx", "excel"] else ".csv"
        return f"{filename}{ext}"
    
    @staticmethod
    def get_full_output_path(input_file_path: str, output_dir: Optional[str], output_type: str) -> Path:
        """
        Get full output file path.
        
        Args:
            input_file_path: Path to input file
            output_dir: Output directory (optional, uses input dir if None)
            output_type: Output format ('xlsx' or 'csv')
            
        Returns:
            Full Path to output file
        """
        output_directory = GuiIO.ensure_output_dir(output_dir or str(Path(input_file_path).parent))
        filename = GuiIO.get_output_filename(input_file_path, output_type)
        return output_directory / filename
    
    @staticmethod
    def check_dir_writable(dir_path: str) -> bool:
        """
        Check if directory is writable.
        
        Args:
            dir_path: Directory path to check
            
        Returns:
            True if writable, False otherwise
        """
        try:
            path = GuiIO.normalize_path(dir_path)
            if path is None:
                return False
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            return os.access(path, os.W_OK)
        except Exception:
            return False
    
    @staticmethod
    def check_file_exists(file_path: str) -> bool:
        """
        Check if file exists.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if file exists and is readable, False otherwise
        """
        try:
            path = GuiIO.normalize_path(file_path)
            if path is None:
                return False
            return path.exists() and path.is_file() and os.access(path, os.R_OK)
        except Exception:
            return False
