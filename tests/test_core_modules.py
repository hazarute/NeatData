"""Comprehensive tests for all core cleaning modules.

Tests cover:
- standardize_headers: Column name normalization
- drop_duplicates: Duplicate row removal
- handle_missing: Missing value handling strategies
- trim_spaces: Whitespace trimming
- convert_types: Type detection and conversion
- text_normalize: Text normalization pipeline
"""

import pytest
import pandas as pd
import numpy as np

from modules.core.standardize_headers import process as standardize_headers
from modules.core.drop_duplicates import process as drop_duplicates
from modules.core.handle_missing import process as handle_missing
from modules.core.trim_spaces import process as trim_spaces
from modules.core.convert_types import process as convert_types
from modules.core.text_normalize import process as text_normalize


class TestStandardizeHeaders:
    """Test column header standardization."""
    
    def test_lowercase_conversion(self):
        """Headers should be converted to lowercase."""
        df = pd.DataFrame({"First Name": [1, 2], "LAST_NAME": [3, 4]})
        result = standardize_headers(df, case="lower")
        assert "first_name" in result.columns
        assert "last_name" in result.columns
    
    def test_whitespace_replacement(self):
        """Spaces should be replaced with underscores."""
        df = pd.DataFrame({"First Name": [1], "Last Name": [2]})
        result = standardize_headers(df)
        assert "first_name" in result.columns
        assert "last_name" in result.columns
    
    def test_special_character_removal(self):
        """Special characters should be removed."""
        df = pd.DataFrame({"First-Name!": [1], "Last@Name#": [2]})
        result = standardize_headers(df)
        assert "firstname" in result.columns or "first_name" in result.columns
    
    def test_max_length(self):
        """Long headers should be truncated."""
        df = pd.DataFrame({"a" * 200: [1]})
        result = standardize_headers(df, max_length=50)
        assert len(result.columns[0]) <= 50
    
    def test_empty_header_becomes_column(self):
        """Headers that normalize to empty string should become 'column'."""
        df = pd.DataFrame({"   ": [1], "   @@@   ": [2]})
        result = standardize_headers(df)
        assert "column" in result.columns or result.columns[0] == "column"


class TestDropDuplicates:
    """Test duplicate row removal."""
    
    def test_basic_duplicate_removal(self):
        """Duplicate rows should be removed, keeping first."""
        df = pd.DataFrame({
            "id": [1, 2, 2, 3],
            "name": ["a", "b", "b", "c"]
        })
        result = drop_duplicates(df)
        assert len(result) == 3
        assert list(result["id"]) == [1, 2, 3]
    
    def test_keep_last(self):
        """Should keep last duplicate when keep='last'."""
        df = pd.DataFrame({
            "id": [1, 2, 2, 3],
            "name": ["a", "b", "b", "c"],
            "value": [10, 20, 20, 30]
        })
        result = drop_duplicates(df, keep="last")
        assert len(result) == 3
        # Index is reset by default
        assert list(result.index) == [0, 1, 2]
        # Second row should have id=2
        assert result.iloc[1]["id"] == 2
    
    def test_subset_columns(self):
        """Should only check duplicates on subset columns."""
        df = pd.DataFrame({
            "id": [1, 1, 2],
            "name": ["a", "b", "c"]
        })
        result = drop_duplicates(df, subset=["id"])
        assert len(result) == 2
    
    def test_reset_index(self):
        """Index should be reset after deduplication."""
        df = pd.DataFrame({
            "id": [1, 2, 2, 3],
            "name": ["a", "b", "b", "c"]
        })
        result = drop_duplicates(df, reset_index=True)
        assert list(result.index) == [0, 1, 2]
    
    def test_no_duplicates(self):
        """DataFrame with no duplicates should remain unchanged."""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["a", "b", "c"]
        })
        result = drop_duplicates(df)
        assert len(result) == 3


