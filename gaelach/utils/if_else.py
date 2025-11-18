import numpy as np

def if_else(condition, true, false):
    """
    Vectorized if-else statement for creating conditional columns.
    
    Parameters:
    -----------
    condition : callable, Series, or boolean
        The condition to evaluate
    true : scalar or callable
        Value to return when condition is True
    false : scalar or callable
        Value to return when condition is False
    
    Returns:
    --------
    Function that applies conditional logic
    """
    
    def _if_else(df):
        # Evaluate condition
        if callable(condition):
            cond = condition(df)
        elif hasattr(condition, '_evaluate'):
            # Handle SymbolicAttr/ChainedSymbolicAttr with _evaluate method
            cond = condition._evaluate(df)
        else:
            cond = condition
        
        # Evaluate true/false values
        if callable(true):
            true_val = true(df)
        elif hasattr(true, '_evaluate'):
            true_val = true._evaluate(df)
        else:
            true_val = true
        
        if callable(false):
            false_val = false(df)
        elif hasattr(false, '_evaluate'):
            false_val = false._evaluate(df)
        else:
            false_val = false
        
        # Use numpy.where for vectorized conditional
        return np.where(cond, true_val, false_val)
    
    return _if_else