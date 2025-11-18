from gaelach.core.symbolic import SymbolicAttr
import pandas as pd
import warnings

def bind_cols(*dfs, suffix="_2"):
    """
    Join DataFrames horizontally (column-wise).
    
    *dfs: Variable number of DataFrames to bind
    suffix: Suffix to add to duplicate column names (default "_2")
    
    Returns a function that takes a DataFrame and horizontally stacks it with others
    Aligns by row position, fills with NaN if row counts don't match
    
    Usage: df >> bind_cols(df2, df3)
    """
    def _bind_cols(df):
        result = df.copy()
        
        # Check row counts and warn if mismatched
        all_dfs = [df] + list(dfs)
        max_rows = max(d.shape[0] for d in all_dfs)
        
        if df.shape[0] < max_rows:
            warnings.warn(
                f"Row count mismatch: primary DataFrame has {df.shape[0]} rows "
                f"but maximum is {max_rows}. Filling with NaNs."
            )
        
        for other_df in dfs:
            if other_df.shape[0] < max_rows:
                warnings.warn(
                    f"Row count mismatch: a DataFrame has {other_df.shape[0]} rows "
                    f"but maximum is {max_rows}. Filling with NaNs."
                )
        
        for other_df in dfs:
            # Reset index to align by position
            other_reset = other_df.reset_index(drop=True)
            
            # Check for duplicate column names
            result_cols = set(result.columns)
            other_cols = set(other_reset.columns)
            duplicate_cols = result_cols & other_cols
            
            if duplicate_cols:
                # Rename duplicates in other_df
                rename_map = {}
                for col in duplicate_cols:
                    base_name = col
                    counter = 2
                    new_name = f"{base_name}{suffix}"
                    
                    # Keep incrementing if still duplicate
                    while new_name in result_cols or new_name in other_cols:
                        counter += 1
                        new_name = f"{base_name}_{counter}"
                    
                    rename_map[col] = new_name
                
                other_reset = other_reset.rename(columns=rename_map)
            
            # Stack horizontally using concat
            result = pd.concat([result.reset_index(drop=True), other_reset], axis=1)
        
        return result
    
    return _bind_cols