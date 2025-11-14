import pandas as pd
import os
from typing import Optional, List


def _choose_column(cols: List[str], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in cols:
            return c
    return None


def _parse_numeric_series(series: pd.Series) -> pd.Series:
    # Remove anything except digits, dot and minus
    cleaned = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce")


def run(df: pd.DataFrame) -> pd.DataFrame:
    """Cafe verileri için özel iş mantığı temizliği.

    Özellikler:
    - Sütun isimlerinin varyasyonlarını destekler (Item / Item Ordered, Transaction Date / Order Date, Total Spent / Price).
    - Fiyatı `Total Spent` olarak önceliklendirir; yoksa `Price Per Unit * Quantity` deneyerek hesaplar.
    - Tarih parse'ı esnektir (ilk deneme infer, ikinci deneme dayfirst=True).
    - Parse edilemeyen Tarih veya Fiyat satırları `deleted_records_log.csv` dosyasına yazılır ("Reason" sütunu ile).
    - Mükerrer silme tüm satır eşleşmesine göre yapılır (tüm sütunlar).
    """

    initial_count = len(df)

    # Audit copy for logging
    df_audit = df.copy()

    # Normalize column selection
    cols = list(df.columns)
    txn_col = _choose_column(cols, ["Transaction ID", "Txn ID", "TransactionID"])
    item_col = _choose_column(cols, ["Item Ordered", "Item", "Product"])
    total_spent_col = _choose_column(cols, ["Total Spent", "Total_Spent", "Amount", "Price"]) 
    price_per_unit_col = _choose_column(cols, ["Price Per Unit", "Price_Per_Unit", "Unit Price", "PricePerUnit"])
    quantity_col = _choose_column(cols, ["Quantity", "Qty"])
    date_col = _choose_column(cols, ["Order Date", "OrderDate", "Transaction Date", "TransactionDate"])

    # 1) Drop exact duplicate rows only
    df = df.drop_duplicates(keep="last")

    # 2) Standardize item names if present (do not coerce missing -> 'Nan')
    if item_col:
        # operate only on non-null values
        mask_item = df[item_col].notna()
        df.loc[mask_item, item_col] = (
            df.loc[mask_item, item_col].astype(str).str.strip().str.title()
        )
        corrections = {"Expresso": "Espresso", "Tea - Hot": "Tea", "Tea - Iced": "Iced Tea", "Cappucino": "Cappuccino"}
        df.loc[mask_item, item_col] = df.loc[mask_item, item_col].replace(corrections)

    # Normalize common placeholder tokens (UNKNOWN, ERROR, N/A) to actual missing values
    placeholder_tokens = {"UNKNOWN", "ERROR", "NA", "N/A", "NONE", "-"}
    # Compute placeholder masks BEFORE we replace them so we can still treat them as 'original content' for logging
    placeholder_mask = {}
    for c in df.select_dtypes(include=[object]).columns:
        mask = df[c].astype(str).str.strip().str.upper().isin(placeholder_tokens)
        placeholder_mask[c] = mask
    for c in df.select_dtypes(include=[object]).columns:
        df[c] = df[c].where(~df[c].astype(str).str.strip().str.upper().isin(placeholder_tokens), other=pd.NA)

    # 3) Parse/compute price
    price_parsed = None
    # If Total Spent exists, try parse it first
    if total_spent_col:
        price_parsed = _parse_numeric_series(df[total_spent_col])

    # If couldn't parse and we have price per unit and quantity, try compute
    if (price_parsed is None or price_parsed.isna().all()) and price_per_unit_col and quantity_col:
        ppu = _parse_numeric_series(df[price_per_unit_col])
        qty = pd.to_numeric(df[quantity_col], errors="coerce")
        computed = (ppu * qty)
        # Prefer computed where parsed is NaN
        if price_parsed is None:
            price_parsed = computed
        else:
            price_parsed = price_parsed.fillna(computed)

    # If still None, create NaN series
    if price_parsed is None:
        price_parsed = pd.Series([pd.NA] * len(df), index=df.index)

    # 4) Parse dates flexibly
    date_parsed = None
    if date_col:
        # first attempt: flexible parse
        date_parsed = pd.to_datetime(df[date_col], errors="coerce")
        try:
            mask = date_parsed.isna() & df[date_col].notna()
            if mask.any():
                # second attempt with dayfirst
                second = pd.to_datetime(df.loc[mask, date_col], errors="coerce", dayfirst=True)
                date_parsed.loc[mask] = second
        except Exception:
            pass
    else:
        date_parsed = pd.Series([pd.NaT] * len(df), index=df.index)

    # 5) Determine invalid rows: where parsing failed but original had content
    invalid_price_mask = pd.Series(False, index=df.index)
    if total_spent_col and total_spent_col in df.columns:
        original_present = df[total_spent_col].notna() | placeholder_mask.get(total_spent_col, pd.Series(False, index=df.index))
        invalid_price_mask = price_parsed.isna() & original_present
    elif price_per_unit_col and quantity_col and price_per_unit_col in df.columns and quantity_col in df.columns:
        # if original components present but computation failed
        invalid_price_mask = price_parsed.isna() & (df[price_per_unit_col].notna() | df[quantity_col].notna())

    invalid_date_mask = pd.Series(False, index=df.index)
    if date_col and date_col in df.columns:
        original_date_present = df[date_col].notna() | placeholder_mask.get(date_col, pd.Series(False, index=df.index))
        invalid_date_mask = date_parsed.isna() & original_date_present

    invalid_mask = invalid_price_mask | invalid_date_mask

    # 6) Log deleted records with reasons
    if invalid_mask.any():
        invalid_rows = df_audit.loc[invalid_mask].copy()
        invalid_rows["Reason"] = ""
        invalid_rows.loc[invalid_price_mask, "Reason"] = invalid_rows.loc[invalid_price_mask, "Reason"] + "Invalid Price"
        invalid_rows.loc[invalid_date_mask, "Reason"] = invalid_rows.loc[invalid_date_mask, "Reason"] + ("; " if invalid_rows.loc[invalid_date_mask, "Reason"].astype(str).ne("").any() else "") + "Invalid Date"

        log_filename = "deleted_records_log.csv"
        write_header = not os.path.exists(log_filename)
        invalid_rows.to_csv(log_filename, mode="a", header=write_header, index=False, encoding="utf-8")

    # 7) Remove invalid rows from main df
    df_clean = df.loc[~invalid_mask].copy()

    # 8) Assign cleaned parsed values back into canonical column names for downstream
    # Use 'Cleaned_Price' and 'Cleaned_Date' to avoid overwriting original source columns
    df_clean["Cleaned_Price"] = price_parsed.loc[df_clean.index]
    df_clean["Cleaned_Date"] = pd.to_datetime(date_parsed.loc[df_clean.index], errors="coerce").dt.strftime("%Y-%m-%d")

    # 9) Convert Quantity to numeric if present
    if quantity_col and quantity_col in df_clean.columns:
        df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors="coerce").astype('Int64')

    # Final duplicates check across full rows (already done earlier but keep idempotent)
    df_clean = df_clean.drop_duplicates(keep="last")

    return df_clean


# Backwards-compatible alias: some parts of the system expect a `process()` callable
process = run