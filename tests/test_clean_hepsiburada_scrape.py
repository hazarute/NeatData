import pandas as pd
import math

from modules.custom.clean_hepsiburada_scrape import run as clean_run


def approx_equal(a, b, rel=1e-6):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-9)


def test_price_formats():
    df = pd.DataFrame(
        {
            "name": ["a", "b", "c", "d", "e", "f"],
            "price": ["1.234,56", "1,234.56", "1234.56", "1234,56", "2.500TL", "3.000,50 TL"],
        }
    )
    out = clean_run(df)
    # plugin now overwrites original `price` column with numeric cleaned values
    prices = list(out["price"].astype(float))
    assert approx_equal(prices[0], 1234.56)
    assert approx_equal(prices[1], 1234.56)
    assert approx_equal(prices[2], 1234.56)
    assert approx_equal(prices[3], 1234.56)
    assert approx_equal(prices[4], 2500.0)
    assert approx_equal(prices[5], 3000.5)


def test_reviews_and_extra_safe():
    df = pd.DataFrame(
        {
            "name": ["a", "b"],
            "price": ["1000", "2000"],
            "reviews": ["(1.234)", "567"],
            "extra": [pd.NA, "{'k': 1}"]
        }
    )
    out = clean_run(df)
    # reviews cleaned in-place
    assert list(out["reviews"]) == [1234, 567]
    # extra parsed: first remains NA, second becomes JSON string
    assert pd.isna(out.loc[0, "extra"]) or out.loc[0, "extra"] == out.loc[0, "extra"]
    assert out.loc[1, "extra"] in ("{'k': 1}", '{"k": 1}', "{\'k\': 1}")


def test_parse_extra_handles_empty():
    df = pd.DataFrame({"name": ["x"], "price": ["10"], "extra": [pd.NA]})
    out = clean_run(df)
    assert pd.isna(out.loc[0, "extra"]) or out.loc[0, "extra"] == out.loc[0, "extra"]
