from gaelach.core.symbolic import SymbolicAttr

def sample(n=None, frac=None, with_replacement=False, shuffle=False, seed=None):
    """
    Sample rows from a DataFrame.
    
    n: Number of rows to sample (integer)
    frac: Fraction of rows to sample (float between 0 and 1)
    with_replacement: Whether to sample with replacement (default False)
    shuffle: Whether to shuffle before sampling (default False)
    seed: Random seed for reproducibility
    
    Returns a function that samples from a DataFrame when piped.
    
    Usage: df >> sample(n=10) or df >> sample(frac=0.1)
    """
    def _sample(df):

        result = df.sample(n=n, frac=frac, replace=with_replacement, 
                          random_state=seed)
        
        # If shuffle=True and no sampling, just shuffle all rows
        if shuffle and n is None and frac is None:
            result = df.sample(frac=1.0, random_state=seed)
        return result
    
    return _sample