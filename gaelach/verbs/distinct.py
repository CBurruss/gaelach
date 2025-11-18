from gaelach.core.symbolic import SymbolicAttr

def distinct(*args):
    """
    Keep only unique rows based on specified columns.
    
    *args: Column names (strings) or symbolic columns
           If no columns specified, uses all columns
    
    Returns a function that removes duplicate rows.
    """
    def _distinct(df):
        if not args:
            return df.drop_duplicates()
        else:
            cols = []
            for arg in args:
                if isinstance(arg, SymbolicAttr):
                    cols.append(arg.name)
                else:
                    cols.append(arg)
            return df.drop_duplicates(subset=cols)
    
    return _distinct