import pandas as pd
from typing import Optional, List
from modules.core.text_normalize import clean_text_pipeline
from pathlib import Path
import os
import unicodedata
import json
import ast

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
    # Robust price parsing supporting formats like:
    # - 1.234,56  (dot thousands, comma decimal)
    # - 1,234.56  (comma thousands, dot decimal)
    # - 1234.56   (dot decimal)
    # - 1234,56   (comma decimal)
    import re

    def normalize_price_text(text: str) -> str:
        if text is None:
            return ''
        s = str(text).strip()
        # drop currency abbreviations and NBSP
        s = s.replace('\u00a0', ' ')
        s = re.sub(r"[^0-9,\.\-]", "", s)
        if s == "":
            return s

        # European style: dots as thousand sep, comma as decimal (e.g. 1.234,56)
        euro_re = re.compile(r'^\d{1,3}(?:\.\d{3})*(?:,\d+)?$')
        # US style: commas as thousand sep, dot as decimal (e.g. 1,234.56)
        us_re = re.compile(r'^\d{1,3}(?:,\d{3})*(?:\.\d+)?$')

        if euro_re.match(s):
            s = s.replace('.', '')
            s = s.replace(',', '.')
            return s
        if us_re.match(s):
            s = s.replace(',', '')
            return s

        # Mixed or ambiguous cases: fallback heuristics
        # If there is both '.' and ',' decide based on last separator
        if ',' in s and '.' in s:
            if s.rfind(',') > s.rfind('.'):
                # comma likely decimal
                s = s.replace('.', '')
                s = s.replace(',', '.')
            else:
                # dot likely decimal
                s = s.replace(',', '')
            return s

        # Only commas -> treat comma as decimal
        if ',' in s and '.' not in s:
            s = s.replace(',', '.')
            return s

        # Only dots -> if single dot and <=2 digits after it => decimal, else remove dots
        if '.' in s and ',' not in s:
            parts = s.split('.')
            if len(parts) == 2 and 1 <= len(parts[1]) <= 2:
                # looks like decimal
                return s
            # otherwise remove dots (thousand separators)
            s = s.replace('.', '')
            return s

        return s

    s = series.astype(str).fillna("")
    normalized = s.map(normalize_price_text)
    # empty strings -> NA
    normalized = normalized.replace('', pd.NA)
    return pd.to_numeric(normalized, errors='coerce')


def _parse_extra(info):
    """Parse an 'extra' JSON-like field safely.

    Returns a dict for valid JSON/dict-like input, or {} for empty/invalid values.
    Ensures we never call string methods on NaN (which caused crashes).
    """
    if pd.isna(info):
        return {}
    if isinstance(info, dict):
        return info
    s = str(info).strip()
    if s == "":
        return {}
    # Try JSON first, fall back to ast.literal_eval, then to a lax replace-based attempt
    try:
        return json.loads(s)
    except Exception:
        try:
            return ast.literal_eval(s)
        except Exception:
            try:
                return json.loads(s.replace("'", '"'))
            except Exception:
                return {}


def run(df: pd.DataFrame, fix_mojibake: bool = True) -> pd.DataFrame:
    """Plugin to clean hepsiburada-like scraped product rows.

    Improvements:
    - Robust price parsing (handles both ' TL' and 'TL', removes '.' thousands and converts ',' to '.')
    - Reviews count cleansing (removes parentheses and '.' thousands separators)
    - Safe parsing of extra/info JSON-like fields (returns {} for NaN / empty cells)

    Returns the DataFrame with added columns: `Clean_Name`, `Cleaned_Price`,
    `Cleaned_Reviews` (if a reviews column is present) and `Extra_Parsed` (if an extra/info column exists).
    """

    df = df.copy()
    cols = list(df.columns)
    name_col = _choose_column(cols, ["name", "title", "product", "product_name", "Name"]) or (cols[0] if cols else None)
    price_col = _choose_column(cols, ["price", "Price", "amount", "Amount", "fiyat", "Fiyat"]) or None
    reviews_col = _choose_column(cols, ["reviews", "review_count", "yorum", "yorum_sayisi", "comments", "Reviews"]) or None
    extra_col = _choose_column(cols, ["extra", "extra_info", "info", "details", "metadata", "extraInfo"]) or None

    # Clean names in-place (replace original column values)
    if name_col and name_col in df.columns:
        df[name_col] = df[name_col].astype(str)
        cleaned_names = df[name_col].apply(lambda s: _clean_name(s, fix_mojibake=fix_mojibake))
        mask_item = cleaned_names.notna()
        try:
            cleaned_names.loc[mask_item] = clean_text_pipeline(cleaned_names.loc[mask_item], fix_mojibake_opt=True, use_unidecode=False)
        except Exception:
            # if pipeline fails, keep our normalized names
            pass
        df[name_col] = cleaned_names

    # Clean price in-place: preserve original text for logging then overwrite column
    if price_col and price_col in df.columns:
        orig_price = df[price_col].copy()
        try:
            cleaned_prices = _clean_price(orig_price)
        except Exception:
            s = orig_price.astype(str).str.replace('\u00a0', ' ', regex=False)
            s = s.str.replace(r'[^0-9,\.\-]', '', regex=True)
            s = s.replace('', pd.NA)
            cleaned_prices = pd.to_numeric(s, errors='coerce')

        # Overwrite original price column with numeric cleaned values
        df[price_col] = cleaned_prices

        # Log rows where original had text but cleaned price is NA
        bad_price_mask = cleaned_prices.isna() & orig_price.notna()
        if bad_price_mask.any():
            log_filename = "deleted_records_log.csv"
            invalid_rows = df.loc[bad_price_mask].copy()
            invalid_rows["Orig_Price_Text"] = orig_price.loc[bad_price_mask].astype(str)
            invalid_rows["Row_Index"] = invalid_rows.index
            invalid_rows["Reason"] = "Invalid Price"
            write_header = not Path(log_filename).exists()
            invalid_rows.to_csv(log_filename, mode="a", header=write_header, index=False, encoding="utf-8")

    # Clean reviews in-place (replace original column values)
    if reviews_col and reviews_col in df.columns:
        r = df[reviews_col].astype(str).fillna('')
        r = r.str.replace(r'[\(\)]', '', regex=True)
        r = r.str.replace(r'\.', '', regex=True)
        r = r.str.replace(r'[^0-9\-]', '', regex=True)
        r = r.replace('', pd.NA)
        cleaned_reviews = pd.to_numeric(r, errors='coerce', downcast='integer')
        df[reviews_col] = cleaned_reviews

    # Optionally parse extra/info column but keep it in the same column (stringified JSON)
    if extra_col and extra_col in df.columns:
        def _to_jsonish(x):
            parsed = _parse_extra(x)
            try:
                return json.dumps(parsed, ensure_ascii=False)
            except Exception:
                return str(x) if not pd.isna(x) else x

        df[extra_col] = df[extra_col].apply(lambda x: _to_jsonish(x) if not pd.isna(x) else x)

    return df


# Backwards-compatible alias
process = run
