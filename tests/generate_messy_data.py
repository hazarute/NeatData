"""Generate messy CSV files for tests.

Creates CSVs in the repository's `Messy Data/` directory that exercise
the `modules/core/drop_duplicates.py` and `modules/core/trim_spaces.py`
cleaning functions.

Run as a script from the repo root or from this file's directory.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
from random import Random


ROOT = Path(__file__).resolve().parents[1]
MESSY_DIR = ROOT / "Messy Data"


def ensure_dir():
    MESSY_DIR.mkdir(parents=True, exist_ok=True)


def make_drop_duplicates_csv(path: Path, n: int = 10000, seed: int = 1):
    """Create a CSV with duplicates and near-duplicates.

    Produces at least `n` rows by repeating a small pattern and shuffling.
    """
    base = [
        {"id": 1, "name": "Alice", "amount": 10},
        {"id": 2, "name": "Bob", "amount": 20},
        {"id": 1, "name": "Alice", "amount": 10},  # exact duplicate
        {"id": 3, "name": "Charlie", "amount": 30},
        {"id": 2, "name": "Bob", "amount": 20},    # exact duplicate
        {"id": 2, "name": "Bob ", "amount": 20},   # near-duplicate (trailing space)
        {"id": 4, "name": "Dana", "amount": 40},
    ]
    # repeat the base rows enough times to reach n
    reps = (n // len(base)) + 2
    df = pd.concat([pd.DataFrame(base) for _ in range(reps)], ignore_index=True)
    # trim to exactly n rows
    df = df.head(n).copy()
    # shuffle deterministically
    rng = Random(seed)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    df.to_csv(path, index=False)


def make_trim_spaces_csv(path: Path, n: int = 10000, seed: int = 2):
    """Create a CSV with textual fields containing leading/trailing spaces.

    Produces at least `n` rows by repeating a small catalogue of products.
    """
    base = [
        {"product": "  Coffee Beans", "description": "Fresh \n roast ", "price": " 15.00 "},
        {"product": "Tea  ", "description": "  Green tea", "price": "7.50"},
        {"product": "Sugar", "description": "Refined  ", "price": " 3.25"},
        {"product": "Milk", "description": "  Full fat", "price": "2.10 "},
        {"product": "Honey  ", "description": " Natural ", "price": "12.00"},
        {"product": "Bread", "description": " Sourdough ", "price": " 5.00"},
    ]
    reps = (n // len(base)) + 2
    df = pd.concat([pd.DataFrame(base) for _ in range(reps)], ignore_index=True)
    df = df.head(n).copy()
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    df.to_csv(path, index=False)


def make_mixed_csv(path: Path, n: int = 10000, seed: int = 3):
    """Create a CSV with both duplicates and spacing issues.

    Produces at least `n` rows by repeating a pattern of problem rows.
    """
    base = [
        {"order_id": 101, "customer": " Anna", "item": "Coffee ", "qty": 2},
        {"order_id": 102, "customer": "Bora", "item": "Tea", "qty": 1},
        {"order_id": 101, "customer": " Anna", "item": "Coffee ", "qty": 2},  # duplicate
        {"order_id": 103, "customer": " Cenk ", "item": "Sugar", "qty": 5},
        {"order_id": 104, "customer": "Derya", "item": "Milk", "qty": 1},
        {"order_id": 102, "customer": "Bora ", "item": "Tea", "qty": 1},       # near-duplicate (space)
    ]
    reps = (n // len(base)) + 2
    df = pd.concat([pd.DataFrame(base) for _ in range(reps)], ignore_index=True)
    df = df.head(n).copy()
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    df.to_csv(path, index=False)


def main(target_rows: int = 10000):
    ensure_dir()
    drop_path = MESSY_DIR / "messy_drop_duplicates.csv"
    spaces_path = MESSY_DIR / "messy_trim_spaces.csv"
    mixed_path = MESSY_DIR / "messy_mixed.csv"

    make_drop_duplicates_csv(drop_path, n=target_rows)
    make_trim_spaces_csv(spaces_path, n=target_rows)
    make_mixed_csv(mixed_path, n=target_rows)

    print(f"Wrote: {drop_path} ({target_rows} rows)")
    print(f"Wrote: {spaces_path} ({target_rows} rows)")
    print(f"Wrote: {mixed_path} ({target_rows} rows)")


if __name__ == "__main__":
    main()
