from gaelach.core.symbolic import SymbolicAttr
import pandas as pd
import warnings

def separate(col, into, sep, regex=False, drop=True, fill="right"):
    """
    Split one column into multiple columns.
    
    col: SymbolicAttr or string name of column to split
    into: List of new column names
    sep: Separator string or regex pattern
    regex: Whether sep is a regex pattern (default False)
    drop: Whether to drop source column (default True)
    fill: How to handle too few splits - "right", "left", or "error" (default "right")
    
    Returns a function that takes a DataFrame and returns the modified DataFrame
    
    Usage: df >> separate(_.col, into=["a", "b"], sep="_")
    """
    def _separate(df):
        # Extract column name
        col_name = col.name if isinstance(col, SymbolicAttr) else col
        
        # Create a copy to avoid modifying original
        result = df.copy()
        
        # Get column index for reordering later
        col_idx = result.columns.get_loc(col_name)
        
        # Split the column
        split_data = result[col_name].str.split(sep, regex=regex, expand=True)
        
        # Check split counts and warn if mismatched
        split_lengths = split_data.notna().sum(axis=1)
        max_len = split_lengths.max()
        min_len = split_lengths.min()
        expected_len = len(into)
        
        if max_len > expected_len:
            warnings.warn(
                f"Some splits produced {max_len} parts but only {expected_len} columns requested. "
                f"Extra parts will be ignored."
            )
        
        if min_len < expected_len and fill == "error":
            raise ValueError(
                f"Some splits produced fewer than {expected_len} parts. "
                f"Use fill='right' or fill='left' to handle this."
            )
        
        # Handle fill strategies
        if fill == "left":
            # Align columns to the right
            for i, col_name_new in enumerate(into):
                # Calculate which split column to pull from (counting from right)
                idx = split_data.shape[1] - expected_len + i
                if idx >= 0 and idx < split_data.shape[1]:
                    result[col_name_new] = split_data.iloc[:, idx]
                else:
                    result[col_name_new] = None
        else:  # "right" or "error"
            # Take first n columns from split
            for i, col_name_new in enumerate(into):
                if i < split_data.shape[1]:
                    result[col_name_new] = split_data.iloc[:, i]
                else:
                    result[col_name_new] = None
        
        # Reorder columns to insert new ones after original
        original_cols = list(df.columns)
        
        if drop:
            # Remove source column and insert new ones at its position
            reordered = (
                original_cols[:col_idx] + 
                into + 
                original_cols[col_idx + 1:]
            )
        else:
            # Insert new columns after source column
            reordered = (
                original_cols[:col_idx + 1] + 
                into + 
                original_cols[col_idx + 1:]
            )
        
        result = result[reordered]
        
        return result
    
    return _separate