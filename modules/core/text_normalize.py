"""General text normalization helpers for NeatData core.

This module contains dataset-agnostic helpers that can be called from
core modules and custom plugins. It includes optional `ftfy` for
fixing mojibake issues and falls back to safe heuristics if ftfy
is not installed.

Functions are flexible: they accept either `str` or `pandas.Series`.
"""
from __future__ import annotations

from typing import Union, Iterable, Optional
import re
import unicodedata

try:
    import ftfy
except Exception:
    ftfy = None  # Optional dependency: better mojibake fixes
try:
    from unidecode import unidecode
except Exception:
    unidecode = None  # Optional dependency: transliteration to ASCII

import pandas as pd


def _call_on_series_or_string(fn, value, *args, **kwargs):
    if isinstance(value, pd.Series):
        return value.apply(lambda x: fn(x, *args, **kwargs))
    return fn(value, *args, **kwargs)


def replace_nbsp(text: Union[str, pd.Series]) -> Union[str, pd.Series]:
    """Replace non-breaking spaces with regular spaces."""

    def _replace(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        return s.replace("\u00a0", " ")

    return _call_on_series_or_string(_replace, text)


def remove_zero_width(text: Union[str, pd.Series]) -> Union[str, pd.Series]:
    """Remove zero width / invisible characters (ZWSP etc.)."""

    ZW_PATTERN = "[\u200B\u200C\u200D\u2060\uFEFF]"

    def _remove(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        return re.sub(ZW_PATTERN, "", s)

    return _call_on_series_or_string(_remove, text)


def normalize_whitespace(text: Union[str, pd.Series], collapse: bool = True) -> Union[str, pd.Series]:
    """Trim and optionally collapse repeated whitespace into a single space."""

    def _norm(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        s = s.strip()
        return " ".join(s.split()) if collapse else s

    return _call_on_series_or_string(_norm, text)


def normalize_quotes(text: Union[str, pd.Series]) -> Union[str, pd.Series]:
    """Replace smart quotes/curly quotes and primes by ASCII equivalents.

    This is generic — site-specific replacements should still live in `modules/custom`.
    """

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

    def _map(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        for k, v in mapping.items():
            s = s.replace(k, v)
        # common artefacts
        s = s.replace("''", '"')
        s = s.replace('""', '"')
        return s

    return _call_on_series_or_string(_map, text)


def fix_mojibake(text: Union[str, pd.Series], use_ftfy: bool = True) -> Union[str, pd.Series]:
    """Attempt to fix mojibake; uses ftfy if available, otherwise heuristics.

    Accepts a string or a pandas Series (element-wise operation).
    """

    def _fix(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        s = str(s)
        # try ftfy first
        if use_ftfy and ftfy is not None:
            try:
                return ftfy.fix_text(s)
            except Exception:
                pass

        # heuristic fallback: try re-decode attempts if replacement char present
        if '�' not in s and '\xc3' not in s:
            return s

        # attempt latin1 -> utf-8 and reverse
        candidates = [s]
        try:
            candidates.append(s.encode('latin-1', errors='replace').decode('utf-8', errors='replace'))
        except Exception:
            pass
        try:
            candidates.append(s.encode('utf-8', errors='replace').decode('latin-1', errors='replace'))
        except Exception:
            pass

        # choose shortest replacement-character count
        best = min(candidates, key=lambda t: t.count('�'))
        return best

    return _call_on_series_or_string(_fix, text)


def unicode_normalize_text(text: Union[str, pd.Series], form: str = "NFC") -> Union[str, pd.Series]:
    """Normalize unicode canonical form: NFC or NFD."""

    def _norm(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        return unicodedata.normalize(form, s)

    return _call_on_series_or_string(_norm, text)


def to_ascii(text: Union[str, pd.Series], use_unidecode: bool = True) -> Union[str, pd.Series]:
    """Transliterate unicode characters to ASCII.

    If `unidecode` is not installed or disabled, returns the input string as-is.
    """

    def _to(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        if use_unidecode and unidecode is not None:
            try:
                return unidecode(s)
            except Exception:
                pass
        return s

    return _call_on_series_or_string(_to, text)


def strip_html_tags(text: Union[str, pd.Series]) -> Union[str, pd.Series]:
    """Strip common HTML tags and unescape entities."""

    import html

    TAG_RE = re.compile(r"<[^>]+>")

    def _strip(s: str) -> str:
        if s is None or pd.isna(s):
            return s
        s = TAG_RE.sub("", s)
        s = html.unescape(s)
        return s

    return _call_on_series_or_string(_strip, text)


def clean_text_pipeline(
    text: Union[str, pd.Series],
    *,
    fix_mojibake_opt: bool = True,
    normalize_quotes_opt: bool = True,
    replace_nbsp_opt: bool = True,
    remove_zw_opt: bool = True,
    collapse_whitespace: bool = True,
    use_unidecode: bool = False,
    strip_html: bool = False,
) -> Union[str, pd.Series]:
    """A convenience pipeline that chains common normalisations.

    Designed for generic pipeline usage where the same sequence of
    normalisations is applied to many datasets.
    """

    s = text
    if replace_nbsp_opt:
        s = replace_nbsp(s)
    if remove_zw_opt:
        s = remove_zero_width(s)
    if fix_mojibake_opt:
        s = fix_mojibake(s)
    if normalize_quotes_opt:
        s = normalize_quotes(s)
    if strip_html:
        s = strip_html_tags(s)
    s = unicode_normalize_text(s)
    if use_unidecode:
        s = to_ascii(s, use_unidecode=True)
    s = normalize_whitespace(s, collapse=collapse_whitespace)
    return s


__all__ = [
    "replace_nbsp",
    "remove_zero_width",
    "normalize_whitespace",
    "normalize_quotes",
    "fix_mojibake",
    "unicode_normalize_text",
    "clean_text_pipeline",
]

# Pipeline-friendly META & process
META = {
    "key": "text_normalize",
    "name": "Metin Normalizasyonu",
    "description": "Genel amaçlı metin normalizasyonu (NBSP, smart quotes, mojibake, whitespace, HTML temizleme).",
    "defaults": {
        "columns": None,
        "fix_mojibake_opt": True,
        "normalize_quotes_opt": True,
        "replace_nbsp_opt": True,
        "remove_zw_opt": True,
        "collapse_whitespace": True,
        "use_unidecode": False,
        "strip_html": False,
    },
    "order": 15,
}


def process(df: pd.DataFrame, *, columns: Optional[Iterable[str]] = None, **kwargs) -> pd.DataFrame:
    """Apply `clean_text_pipeline` to specified textual columns.

    Parameters mirror `clean_text_pipeline` options. If `columns` is None,
    operates on all object/string dtype columns.
    """

    frame = df.copy()
    target_columns = list(columns) if columns else frame.select_dtypes(include=["object", "string"]).columns.tolist()
    for col in target_columns:
        if col not in frame.columns:
            continue
        frame[col] = clean_text_pipeline(
            frame[col],
            fix_mojibake_opt=kwargs.get("fix_mojibake_opt", True),
            normalize_quotes_opt=kwargs.get("normalize_quotes_opt", True),
            replace_nbsp_opt=kwargs.get("replace_nbsp_opt", True),
            remove_zw_opt=kwargs.get("remove_zw_opt", True),
            collapse_whitespace=kwargs.get("collapse_whitespace", True),
            use_unidecode=kwargs.get("use_unidecode", False),
            strip_html=kwargs.get("strip_html", False),
        )
    return frame
