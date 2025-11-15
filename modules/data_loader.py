"""Robust CSV/XLSX data loading utilities."""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import chardet
import pandas as pd


@dataclass
class DataLoaderConfig:
    sample_size: int = 65536
    fallback_encoding: str = "utf-8"
    default_delimiter: str = ","
    bad_lines_log: Path = Path("bad_lines.csv")


class DataLoader:
    """High level wrapper around pandas read_csv/read_excel with smart defaults."""

    def __init__(self, config: Optional[DataLoaderConfig] = None) -> None:
        self.config = config or DataLoaderConfig()
        self.logger = logging.getLogger("DataLoader")

    def detect_encoding_and_delimiter(self, file_path: Path) -> Tuple[str, str]:
        with file_path.open("rb") as handle:
            raw_bytes = handle.read(self.config.sample_size)
        result = chardet.detect(raw_bytes)
        encoding = result.get("encoding") or self.config.fallback_encoding

        with file_path.open("r", encoding=encoding, errors="replace") as handle:
            sample = handle.read(self.config.sample_size)
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = self.config.default_delimiter
        return encoding, delimiter

    def load(self, path: str, *, encoding: Optional[str] = None, delimiter: Optional[str] = None) -> pd.DataFrame:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {path}")

        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            encoding, delimiter = encoding, delimiter
            if encoding is None or delimiter is None:
                detected_encoding, detected_delimiter = self.detect_encoding_and_delimiter(file_path)
                encoding = encoding or detected_encoding
                delimiter = delimiter or detected_delimiter
            bad_lines = []

            def _capture_bad_lines(line):
                bad_lines.append(line)

            frame = pd.read_csv(
                file_path,
                encoding=encoding,
                sep=delimiter,
                engine="python",
                on_bad_lines=_capture_bad_lines,
            )
            # Heuristic fallback: if we ended up with a single-column frame
            # and that column name or first row contains commas, it's likely
            # the delimiter detection was wrong. Try re-reading with comma.
            if frame.shape[1] == 1 and delimiter != ',':
                first_col = str(frame.columns[0])
                first_val = ''
                try:
                    first_val = str(frame.iloc[0, 0]) if len(frame) > 0 else ''
                except Exception:
                    first_val = ''
                if (',' in first_col) or (',' in first_val):
                    self.logger.info("Tek sütun tespit edildi; comma olarak yeniden deneme yapılıyor.")
                    try:
                        frame = pd.read_csv(
                            file_path,
                            encoding=encoding,
                            sep=',',
                            engine='python',
                            on_bad_lines=_capture_bad_lines,
                            quotechar='"',
                        )
                    except Exception:
                        # if fallback fails, keep original frame and continue
                        self.logger.debug("Comma fallback read başarısız oldu; orijinal okuma korunuyor.")
            if bad_lines:
                self._append_bad_lines(bad_lines, encoding)
                self.logger.warning("%s satır bad_lines.csv dosyasına kaydedildi.", len(bad_lines))
            self.logger.info("%s başarıyla okundu (satır: %s)", path, len(frame))
            return frame

        if suffix in {".xlsx", ".xls", ".xlsm"}:
            frame = pd.read_excel(file_path)
            self.logger.info("%s başarıyla okundu (satır: %s)", path, len(frame))
            return frame

        raise ValueError(f"Desteklenmeyen dosya formatı: {suffix}")

    def _append_bad_lines(self, bad_lines, encoding: str) -> None:
        destination = self.config.bad_lines_log
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("a", encoding=encoding, newline="") as handle:
            writer = csv.writer(handle)
            for line in bad_lines:
                writer.writerow(line)


__all__ = ["DataLoader", "DataLoaderConfig"]