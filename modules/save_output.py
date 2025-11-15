import json
from pathlib import Path
from typing import Optional

import pandas as pd

from .save_to_excel import process as _save_to_excel


def save_csv(df: pd.DataFrame, output_file: str | Path, *, sep_preamble: bool = True, encoding: str = "utf-8-sig", create_excel_copy: bool = False) -> Path:
    """Save DataFrame to CSV with BOM and optional 'sep=,' preamble.

    If create_excel_copy is True, also write an .xlsx copy using the existing excel helper.
    Returns the Path to the written CSV file.
    """
    outp = Path(output_file)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w", encoding=encoding, newline="") as f:
        if sep_preamble:
            f.write("sep=,\n")
        df.to_csv(f, index=False)

    if create_excel_copy:
        try:
            xlsx_path = outp.with_suffix(".xlsx")
            _save_to_excel(df, output_file=str(xlsx_path))
        except Exception:
            # swallow errors to keep CSV write as primary
            pass

    return outp


def save_excel(df: pd.DataFrame, output_file: str | Path, **kwargs) -> Path:
    """Save DataFrame to Excel using existing helper. Returns Path to written file."""
    outp = Path(output_file)
    outp.parent.mkdir(parents=True, exist_ok=True)
    _save_to_excel(df, output_file=str(outp), **kwargs)
    return outp


__all__ = ["save_csv", "save_excel"]
