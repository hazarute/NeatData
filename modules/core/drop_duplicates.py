"""Drop duplicate rows with configurable behaviour."""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

META = {
    "key": "drop_duplicates",
    "name": "Tekrar Eden Satırları Kaldır",
    "description": "Belirli sütunlara göre yinelenen satırları temizler ve isteğe bağlı olarak yalnızca ilk veya son kaydı tutar.",
    "defaults": {
        "subset": None,
        "keep": "first",
        "reset_index": True,
    },
    "order": 20,
}


def process(
    df: pd.DataFrame,
    *,
    subset: Optional[Iterable[str]] = None,
    keep: str = "first",
    reset_index: bool = True,
) -> pd.DataFrame:
    """Return dataframe without duplicate rows."""

    frame = df.copy()
    subset = list(subset) if subset else None
    deduped = frame.drop_duplicates(subset=subset, keep=keep)
    if reset_index:
        deduped = deduped.reset_index(drop=True)
    return deduped
