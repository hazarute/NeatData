# modules/custom/__init__.py

import pandas as pd
from typing import Protocol, runtime_checkable, Any, Dict

"""
NEATDATA CUSTOM PLUGIN STANDARDI
================================
Bu klasöre eklenecek her yeni .py dosyası (plugin) PipelineManager ile uyumlu
olmak için aşağıdaki yapıya sahip olmalıdır.

ZORUNLU YAPILAR:
1. META Sözlüğü: Plugin'in arayüzde nasıl görüneceğini belirler.
2. process Fonksiyonu: Temizlik mantığını içerir. 'run' DEĞİL, 'process' olmalıdır.

ÖRNEK KOD ŞABLONU:
------------------
META = {
    "key": "my_plugin_key",          # Benzersiz ID
    "name": "Plugin Görünen Adı",    # GUI'de görünecek isim
    "description": "Ne işe yarar?",  # Açıklama
    "defaults": {}                   # Varsayılan parametreler (Opsiyonel)
}

def process(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    df_copy = df.copy()
    # İşlemler...
    return df_copy
"""

@runtime_checkable
class NeatDataPlugin(Protocol):
    """
    GitHub Copilot için teknik imza. 
    PipelineManager.py dosyası 'process' fonksiyonunu aradığı için
    burada da 'process' tanımlanmıştır.
    """
    
    # PipelineManager META verisini okur, bu yüzden bu değişkenin varlığı önemlidir.
    META: Dict[str, Any]

    def process(self, df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
        """
        Veri temizleme mantığını uygulayan ana fonksiyon.
        
        Args:
            df (pd.DataFrame): Temizlenecek ham veri.
            **kwargs: META['defaults'] içindeki parametreler buraya gelir.
            
        Returns:
            pd.DataFrame: Temizlenmiş veri.
        """
        ...