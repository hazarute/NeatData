"""Standardize column headers by normalising casing and whitespace."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

META = {
    "key": "standardize_headers",
    "name": "Sütun Başlıklarını Standartlaştır",
    "description": "Tüm sütun adlarını küçük harfe çevirir, boşlukları alt çizgiye dönüştürür ve özel karakterleri temizler.",
    "defaults": {
        "case": "lower",
        "whitespace_replacement": "_",
        "allow_unicode": False,
        "max_length": 128,
    },
    "order": 10,
}


def _normalise(value: str, *, case: str, whitespace_replacement: str, allow_unicode: bool, max_length: int) -> str:
    cleaned = value.strip()
    if case == "lower":
        cleaned = cleaned.lower()
    elif case == "upper":
        cleaned = cleaned.upper()
    cleaned = re.sub(r"\s+", whitespace_replacement, cleaned)
    if not allow_unicode:
        cleaned = cleaned.encode("ascii", "ignore").decode()
    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "", cleaned)
    return cleaned[:max_length] or "column"


def process(
    df: pd.DataFrame,
    *,
    case: str = "lower",
    whitespace_replacement: str = "_",
    allow_unicode: bool = False,
    max_length: int = 128,
) -> pd.DataFrame:
    """Return a dataframe with standardised column headers."""

    frame = df.copy()
    new_columns: Iterable[str] = (
        _normalise(str(col), case=case, whitespace_replacement=whitespace_replacement, allow_unicode=allow_unicode, max_length=max_length)
        for col in frame.columns
    )
    frame.columns = list(new_columns)
    return frame
