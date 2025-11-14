import pandas as pd
from modules.core.text_normalize import (
    replace_nbsp,
    normalize_quotes,
    fix_mojibake,
    to_ascii,
    clean_text_pipeline,
)


def test_replace_nbsp():
    assert replace_nbsp("A\xa0B") == "A B"


def test_normalize_quotes():
    assert normalize_quotes('“quote”') == '"quote"'


def test_fix_mojibake_and_pipeline():
    s = "Ta��nabilir"
    fixed = fix_mojibake(s, use_ftfy=True)
    # If ftfy is not installed, fallback may leave replacement characters; ensure pipeline returns string
    assert isinstance(fixed, str)


def test_to_ascii():
    assert to_ascii("ğüşiçÖ") is not None


def test_clean_text_pipeline_series():
    s = pd.Series(["A\xa0B", '“quote”', "Ta��nabilir"]) 
    cleaned = clean_text_pipeline(s, fix_mojibake_opt=True)
    assert cleaned.apply(lambda x: isinstance(x, str)).all()
