# Establish the pipe operator >> for Pandas
import pandas as pd

class MethodCall:
    """
    Represents a method call to be executed on a DataFrame.
    
    Used when piping to DataFrame methods via _.method_name()
    """
    def __init__(self, method_name, args, kwargs):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, df):
        """
        Execute the method call on the DataFrame.
        
        df: The Pandas DataFrame to call the method on
        
        Returns the result of the method call
        """
        method = getattr(df, self.method_name)
        return method(*self.args, **self.kwargs)

class _:
    """
    Placeholder for DataFrame method calls in pipes.
    
    Usage: df >> _.method_name(args)
    """
    def __getattr__(self, name):
        def method_caller(*args, **kwargs):
            return MethodCall(name, args, kwargs)
        return method_caller

_ = _()

def _pipe_rshift(self, other):
    """
    Pipe operator for Pandas DataFrames.
    
    self: The Pandas DataFrame
    other: Either a verb function or a MethodCall object
    
    Returns the result of applying the verb function or method call.
    """
    # Check if other is a MethodCall (from _.method_name())
    if isinstance(other, MethodCall):
        return other(self)
    # Otherwise it's a verb function
    return other(self)

# Monkey-patch Pandas DataFrame
pd.DataFrame.__rshift__ = _pipe_rshift

# Make Pandas GroupBy pipeable
pd.core.groupby.generic.DataFrameGroupBy.__rshift__ = _pipe_rshift