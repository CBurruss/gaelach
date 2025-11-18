from gaelach.core.symbolic import SymbolicAttr
import pandas as pd

# Define the join() verb
def join(other, on=None, left_on=None, right_on=None, how="inner"):
    """
    Join two DataFrames together.
    
    Parameters:
    - other: DataFrame to join with
    - on: Column name(s) to join on (used when column names match)
    - left_on: Column name(s) from left DataFrame
    - right_on: Column name(s) from right DataFrame  
    - how: Join type:
        "inner", "left", "right", "outer", "cross", "semi", "anti"
    
    Usage:
        df >> join(other_df, on="id", how="left")
        df >> join(other_df, left_on="id", right_on="user_id", how="inner")
    """
    def _join(df):
        # Handle semi join (rows in left that have matches in right)
        if how == "semi":
            if on is not None:
                merge_left = merge_right = on
            else:
                merge_left = left_on
                merge_right = right_on
            
            return df[df[merge_left].isin(other[merge_right])]
        
        # Handle anti join (rows in left that have no matches in right)
        elif how == "anti":
            if on is not None:
                merge_left = merge_right = on
            else:
                merge_left = left_on
                merge_right = right_on
            
            return df[~df[merge_left].isin(other[merge_right])]
        
        # Handle standard pandas joins
        else:
            return df.merge(other, on=on, left_on=left_on, right_on=right_on, how=how)
    
    return _join