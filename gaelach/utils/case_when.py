import pandas as pd
import numpy as np

def case_when(*conditions, default=None):
    """
    Vectorized multi-condition case statement (similar to SQL CASE WHEN).
    
    Parameters:
    -----------
    *conditions : tuples of (condition, value)
        Each tuple contains a condition expression and the value to return
        Conditions are evaluated in order
    default : scalar, expression, or SymbolicAttr, optional
        Value to return when no conditions are met (default: None)
    
    Returns:
    --------
    Function that applies case logic
    """
    
    if not conditions:
        raise ValueError("case_when requires at least one condition")
    
    def _case_when(df):
        # Evaluate default value
        if callable(default):
            default_val = default(df)
        elif hasattr(default, '_evaluate'):
            default_val = default._evaluate(df)
        else:
            default_val = default
        
        # Start with default value for all rows
        result = pd.Series([default_val] * len(df), index=df.index)
        
        # Apply conditions in reverse order (later conditions override earlier)
        for condition, value in reversed(conditions):
            # Evaluate condition
            if callable(condition):
                cond = condition(df)
            elif hasattr(condition, '_evaluate'):
                cond = condition._evaluate(df)
            else:
                cond = condition
            
            # Evaluate value
            if callable(value):
                val = value(df)
            elif hasattr(value, '_evaluate'):
                val = value._evaluate(df)
            else:
                val = value
            
            result = np.where(cond, val, result)
        
        return result
    
    return _case_when