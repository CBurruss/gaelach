from gaelach.core.symbolic import SymbolicAttr, ChainedSymbolicAttr
from gaelach.verbs.mutate import _resolve_across_columns, Across, _evaluate_expression
import pandas as pd

def reframe(*args, **kwargs):
    """
    Group-wise computation that creates new rows based on group summaries.
    Unlike mutate(), reframe() can change the number of rows.
    
    *args: Across objects (used without keyword assignment)
    **kwargs: Column names as keys, pandas expressions as values
    
    Returns a function that performs the reframe operation on a DataFrame or GroupBy.
    """
    # Capture parameters in outer scope to avoid UnboundLocalError
    outer_args = args
    outer_kwargs = kwargs
    
    def _reframe(df_or_group):
        # Determine if we're working with a grouped DataFrame
        is_grouped = isinstance(df_or_group, pd.core.groupby.GroupBy)
        df = df_or_group.obj if is_grouped else df_or_group
        
        # First, expand any across() calls
        expanded_kwargs = {}
        
        # Handle positional Across objects
        for arg in outer_args:
            if isinstance(arg, Across):
                target_cols = _resolve_across_columns(arg.cols, df.columns, df)
                
                for col_name in target_cols:
                    col_series = df[col_name]
                    result_value = arg.func(col_series)
                    
                    if arg.names:
                        output_name = arg.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_value
        
        # Handle keyword arguments
        for key, value in outer_kwargs.items():
            if isinstance(value, Across):
                target_cols = _resolve_across_columns(value.cols, df.columns, df)
                
                for col_name in target_cols:
                    col_series = df[col_name]
                    result_value = value.func(col_series)
                    
                    if value.names:
                        output_name = value.names.format(col=col_name)
                    else:
                        output_name = col_name
                    
                    expanded_kwargs[output_name] = result_value
            else:
                expanded_kwargs[key] = value
        
        # If grouped, perform aggregation similar to summarize
        if is_grouped:
            agg_dict = {}
            post_agg_operations = {}
            
            for new_name, expr in expanded_kwargs.items():
                if isinstance(expr, ChainedSymbolicAttr):
                    # Walk the chain to separate pre/post aggregation operations
                    current = expr
                    operations = []
                    
                    while isinstance(current, ChainedSymbolicAttr):
                        operations.append((current.method_name, current.args, current.kwargs))
                        current = current.parent
                    
                    operations.reverse()
                    
                    # Find aggregation method
                    agg_idx = next((i for i, (m, _, _) in enumerate(operations) 
                                   if m in ['count', 'sum', 'mean', 'min', 'max', 'std', 'var', 
                                           'first', 'last', 'median', 'unique', 'nunique', 'tolist']), 
                                  None)
                    
                    if agg_idx is not None:
                        pre_agg = operations[:agg_idx]
                        agg_method_name = operations[agg_idx][0]
                        post_agg = operations[agg_idx+1:]
                        
                        def make_agg_func(pre_ops, agg_name):
                            def agg_func(series):
                                result = series
                                for method_name, args, kw in pre_ops:
                                    if hasattr(result, method_name):
                                        method = getattr(result, method_name)
                                        result = method(*args, **kw)
                                agg_method = getattr(result, agg_name)
                                return agg_method()
                            return agg_func
                        
                        agg_dict[new_name] = pd.NamedAgg(column=expr.name, aggfunc=make_agg_func(pre_agg, agg_method_name))
                        
                        if post_agg:
                            post_agg_operations[new_name] = post_agg
                
                elif isinstance(expr, SymbolicAttr):
                    if hasattr(expr, '_agg_func'):
                        agg_dict[new_name] = pd.NamedAgg(column=expr.name, aggfunc=expr._agg_func)
                    else:
                        agg_dict[new_name] = pd.NamedAgg(column=expr.name, aggfunc='first')
                else:
                    # Literal or callable
                    agg_dict[new_name] = expr
            
            result = df_or_group.agg(**agg_dict)
            
            # Apply post-aggregation operations
            for col_name, operations in post_agg_operations.items():
                for method_name, args, kw in operations:
                    if hasattr(result[col_name], method_name):
                        method = getattr(result[col_name], method_name)
                        result[col_name] = method(*args, **kw)
            
            return result
        else:
            # Ungrouped: evaluate expressions and create new DataFrame
            result_dict = {}
            for new_name, expr in expanded_kwargs.items():
                evaluated = _evaluate_expression(expr, df)
                result_dict[new_name] = evaluated if isinstance(evaluated, (list, pd.Series)) else [evaluated]
            
            return pd.DataFrame(result_dict)
    
    return _reframe