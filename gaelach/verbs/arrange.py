from gaelach.core.symbolic import SymbolicAttr, ChainedSymbolicAttr

# Define the arrange() verb
def arrange(*args, descending=False):
    """
    Sort rows by column expressions.
    
    *args: Column names (strings) or symbolic columns
           Use _.column_name for ascending
           Use -_.column_name for descending
    descending: If True, reverses all sort orders (default: False)
    
    Returns a function that performs the sort on a DataFrame.
    """
    def _arrange(df):
        cols = []
        desc_flags = []
        
        for arg in args:
            if isinstance(arg, SymbolicAttr):
                try:
                    is_negated = object.__getattribute__(arg, '_is_negated')
                    original = object.__getattribute__(arg, '_original')
                    cols.append(original)
                    desc_flags.append(True)
                except AttributeError:
                    # Not negated
                    col_name = object.__getattribute__(arg, '_column_name')
                    cols.append(col_name)
                    desc_flags.append(False)
            elif isinstance(arg, ChainedSymbolicAttr):
                cols.append(arg.name)
                desc_flags.append(False)
            else:
                cols.append(arg)
                desc_flags.append(False)
        
        if descending:
            desc_flags = [not flag for flag in desc_flags]
        
        # pandas uses ascending parameter (opposite of descending)
        ascending_flags = [not flag for flag in desc_flags]
        return df.sort_values(by=cols, ascending=ascending_flags)
    
    return _arrange