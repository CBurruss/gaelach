from gaelach.core.symbolic import SymbolicAttr

# Define the drop_na() verb
def drop_na(subset=None, how="any"):
    """
    Remove rows with null values.
    
    subset: Column name(s) to check for nulls. If None, checks all columns.
            Can be a string, list of strings, or SymbolicAttr
            
    how: Whether drop_na() checks for all NA values, or any NA values
         Where the default is "all"
        
    Usage: df >> drop_na() 
        df >> drop_na("column") 
        df >> drop_na(["col1", "col2"], how="any")
    """
    def _drop_na(df):
        # Handle SymbolicAttr objects
        if hasattr(subset, 'name'):
            cols = subset.name
        else:
            cols = subset
        return df.dropna(subset=cols, how=how, axis=0)
    return _drop_na