"""GUI Logger: Centralized logging adapter for GUI and tests with styled output."""

import logging
from typing import Callable, Optional
from datetime import datetime


class GuiLogger:
    """Adapter that logs to terminal (with timestamps) and GUI callbacks."""

    def __init__(self, gui_callback: Optional[Callable[[str], None]] = None, level: int = logging.INFO):
        self.gui_callback = gui_callback
        self.level = level

        self.logger = logging.getLogger("NeatData")
        self.logger.setLevel(level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _emit(self, message: str, level: int = logging.INFO, gui_prefix: str = "") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        terminal_message = f"[{timestamp}] {message}"

        if self.gui_callback:
            try:
                self.gui_callback(f"{gui_prefix}{message}")
            except Exception as exc:
                self.logger.warning(f"GUI callback failed: {exc}")

        self.logger.log(level, terminal_message)

    def section(self, title: str) -> None:
        """Log a prominent section header."""
        self._emit("", logging.INFO)
        self._emit(f"--- [ {title} ] ---", logging.INFO)

    def step(self, message: str) -> None:
        """Log a pipeline step indicator."""
        self._emit(message, logging.INFO, gui_prefix=">> ")

    def success(self, message: str) -> None:
        """Log a success message."""
        self._emit(message, logging.INFO, gui_prefix="✅ ")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._emit(message, logging.WARNING, gui_prefix="⚠️ ")

    def error(self, message: str) -> None:
        """Log an error message."""
        self._emit(message, logging.ERROR, gui_prefix="❌ ")

    def info(self, message: str) -> None:
        """Log an informational message."""
        self._emit(message, logging.INFO)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self._emit(message, logging.DEBUG, gui_prefix="🐛 ")
