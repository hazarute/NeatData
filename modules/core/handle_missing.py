"""Flexible missing value handling utilities."""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

META = {
    "key": "handle_missing",
    "name": "Eksik Verileri Yönet",
    "description": "Eksik (NaN) değerleri silme, sabit değerle doldurma veya ileri/geri doldurma stratejileri sunar.",
    "defaults": {
        # Safer default: no-op unless caller specifies a strategy and columns.
        "strategy": "noop",
        "fill_value": None,
        "columns": None,
        "limit": None,
    },
    "order": 30,
}


def process(
    df: pd.DataFrame,
    *,
    strategy: str = "drop",
    fill_value=None,
    columns: Optional[Iterable[str]] = None,
    limit: Optional[int] = None,
) -> pd.DataFrame:
    """Handle missing values and return a new dataframe."""

    frame = df.copy()
    # If columns is None, do not operate on all columns implicitly — require explicit columns.
    if columns is None:
        return frame

    target_columns = [col for col in columns if col in frame.columns]
    if not target_columns:
        return frame

    if strategy == "noop":
        return frame

    if strategy == "drop":
        return frame.dropna(subset=target_columns)

    if strategy == "fill":
        frame[target_columns] = frame[target_columns].fillna(fill_value)
        return frame

    if strategy == "ffill":
        frame[target_columns] = frame[target_columns].fillna(method="ffill", limit=limit)
        return frame

    if strategy == "bfill":
        frame[target_columns] = frame[target_columns].fillna(method="bfill", limit=limit)
        return frame

    raise ValueError(f"Bilinmeyen strateji: {strategy}")
