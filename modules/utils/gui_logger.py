"""GUI Logger: Centralized logging adapter for GUI and tests."""

import logging
from typing import Callable, Optional
from datetime import datetime


class GuiLogger:
    """
    Adapter for logging messages to GUI textbox and/or Python logging.
    
    Allows GUI textbox callbacks while maintaining compatibility with
    standard logging and test environments.
    """
    
    def __init__(self, gui_callback: Optional[Callable[[str], None]] = None, level: int = logging.INFO):
        """
        Initialize GuiLogger.
        
        Args:
            gui_callback: Function to call for GUI updates (e.g., lambda msg: log_box.insert(...))
            level: Logging level (default: INFO)
        """
        self.gui_callback = gui_callback
        self.level = level
        
        # Setup Python logging
        self.logger = logging.getLogger("NeatData")
        self.logger.setLevel(level)
        
        # Console handler for non-GUI environments
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log(self, message: str, level: int = logging.INFO):
        """
        Log a message to GUI callback and Python logging.
        
        Args:
            message: Message to log
            level: Log level (default: INFO)
        """
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        
        # Send to GUI if callback exists
        if self.gui_callback:
            try:
                self.gui_callback(f">> {formatted_msg}")
            except Exception as exc:
                self.logger.warning(f"GUI callback failed: {exc}")
        
        # Send to Python logging
        if level == logging.DEBUG:
            self.logger.debug(formatted_msg)
        elif level == logging.INFO:
            self.logger.info(formatted_msg)
        elif level == logging.WARNING:
            self.logger.warning(formatted_msg)
        elif level == logging.ERROR:
            self.logger.error(formatted_msg)
        elif level == logging.CRITICAL:
            self.logger.critical(formatted_msg)
    
    def info(self, message: str):
        """Log info message."""
        self.log(message, logging.INFO)
    
    def warning(self, message: str):
        """Log warning message."""
        self.log(message, logging.WARNING)
    
    def error(self, message: str):
        """Log error message."""
        self.log(message, logging.ERROR)
    
    def debug(self, message: str):
        """Log debug message."""
        self.log(message, logging.DEBUG)
