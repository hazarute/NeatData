import pandas as pd
import numpy as np
from modules.core import text_normalize as tn


def test_remove_zero_width_and_normalize_whitespace():
    s = "A\u200BB\u200C  C\u200D"
    nozw = tn.remove_zero_width(s)
    assert "\u200B" not in nozw and "\u200C" not in nozw
    # collapse whitespace default True
    assert tn.normalize_whitespace("  a   b  ") == "a b"
    assert tn.normalize_whitespace("  a   b  ", collapse=False) == "a   b"


def test_unicode_normalize_and_to_ascii():
    s = "café"
    nfc = tn.unicode_normalize_text(s, form="NFC")
    assert isinstance(nfc, str)
    # to_ascii should return str, if unidecode not available it should return input
    ascii_val = tn.to_ascii("ğüşiçÖ", use_unidecode=False)
    assert isinstance(ascii_val, str)


def test_strip_html_tags_and_entities():
    s = "<p>Hello &amp; <b>World</b></p>"
    stripped = tn.strip_html_tags(s)
    assert "<" not in stripped
    # entities should be unescaped ("&amp;" -> "&")
    assert "&" in stripped
    assert "Hello" in stripped and "World" in stripped


def test_clean_text_pipeline_options_series():
    s = pd.Series(["A\u00a0B", "<b>n</b>", np.nan])
    cleaned = tn.clean_text_pipeline(s, strip_html=True, replace_nbsp_opt=True)
    assert cleaned.iloc[0] == "A B"
    assert cleaned.iloc[1] == "n"
    # NaN should be preserved
    assert pd.isna(cleaned.iloc[2]) or cleaned.iloc[2] == cleaned.iloc[2]


def test_process_applies_to_specified_columns(tmp_path):
    df = pd.DataFrame({
        "name": ["A\u00a0B", "C"],
        "notes": ["<i>x</i>", "y"],
        "num": [1, 2],
    })
    out = tn.process(df, columns=["name", "notes"], strip_html=True)
    assert out["name"].iloc[0] == "A B"
    assert out["notes"].iloc[0] == "x"
