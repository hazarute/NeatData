import pandas as pd
from typing import Optional, List
from modules.core.text_normalize import clean_text_pipeline
from pathlib import Path
import os
import unicodedata

META = {
    "name": "clean_hepsiburada_scrape",
    "version": "0.1",
    "description": "Cleans messy scraped product names and price fields from Hepsiburada/marketplace exports. Fixes NBSP, smart quotes, mojibake, inch representation, and trims extra whitespace.",
    "author": "hazarute",
    "params": {
        "fix_mojibake": True,
    },
}


def _choose_column(cols: List[str], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in cols:
            return c
    return None


def _normalize_whitespace(s: str) -> str:
    # collapse consecutive whitespace into a single space and trim
    return " ".join(s.split())


def _replace_nbsp(s: str) -> str:
    return s.replace("\u00a0", " ")


def _replace_smart_quotes_and_primes(s: str) -> str:
    # Replace multiple Unicode quote-like characters with ASCII equivalents
    mapping = {
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2013": "-",
        "\u2014": "-",
        "\u00b4": "'",
        "\u02bc": "'",
        "\u2032": "'",  # prime
        "\u2033": '"',  # double prime
    }
    for k, v in mapping.items():
        if k in s:
            s = s.replace(k, v)
    # Fix two apostrophes used to indicate inches -> to double quote
    s = s.replace("''", '"')
    # Convert double double-quotes previously output by scrapers
    s = s.replace('""', '"')
    return s


def _attempt_mojibake_fix(s: str) -> str:
    # If string contains replacement character U+FFFD (�) or other mojibake indicators
    # try re-decoding tricks between latin-1 and utf-8. Keep the best candidate.
    if '�' not in s and '\xc3' not in s:
        return s

    candidates = [s]
    try:
        candidates.append(s.encode('latin-1', errors='replace').decode('utf-8', errors='replace'))
    except Exception:
        pass
    try:
        # reverse attempt
        candidates.append(s.encode('utf-8', errors='replace').decode('latin-1', errors='replace'))
    except Exception:
        pass

    # Choose candidate with lowest count of replacement character
    def score(text: str) -> int:
        return text.count('�')

    best = min(candidates, key=score)
    return best


def _clean_name(s: str, fix_mojibake: bool = True) -> str:
    if s is None:
        return s
    s = str(s)
    s = _replace_nbsp(s)
    s = _replace_smart_quotes_and_primes(s)
    if fix_mojibake:
        s = _attempt_mojibake_fix(s)
    s = _normalize_whitespace(s)
    # NFC normalization: prefer composed forms for Turkish ç, ı, ğ, ş, etc.
    s = unicodedata.normalize('NFC', s)
    return s


def _clean_price(series: pd.Series) -> pd.Series:
    # Remove grouping separators and currency symbols if present and parse to float
    s = series.astype(str)
    s = s.str.replace(r"[^0-9.,-]", "", regex=True)
    # convert comma-as-thousands or decimal
    # Hepsiburada export uses dot as decimal in observed file, so prefer '.'; convert commas if needed
    s = s.str.replace(',', '')
    return pd.to_numeric(s, errors='coerce')


def run(df: pd.DataFrame, fix_mojibake: bool = True) -> pd.DataFrame:
    """Plugin to clean hepsiburada-like scraped product rows.

    - Replaces NBSP and normalizes space
    - Normalizes smart quotes and prime/inch notations
    - Attempts mojibake fixes (if enabled)
    - Standardizes price field to float (numbers only)

    Returns a cleaned DataFrame with columns: the original plus
    `Clean_Name` and `Cleaned_Price`.
    """

    df = df.copy()
    cols = list(df.columns)
    name_col = _choose_column(cols, ["name", "title", "product", "product_name", "Name"]) or (cols[0] if cols else None)
    price_col = _choose_column(cols, ["price", "Price", "amount", "Amount"]) or None

    # Clean names
    if name_col:
        df[name_col] = df[name_col].astype(str)
        df["Clean_Name"] = df[name_col].apply(lambda s: _clean_name(s, fix_mojibake=fix_mojibake))
        # First run general text normalization for item names (ftfy/unidecode optional)
        mask_item = df[name_col].notna()
        try:
            df.loc[mask_item, name_col] = clean_text_pipeline(df.loc[mask_item, name_col], fix_mojibake_opt=True, use_unidecode=False)
        except Exception:
            # Fall back to safe title-case if normalization fails
            df.loc[mask_item, name_col] = df.loc[mask_item, name_col].astype(str)

    # Clean price
    if price_col and price_col in df.columns:
        df["Cleaned_Price"] = _clean_price(df[price_col])
    else:
        # try to find a numeric column or guess
        df["Cleaned_Price"] = pd.Series([pd.NA] * len(df), index=df.index)

    # Optional: log rows with null price but original had price text
    if price_col:
        bad_price_mask = df["Cleaned_Price"].isna() & df[price_col].notna()
        if bad_price_mask.any():
            log_filename = "deleted_records_log.csv"
            invalid_rows = df.loc[bad_price_mask].copy()
            invalid_rows["Reason"] = "Invalid Price"
            write_header = not Path(log_filename).exists()
            invalid_rows.to_csv(log_filename, mode="a", header=write_header, index=False, encoding="utf-8")

    # Return cleaned frame
    return df


# Backwards-compatible alias
process = run
