from gaelach.core.symbolic import SymbolicAttr
import pandas as pd

def bind_rows(*dfs):
    """
    Stack DataFrames vertically (row-wise).
    
    *dfs: Variable number of DataFrames to bind
    
    Returns a function that takes a DataFrame and concatenates it with the others
    Uses union of all columns (fills missing with NaN)
    
    Usage: df >> bind_rows(df2, df3)
    """
    def _bind_rows(df):
        # Combine the piped df with the additional dfs
        all_dfs = [df] + list(dfs)
        
        # Concatenate with union of columns, ignore index
        return pd.concat(all_dfs, axis=0, ignore_index=True, sort=False)
    
    return _bind_rows