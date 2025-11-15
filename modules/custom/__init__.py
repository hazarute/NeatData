"""Custom Plugins Directory - Organisation-specific cleaning logic.

This directory contains custom cleaning plugins that extend NeatData's core functionality.
The PipelineManager dynamically imports every .py file in this folder.

PLUGIN STRUCTURE TEMPLATE:
==========================

Each plugin must follow this structure:

    ```python
    # modules/custom/my_plugin.py
    import pandas as pd
    from typing import Optional, List
    
    # Metadata describing the plugin
    META = {
        "key": "my_plugin",              # Unique identifier (used in CLI/GUI)
        "name": "My Custom Plugin",      # Display name
        "description": "Cleans specific data in our domain",  # Description
        "parameters": {
            "columns": {
                "type": "list",
                "description": "Columns to clean",
                "default": []
            }
        },
        "defaults": {}
    }
    
    def process(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        '''
        Main processing function.
        
        Args:
            df: Input dataframe
            **kwargs: Additional parameters (e.g., columns=['col1', 'col2'])
            
        Returns:
            Cleaned dataframe
        '''
        df_copy = df.copy()
        
        # Your custom cleaning logic here
        # Example: Clean specific columns, fix formats, standardize values
        columns = kwargs.get("columns", [])
        if columns:
            for col in columns:
                if col in df_copy.columns:
                    # Apply your custom logic
                    df_copy[col] = df_copy[col].str.strip().str.lower()
        
        return df_copy
    ```

GUIDELINES:
===========
1. Always work on a copy: `df_copy = df.copy()` to avoid modifying the original
2. META dict must include: key, name, description, parameters, defaults
3. process() must accept **kwargs for flexible parameterization
4. Keep the function stateless (no side effects)
5. Handle missing values gracefully (check if columns exist)
6. Return the cleaned dataframe
7. Plugin errors are logged but don't stop the pipeline

EXAMPLES:
=========
- clean_hepsiburada_scrape.py: Site-specific e-commerce data cleaning
- fix_cafe_business_logic.py: Business domain-specific logic (CSV logging, date parsing)
- Future HR plugins: clean_currency, clean_phone_format, clean_dates

REGISTRATION:
=============
Once created, plugins are automatically discovered by PipelineManager.
Use in CLI:  python -m modules.cli_handler --input data.csv --custom-modules my_plugin
Use in GUI:  GUI module selection panel automatically includes your plugin
"""
