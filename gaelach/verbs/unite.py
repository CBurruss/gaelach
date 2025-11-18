from gaelach.core.symbolic import SymbolicAttr
import pandas as pd
import warnings

def unite(new_col, from_cols, sep="_", drop=True):
    """
    Combine multiple columns into one with a separator.
    
    new_col: Name of the new column to create
    from_cols: List of SymbolicAttr column references or column names
    sep: Separator string (default "_")
    drop: Whether to drop source columns (default True)
    
    Returns a function that takes a DataFrame and returns the modified DataFrame
    
    Usage: df >> unite("combined", [_.col1, _.col2], sep="-")
    """
    def _unite(df):
        # Extract column names from SymbolicAttr objects
        col_names = []
        for col in from_cols:
            if isinstance(col, SymbolicAttr):
                col_names.append(col.name)
            else:
                col_names.append(col)
        
        # Create a copy to avoid modifying original
        result = df.copy()
        
        # Convert columns to string and fill NaN with empty string, then concatenate
        result[new_col] = result[col_names].fillna("").astype(str).agg(sep.join, axis=1)
        
        # Drop source columns if requested
        if drop:
            result = result.drop(columns=col_names)
        
        return result
    
    return _unite