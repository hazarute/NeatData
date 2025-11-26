"""Trim leading/trailing spaces from textual columns."""

from __future__ import annotations

import pandas as pd

META = {
    "key": "trim_spaces",
    "name": "Boşlukları Temizle",
    "description": "Tüm metin sütunlarındaki baştaki ve sondaki boşlukları temizler, iç boşlukları korur.",
    "defaults": {},
    "order": 18,
}


def _trim_value(value):
    if isinstance(value, str):
        return value.strip()
    return value


def process(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    text_columns = frame.select_dtypes(include=["object", "string"]).columns
    if not len(text_columns):
        return frame
    frame[text_columns] = frame[text_columns].apply(lambda column: column.map(_trim_value))
    return frame
