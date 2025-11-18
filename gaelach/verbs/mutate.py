from gaelach.core.symbolic import SymbolicAttr, BinaryOperation, ChainedSymbolicAttr, ColumnExpression
import pandas as pd
import re
import numpy as np

from gaelach.utils.helpers import (
    WhereSelector,
    where,
    is_numeric,
    is_integer,
    is_float,
    is_object,
    is_boolean,
    is_temporal,
    is_cat,
    all
)

# Define Across class (same as before)
class Across:
    """
    Represents an across() operation for mutating multiple columns.
    
    Applies a function to multiple columns selected by pattern or list.
    """
    def __init__(self, cols, func, names=None):
        self.cols = cols
        self.func = func
        self.names = names  # Optional naming pattern like "{col}_new"

# Define across() helper function (same as before)
def across(cols, func, names=None):
    """
    Apply a function across multiple columns.
    
    cols: Column selector (list of strings/SymbolicAttr, or selector function like starts_with())
    func: Function to apply to each column (should accept a pandas Series)
    names: Optional naming pattern with {col} placeholder, e.g. "{col}_log"
    
    Usage:
        df >> mutate(across([_.col1, _.col2], lambda x: x * 2))
        df >> mutate(across(starts_with("bill"), lambda x: np.log(x)))
    """
    return Across(cols, func, names)

# Define resolve_across_columns() helper function (adapted for pandas)
def _resolve_across_columns(cols, all_columns, df=None):
    """
    Resolve column specifications for across() to actual column names.
    
    cols: Column specification (list, selector function, or single column)
    all_columns: List of all column names in the DataFrame
    df: The DataFrame (needed for where() selectors to check dtypes)
    
    Returns a list of column names to operate on.
    """
    from gaelach.utils.helpers import StartsWithSelector, EndsWithSelector, ContainsSelector
    
    # Handle where() selector
    if isinstance(cols, WhereSelector):
        if df is None:
            raise ValueError("DataFrame required for where() selector")
        else:
            return [col for col in all_columns if cols.predicate(df[col].dtype)]
    
    # Handle selector functions
    if isinstance(cols, StartsWithSelector):
        if cols.is_regex:
            pattern = re.compile(f"({cols.prefix})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if col.startswith(cols.prefix)]
    
    if isinstance(cols, EndsWithSelector):
        if cols.is_regex:
            pattern = re.compile(f"({cols.suffix})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if col.endswith(cols.suffix)]
    
    if isinstance(cols, ContainsSelector):
        if cols.is_regex:
            pattern = re.compile(f"({cols.substring})$")
            return [col for col in all_columns if pattern.search(col)]
        else:
            return [col for col in all_columns if cols.substring in col]
    
    # Handle list of columns
    if isinstance(cols, list):
        result = []
        for col in cols:
            if isinstance(col, SymbolicAttr):
                result.append(col.name)
            elif isinstance(col, str):
                result.append(col)
        return result
    
    # Handle single column
    if isinstance(cols, SymbolicAttr):
        return [cols.name]
    
    if isinstance(cols, str):
        return [cols]
    
    return []

def _evaluate_expression(expr, df):
    """Helper to evaluate symbolic expressions into actual values."""
    # Handle callables (like if_else, case_when results)
    if callable(expr):
        return expr(df)
    elif isinstance(expr, ChainedSymbolicAttr):
        # Start with the base column
        result = df[expr.name]
        current = expr
        operations = []
        
        # Collect all operations in the chain
        while isinstance(current, ChainedSymbolicAttr):
            operations.append((current.method_name, current.args, current.kwargs))
            current = current.parent
        
        # Apply operations in reverse order
        for method_name, args, kw in reversed(operations):
            if hasattr(result, method_name):
                method = getattr(result, method_name)
                result = method(*args, **kw)
        
        return result
    elif isinstance(expr, SymbolicAttr):
        return df[expr.name]
    elif isinstance(expr, BinaryOperation):
        return expr._evaluate(df)
    elif isinstance(expr, ColumnExpression):
        return expr._evaluate(df)
    else:
        return expr

def mutate(*args, _before=None, _after=None, **kwargs):
    """
    Create new columns or modify existing ones.
    
    *args: Across objects (used without keyword assignment)
    **kwargs: Column names as keys, pandas expressions as values
              Use _ to reference columns: _.column_name
              Lists will be automatically converted to Series
              Use across() to apply functions to multiple columns
    _before: Column name (string) to place new columns before
    _after: Column name (string) to place new columns after
    
    Returns a function that performs the mutation on a DataFrame.
    """
    def _mutate(df):
        # Make a copy to avoid modifying the original
        result = df.copy()
        
        # First, expand any across() calls
        expanded_kwargs = {}
        
        # Handle positional Across objects
        for arg in args:
            if isinstance(arg, Across):
                target_cols = _resolve_across_columns(arg.cols, df.columns, df)
                
                for col_name in target_cols:
                    # Get the pandas Series for this column
                    col_series = df[col_name]
                    # Apply the function
                    result_series = arg.func(col_series)
                    
                    if arg.names:
                        output_name = arg.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_series
        
        # Handle keyword arguments (including Across objects)
        for key, value in kwargs.items():
            if isinstance(value, Across):
                target_cols = _resolve_across_columns(value.cols, df.columns, df)
                
                for col_name in target_cols:
                    col_series = df[col_name]
                    result_series = value.func(col_series)
                    
                    if value.names:
                        output_name = value.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_series
            else:
                expanded_kwargs[key] = value
        
        # Apply all the mutations
        for col_name, value in expanded_kwargs.items():
            # Evaluate the expression first
            evaluated_value = _evaluate_expression(value, result)
            
            # Handle lists/arrays by converting to pandas Series
            if isinstance(evaluated_value, (list, np.ndarray)):
                if len(evaluated_value) != len(df):
                    raise ValueError(f"Length of values ({len(evaluated_value)}) must match DataFrame length ({len(df)})")
                result[col_name] = evaluated_value
            elif hasattr(evaluated_value, '__len__') and not isinstance(evaluated_value, (str, pd.Series)):
                # Handle other sequence-like objects
                if len(evaluated_value) != len(df):
                    raise ValueError(f"Length of values ({len(evaluated_value)}) must match DataFrame length ({len(df)})")
                result[col_name] = pd.Series(evaluated_value, index=df.index)
            else:
                # Handle scalar values, Series, or expressions
                result[col_name] = evaluated_value
        
        # If positioning is specified, reorder columns
        if _before is not None or _after is not None:
            new_col_names = list(expanded_kwargs.keys())
            existing_columns = df.columns.tolist()
            
            # Remove new columns from existing columns list
            other_cols = [c for c in existing_columns if c not in new_col_names]
            
            if _before is not None:
                if _before not in other_cols:
                    raise ValueError(f"Column '{_before}' not found in DataFrame")
                anchor_idx = other_cols.index(_before)
                new_order = other_cols[:anchor_idx] + new_col_names + other_cols[anchor_idx:]
            else:
                if _after not in other_cols:
                    raise ValueError(f"Column '{_after}' not found in DataFrame")
                anchor_idx = other_cols.index(_after)
                new_order = other_cols[:anchor_idx + 1] + new_col_names + other_cols[anchor_idx + 1:]
            
            result = result[new_order]
        
        return result
    
    return _mutate