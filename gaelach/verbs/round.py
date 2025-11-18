# Define the round() verb
import pandas as pd
from gaelach.core.symbolic import SymbolicAttr

def round(*args, decimals=2):
    """
    Round numeric columns to specified decimal places.
    
    *args: Column names (strings) or symbolic columns to round
           If no columns specified, rounds all numeric columns
    decimals: Number of decimal places (default: 2)
    
    Returns a function that performs the rounding on a DataFrame.
    """
    def _round(df):
        if not args:
            # Round all numeric columns
            # select_dtypes() filters columns by data type
            # include=['number'] selects all numeric types (int, float)
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                # Create a copy to avoid modifying original
                df = df.copy()
                # Apply round() to all numeric columns at once
                df[numeric_cols] = df[numeric_cols].round(decimals)
            return df
        else:
            # Round specified columns
            df = df.copy()
            for arg in args:
                # Extract column name from SymbolicAttr or use string directly
                col_name = arg.name if isinstance(arg, SymbolicAttr) else arg
                df[col_name] = df[col_name].round(decimals)
            return df
    
    return _round