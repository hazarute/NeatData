"""Convert textual numeric columns into proper numeric dtypes."""

from __future__ import annotations

import re
from typing import Iterable, Optional

import pandas as pd

META = {
    "key": "convert_types",
    "name": "Veri Türlerini Düzelt",
    "description": "Metinsel olarak tutulmuş sayısal sütunları otomatik tespit eder ve uygun dtype'a dönüştürür.",
    "defaults": {
        "columns": None,
        "numeric_threshold": 0.7,
        "strip_characters": [",", " ", "$", "TL", "€", "%"],
        "coerce": True,
    },
    "order": 50,
}


def _clean_numeric_string(value: str, patterns) -> str:
    cleaned = value
    for token in patterns:
        cleaned = cleaned.replace(token, "")
    cleaned = re.sub(r"[^0-9+\-\.eE]", "", cleaned)
    return cleaned


def process(
    df: pd.DataFrame,
    *,
    columns: Optional[Iterable[str]] = None,
    numeric_threshold: float = 0.7,
    strip_characters: Optional[Iterable[str]] = None,
    coerce: bool = True,
) -> pd.DataFrame:
    """Convert eligible columns to numeric values."""

    frame = df.copy()
    strip_characters = list(strip_characters or [])
    candidate_columns = list(columns) if columns else frame.select_dtypes(include=["object", "string"]).columns.tolist()

    for column in candidate_columns:
        if column not in frame.columns:
            continue
        series = frame[column]
        prepared = series.astype(str).str.strip()
        if strip_characters:
            prepared = prepared.apply(lambda value: _clean_numeric_string(value, strip_characters))
        numeric_series = pd.to_numeric(prepared, errors="coerce" if coerce else "ignore")
        non_null_ratio = numeric_series.notna().mean()
        if non_null_ratio >= numeric_threshold:
            frame[column] = numeric_series
    return frame
