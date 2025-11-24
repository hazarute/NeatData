from pathlib import Path

import pandas as pd


def save_csv(
    df: pd.DataFrame,
    output_file: str | Path,
    *,
    sep_preamble: bool = False,
    encoding: str = "utf-8-sig",
    create_excel_copy: bool = False,
) -> Path:
    """Save a DataFrame to CSV without inserting a ``sep=,`` preamble.

    The legacy ``sep_preamble`` flag is kept for callers that still pass it,
    but the value is ignored because the GUI now expects clean CSV files.
    """

    outp = Path(output_file)
    outp.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(outp, index=False, encoding=encoding)

    if create_excel_copy:
        try:
            xlsx_path = outp.with_suffix(".xlsx")
            save_excel(df, xlsx_path)
        except Exception:
            # swallow errors to keep CSV write as primary
            pass

    return outp


def save_excel(df: pd.DataFrame, output_file: str | Path, **kwargs) -> Path:
    """Save DataFrame to Excel. This is the canonical implementation for Excel output.

    This function replaces the prior implementation in `save_to_excel.py` so
    that all output I/O is managed from a single module. It still uses
    `pandas.DataFrame.to_excel` directly and returns the written Path.
    """
    outp = Path(output_file)
    outp.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_excel(str(outp), index=False, **kwargs)
    except Exception as e:
        # Keep behavior simple: log to stdout and re-raise so callers can decide
        # (CLI/GUI may handle exceptions differently). Raising helps tests detect
        # failures instead of silently continuing.
        print(f"Excel'e kaydetme hatası: {e}")
        raise
    return outp


__all__ = ["save_csv", "save_excel"]
