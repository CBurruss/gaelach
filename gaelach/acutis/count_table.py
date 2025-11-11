import pandas as pd
import numpy as np

def count_table(self):
    """
    count_table extension for Pandas Series.

    This module monkey-patches the count_table() method onto pd.Series.
    The patch is applied automatically when this module is imported.

    Usage: series.count_table() or df["column"].count_table()
    """
    # Get value counts and convert to DataFrame
    table = self.value_counts(dropna = False).reset_index()
    table.columns = [self.name or "value", "count"]
    
    # Calculate percentages
    table["percent"] = (table["count"] / table["count"].sum() * 100).round(0).astype(int).astype(str) + "%"
    
    # Handle the <1% case
    table["percent"] = np.where(
        (table["percent"] == "0%") & (table["count"] != 0),
        "<1%",
        table["percent"]
    )
    
    return table

# Monkey patch the method onto Series
pd.Series.count_table = count_table