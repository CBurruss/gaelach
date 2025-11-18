from gaelach.core.symbolic import SymbolicAttr, ChainedSymbolicAttr
import pandas as pd

# Define the summarize() verb
def summarize(**kwargs):
    """
    Aggregate data, typically after group_by().
    
    **kwargs: Column names as keys, aggregation expressions as values
              Use _.column_name with aggregation methods
    
    Returns a function that performs the aggregation on a DataFrame or GroupBy.
    """
    def _summarize(df_or_group):
        # Check if grouped or ungrouped
        if isinstance(df_or_group, pd.core.groupby.GroupBy):
            # Grouped: build aggregation dict
            agg_dict = {}
            post_agg_operations = {}  # Store operations to apply after aggregation
            
            for new_name, expr in kwargs.items():
                if isinstance(expr, ChainedSymbolicAttr):
                    # Walk the chain to find the aggregation and separate pre/post operations
                    current = expr
                    operations = []
                    agg_method = None
                    
                    while isinstance(current, ChainedSymbolicAttr):
                        operations.append((current.method_name, current.args, current.kwargs))
                        if current.method_name in ['count', 'sum', 'mean', 'min', 'max', 'std', 'var', 'first', 'last', 'median']:
                            agg_method = current.method_name
                        current = current.parent
                    
                    operations.reverse()
                    
                    # Split operations into pre-agg and post-agg
                    agg_idx = next((i for i, (m, _, _) in enumerate(operations) 
                                   if m in ['count', 'sum', 'mean', 'min', 'max', 'std', 'var', 'first', 'last', 'median']), 
                                  None)
                    
                    if agg_idx is not None:
                        pre_agg = operations[:agg_idx]
                        agg_method_name = operations[agg_idx][0]  # Get the aggregation method name
                        post_agg = operations[agg_idx+1:]
    
                        # Create aggregation function that includes pre-processing AND aggregation
                        def make_agg_func(pre_ops, agg_name):
                            def agg_func(series):
                                result = series
                                # Apply pre-processing
                                for method_name, args, kw in pre_ops:
                                    if method_name == 'astype':
                                        target_type = args[0] if args else kw.get('dtype')
                                        if target_type in ["Int64", "Float64"]:
                                            result = pd.to_numeric(result, errors='coerce')
                                            if target_type == "Int64":
                                                result = result.astype('float64').astype('Int64')
                                            else:
                                                result = result.astype('Float64')
                                        else:
                                            result = result.astype(*args, **kw)
                                    elif hasattr(result, method_name):
                                        method = getattr(result, method_name)
                                        result = method(*args, **kw)
                                # Apply aggregation
                                agg_method = getattr(result, agg_name)
                                return agg_method()
                            return agg_func
    
                        agg_dict[new_name] = pd.NamedAgg(column=expr.name, aggfunc=make_agg_func(pre_agg, agg_method_name))
    
                        # Store post-aggregation operations
                        if post_agg:
                            post_agg_operations[new_name] = post_agg
                    
                elif isinstance(expr, SymbolicAttr):
                    agg_dict[new_name] = pd.NamedAgg(column=expr.name, aggfunc=expr._agg_func)
                else:
                    # Literal value
                    agg_dict[new_name] = pd.NamedAgg(column=df_or_group.obj.columns[0], 
                                                      aggfunc=lambda x, val=expr: val)
            
            result = df_or_group.agg(**agg_dict)
            
            # Apply post-aggregation operations
            for col_name, operations in post_agg_operations.items():
                for method_name, args, kw in operations:
                    if hasattr(result[col_name], method_name):
                        method = getattr(result[col_name], method_name)
                        result[col_name] = method(*args, **kw)
            
            return result
        else:
            # Ungrouped: build a dictionary for aggregation
            result_dict = {}
            for new_name, expr in kwargs.items():
                if isinstance(expr, (SymbolicAttr, ChainedSymbolicAttr)):
                    result_dict[new_name] = [getattr(df_or_group[expr.name], expr._agg_func)()]
                else:
                    # Literal value
                    result_dict[new_name] = [expr]
        
            return pd.DataFrame(result_dict)

    return _summarize