class TestHandleMissing:
    """Test missing value handling."""
    
    def test_noop_strategy(self):
        """Noop strategy should not modify dataframe."""
        df = pd.DataFrame({
            "a": [1, np.nan, 3],
            "b": ["x", "y", np.nan]
        })
        result = handle_missing(df, strategy="noop")
        assert result.isna().sum().sum() == 2  # Same missing values
    
    def test_drop_strategy(self):
        """Drop strategy should remove rows with NaN."""
        df = pd.DataFrame({
            "a": [1, np.nan, 3],
            "b": ["x", "y", "z"]
        })
        result = handle_missing(df, strategy="drop", columns=["a"])
        assert len(result) == 2
        assert not result["a"].isna().any()
    
    def test_fill_strategy(self):
        """Fill strategy should replace NaN with value."""
        df = pd.DataFrame({
            "a": [1, np.nan, 3],
            "b": [np.nan, 2, 3]
        })
        result = handle_missing(df, strategy="fill", fill_value=0, columns=["a", "b"])
        assert not result.isna().any().any()
        assert result.loc[1, "a"] == 0
    
    def test_ffill_strategy(self):
        """Forward fill should propagate forward."""
        df = pd.DataFrame({
            "a": [1, np.nan, np.nan, 4]
        })
        result = handle_missing(df, strategy="ffill", columns=["a"])
        assert result.loc[1, "a"] == 1
        assert result.loc[2, "a"] == 1
    
    def test_bfill_strategy(self):
        """Backward fill should propagate backward."""
        df = pd.DataFrame({
            "a": [1, np.nan, np.nan, 4]
        })
        result = handle_missing(df, strategy="bfill", columns=["a"])
        assert result.loc[1, "a"] == 4
        assert result.loc[2, "a"] == 4
    
    def test_no_columns_specified(self):
        """Should return unmodified if no columns specified."""
        df = pd.DataFrame({
            "a": [1, np.nan, 3]
        })
        result = handle_missing(df, strategy="drop", columns=None)
        assert result.equals(df)
    
    def test_invalid_strategy(self):
        """Should raise ValueError for unknown strategy."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        with pytest.raises(ValueError):
            handle_missing(df, strategy="invalid_strategy", columns=["a"])


class TestTrimSpaces:
    """Test whitespace trimming."""
    
    def test_trim_leading_trailing(self):
        """Should trim leading and trailing spaces."""
        df = pd.DataFrame({
            "name": ["  Alice  ", " Bob ", "Charlie"]
        })
        result = trim_spaces(df)
        assert result.loc[0, "name"] == "Alice"
        assert result.loc[1, "name"] == "Bob"
    
    def test_preserve_internal_spaces(self):
        """Should preserve spaces within text."""
        df = pd.DataFrame({
            "name": ["  John Doe  ", "  Jane Smith  "]
        })
        result = trim_spaces(df)
        assert "John Doe" in str(result.loc[0, "name"])
        assert "Jane Smith" in str(result.loc[1, "name"])
    
    def test_non_string_columns_unchanged(self):
        """Non-string columns should remain unchanged."""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["  Alice  ", "  Bob  ", "  Charlie  "]
        })
        result = trim_spaces(df)
        assert list(result["id"]) == [1, 2, 3]
    
    def test_numeric_columns_ignored(self):
        """Numeric columns should be ignored."""
        df = pd.DataFrame({
            "value": [1.5, 2.3, 3.7]
        })
        result = trim_spaces(df)
        assert result["value"].dtype in [float, np.float64]
    
    def test_nan_values_preserved(self):
        """NaN values should remain NaN."""
        df = pd.DataFrame({
            "name": ["  Alice  ", np.nan, "  Charlie  "]
        })
        result = trim_spaces(df)
        assert pd.isna(result.loc[1, "name"])


class TestConvertTypes:
    """Test automatic type conversion."""
    
    def test_numeric_string_conversion(self):
        """Numeric strings should be converted to float/int."""
        df = pd.DataFrame({
            "value": ["1", "2.5", "3"]
        })
        result = convert_types(df)
        assert result["value"].dtype in [float, np.float64]
    
    def test_currency_conversion(self):
        """Currency strings should be converted to numeric."""
        df = pd.DataFrame({
            "price": ["$10.50", "$20.00", "$15.75"]
        })
        result = convert_types(df, strip_characters=["$"])
        assert result["price"].dtype in [float, np.float64]
        assert result.loc[0, "price"] == 10.50
    
    def test_percentage_conversion(self):
        """Percentage strings should be converted."""
        df = pd.DataFrame({
            "rate": ["10%", "20%", "30%"]
        })
        result = convert_types(df, strip_characters=["%"])
        # Should convert to numeric (int64 or float64)
        assert result["rate"].dtype in [int, np.int64, float, np.float64]
    
    def test_mixed_numeric_strings(self):
        """Mixed numeric formats should be detected."""
        df = pd.DataFrame({
            "value": ["100", "200.5", "1,000"]
        })
        result = convert_types(df, strip_characters=[","], numeric_threshold=0.6)
        assert result["value"].dtype in [float, np.float64]
    
    def test_threshold_sensitivity(self):
        """High threshold should prevent conversion if many non-numeric."""
        df = pd.DataFrame({
            "mixed": ["100", "200", "abc", "def"]
        })
        result = convert_types(df, numeric_threshold=0.9)
        # Should not convert because < 90% are numeric
        assert result["mixed"].dtype == object
    
    def test_column_selection(self):
        """Should only convert specified columns."""
        df = pd.DataFrame({
            "numeric": ["1", "2", "3"],
            "text": ["a", "b", "c"]
        })
        result = convert_types(df, columns=["numeric"])
        # Should convert to numeric (int or float)
        assert result["numeric"].dtype in [int, np.int64, float, np.float64]
        assert result["text"].dtype == object
    
    def test_coerce_mode(self):
        """Coerce should replace non-numeric with NaN."""
        df = pd.DataFrame({
            "value": ["1", "2", "abc", "4"]
        })
        result = convert_types(df, coerce=True, numeric_threshold=0.6)
        assert pd.isna(result.loc[2, "value"])


class TestTextNormalize:
    """Test text normalization pipeline."""
    
    def test_nbsp_removal(self):
        """Non-breaking spaces should be replaced."""
        df = pd.DataFrame({
            "text": ["hello\u00a0world"]  # NBSP
        })
        result = text_normalize(df, columns=["text"], replace_nbsp_opt=True)
        assert "\u00a0" not in str(result.loc[0, "text"])
    
    def test_quote_normalization(self):
        """Smart quotes should be converted to ASCII."""
        df = pd.DataFrame({
            "text": ["He said \u201cHello\u201d"]  # Smart quotes
        })
        result = text_normalize(df, columns=["text"], normalize_quotes_opt=True)
        assert '"' in str(result.loc[0, "text"])
        assert '\u201c' not in str(result.loc[0, "text"])
    
    def test_whitespace_collapse(self):
        """Multiple spaces should collapse to single."""
        df = pd.DataFrame({
            "text": ["Hello    world   test"]
        })
        result = text_normalize(df, columns=["text"], collapse_whitespace=True)
        assert "Hello world test" in str(result.loc[0, "text"])
    
    def test_html_tag_removal(self):
        """HTML tags should be removed."""
        df = pd.DataFrame({
            "text": ["<p>Hello</p> <b>world</b>"]
        })
        result = text_normalize(df, columns=["text"], strip_html=True)
        assert "<" not in str(result.loc[0, "text"])
        assert "Hello" in str(result.loc[0, "text"])
    
    def test_zero_width_removal(self):
        """Zero-width characters should be removed."""
        df = pd.DataFrame({
            "text": ["hello\u200Bworld"]  # Zero-width space
        })
        result = text_normalize(df, columns=["text"], remove_zw_opt=True)
        assert "\u200B" not in str(result.loc[0, "text"])
    
    def test_nan_preservation(self):
        """NaN values should remain NaN."""
        df = pd.DataFrame({
            "text": ["Hello", np.nan, "World"]
        })
        result = text_normalize(df, columns=["text"])
        assert pd.isna(result.loc[1, "text"])
    
    def test_all_columns_if_none_specified(self):
        """Should normalize all string columns if none specified."""
        df = pd.DataFrame({
            "text1": ["  hello  "],
            "text2": ["  world  "],
            "id": [1]
        })
        result = text_normalize(df)
        # text1 and text2 should be normalized
        assert result.loc[0, "text1"] == "hello"
        assert result.loc[0, "text2"] == "world"


class TestCoreModuleIntegration:
    """Test multiple core modules together."""
    
    def test_pipeline_execution(self):
        """Modules should work together in a pipeline."""
        df = pd.DataFrame({
            "First  Name": ["  Alice  ", "  Bob  ", "  Bob  "],
            "Last Name": ["Smith", "Jones", "Jones"],
            "Age": ["25", "30", "30"]
        })
        
        # Execute pipeline
        df = standardize_headers(df)
        df = trim_spaces(df)
        df = drop_duplicates(df)
        df = convert_types(df)
        
        # Verify results
        assert "first_name" in df.columns
        assert len(df) == 2  # Duplicate removed
        # Should convert to numeric (int or float)
        assert df["age"].dtype in [int, np.int64, float, np.float64]
    
    def test_missing_value_with_other_modules(self):
        """Missing value handling with other modules."""
        df = pd.DataFrame({
            "Name": ["  Alice  ", np.nan, "  Charlie  "],
            "Value": ["100", "200", np.nan]
        })
        
        # Trim first
        df = trim_spaces(df)
        # Then handle missing
        df = handle_missing(df, strategy="drop", columns=["Name", "Value"])
        
        assert len(df) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
