import unittest
import pandas as pd
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.custom.fix_cafe_business_logic import run


class TestCafeBusinessLogic(unittest.TestCase):
    """fix_cafe_business_logic modülü için test sınıfı"""

    def setUp(self):
        """Her test öncesi temizlik"""
        # Silme log dosyası varsa sil
        if os.path.exists("deleted_records_log.csv"):
            os.remove("deleted_records_log.csv")

    def tearDown(self):
        """Her test sonrası temizlik"""
        if os.path.exists("deleted_records_log.csv"):
            os.remove("deleted_records_log.csv")

    def test_column_naming_variations(self):
        """Sütun ismi varyasyonlarının tanınıp tanınmadığını test et"""
        # Farklı sütun isimleri ile DataFrame oluştur
        df = pd.DataFrame({
            "TransactionID": [1, 2],
            "Item": ["Coffee", "Tea"],
            "Total_Spent": [5.50, 3.00],
            "OrderDate": ["2023-01-01", "2023-01-02"]
        })

        result = run(df)

        # Sonuç boş olmadığını ve temizlenmiş sütunları içerdiğini kontrol et
        self.assertGreater(len(result), 0)
        self.assertIn("Cleaned_Price", result.columns)
        self.assertIn("Cleaned_Date", result.columns)

    def test_price_parsing(self):
        """Fiyat parsing'inin düzgün çalışıp çalışmadığını test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2, 3],
            "Item Ordered": ["Espresso", "Cappuccino", "Tea"],
            "Total Spent": ["$5.50", "€3.20", "£2.75"],
            "Transaction Date": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })

        result = run(df)

        # Temizlenmiş fiyatların sayısal olduğunu kontrol et
        prices = pd.to_numeric(result["Cleaned_Price"], errors="coerce")
        self.assertTrue((prices > 0).all())
        self.assertAlmostEqual(prices.iloc[0], 5.50, places=1)

    def test_date_parsing_flexible(self):
        """Esnek tarih parsing'ini test et"""
        df = pd.DataFrame({
            "Txn ID": [1, 2],
            "Item": ["Coffee", "Tea"],
            "Amount": [5.50, 3.20],
            "Order Date": ["2023-02-15", "2023-01-10"]
        })

        result = run(df)

        # Tarih sütununun olduğunu ve geçerli olduğunu kontrol et
        self.assertIn("Cleaned_Date", result.columns)
        self.assertGreater(len(result), 0)

    def test_duplicate_removal(self):
        """Mükerrer satırların silinip silinmediğini test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 1, 2],
            "Item Ordered": ["Coffee", "Coffee", "Tea"],
            "Total Spent": [5.50, 5.50, 3.00],
            "Transaction Date": ["2023-01-01", "2023-01-01", "2023-01-02"]
        })

        result = run(df)

        # Mükerrer satırın silinmiş olduğunu kontrol et
        self.assertEqual(len(result), 2)

    def test_invalid_price_logging(self):
        """Geçersiz fiyatların log dosyasına yazıldığını test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2],
            "Item Ordered": ["Coffee", "Tea"],
            "Total Spent": ["$5.50", "INVALID_PRICE"],
            "Transaction Date": ["2023-01-01", "2023-01-02"]
        })

        result = run(df)

        # Geçersiz satırın silinmiş olduğunu kontrol et
        self.assertEqual(len(result), 1)

        # Log dosyasının oluşturulup oluşturulmadığını kontrol et
        self.assertTrue(os.path.exists("deleted_records_log.csv"))
        
        log_df = pd.read_csv("deleted_records_log.csv")
        self.assertGreater(len(log_df), 0)
        self.assertIn("Reason", log_df.columns)

    def test_invalid_date_logging(self):
        """Geçersiz tarihlerin log dosyasına yazıldığını test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2],
            "Item Ordered": ["Coffee", "Tea"],
            "Total Spent": [5.50, 3.00],
            "Transaction Date": ["2023-01-01", "NOT_A_DATE"]
        })

        result = run(df)

        # Geçersiz satırın silinmiş olduğunu kontrol et
        self.assertEqual(len(result), 1)

        # Log dosyasının geçersiz tarih nedenini içerdiğini kontrol et
        self.assertTrue(os.path.exists("deleted_records_log.csv"))
        log_df = pd.read_csv("deleted_records_log.csv")
        self.assertTrue((log_df["Reason"].str.contains("Date", na=False)).any())

    def test_item_normalization(self):
        """Ürün isimlerinin normalizasyonunu test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2, 3],
            "Item Ordered": ["expresso", "cappucino", "tea - hot"],
            "Total Spent": [5.50, 4.00, 3.00],
            "Transaction Date": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })

        result = run(df)

        # Normalizasyon sonuçlarını kontrol et
        items = result["Item Ordered"].tolist()
        self.assertIn("Espresso", items)  # "expresso" -> "Espresso"
        self.assertIn("Cappuccino", items)  # "cappucino" -> "Cappuccino"
        self.assertIn("Tea", items)  # "tea - hot" -> "Tea"

    def test_placeholder_tokens_to_missing(self):
        """Placeholder token'ların missing value'ya dönüştürülmesini test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2, 3],
            "Item Ordered": ["Coffee", "UNKNOWN", "N/A"],
            "Total Spent": [5.50, 3.00, 2.50],
            "Transaction Date": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })

        result = run(df)

        # Placeholder token'ların NaN'a dönüştürüldüğünü kontrol et
        self.assertFalse((result["Item Ordered"] == "UNKNOWN").any())
        self.assertFalse((result["Item Ordered"] == "N/A").any())

    def test_quantity_to_numeric(self):
        """Quantity sütununun numeric'e dönüştürüldüğünü test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2, 3],
            "Item": ["Coffee", "Tea", "Cappuccino"],
            "Price Per Unit": [5.00, 3.00, 4.00],
            "Quantity": ["2", "1", "3"],
            "OrderDate": ["2023-01-01", "2023-01-02", "2023-01-03"]
        })

        result = run(df)

        # Quantity sütununun numeric olduğunu kontrol et
        if "Quantity" in result.columns:
            self.assertTrue(pd.api.types.is_integer_dtype(result["Quantity"]) or 
                          pd.api.types.is_numeric_dtype(result["Quantity"]))

    def test_price_computation_from_components(self):
        """Price Per Unit * Quantity ile fiyat hesaplamasını test et"""
        df = pd.DataFrame({
            "Transaction ID": [1, 2],
            "Item": ["Coffee", "Tea"],
            "Price Per Unit": [2.50, 1.50],
            "Quantity": [2, 3],
            "OrderDate": ["2023-01-01", "2023-01-02"]
        })

        result = run(df)

        # Hesaplanan fiyatları kontrol et
        prices = pd.to_numeric(result["Cleaned_Price"], errors="coerce")
        self.assertAlmostEqual(prices.iloc[0], 5.00, places=1)  # 2.50 * 2
        self.assertAlmostEqual(prices.iloc[1], 4.50, places=1)  # 1.50 * 3

    def test_empty_dataframe(self):
        """Boş DataFrame'in işlenmesini test et"""
        df = pd.DataFrame({
            "Transaction ID": [],
            "Item Ordered": [],
            "Total Spent": [],
            "Transaction Date": []
        })

        result = run(df)

        # Sonuç boş olmalı
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
