# Establish symbolic attribution for Pandas dataframes
import pandas as pd 
from gaelach.core.pipe import MethodCall

class BinaryOperation:
    """Represents a binary operation between columns or values."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def _evaluate(self, df):
        """Evaluate the operation on a DataFrame."""
        # Resolve left side
        if isinstance(self.left, SymbolicAttr):
            left_val = df[self.left.name]
        elif isinstance(self.left, BinaryOperation):
            left_val = self.left._evaluate(df)
        else:
            left_val = self.left
        
        # Resolve right side
        if isinstance(self.right, SymbolicAttr):
            right_val = df[self.right.name]
        elif isinstance(self.right, BinaryOperation):
            right_val = self.right._evaluate(df)
        else:
            right_val = self.right
        
        # Perform operation
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val
        elif self.operator == '//':
            return left_val // right_val
        elif self.operator == '%':
            return left_val % right_val
        elif self.operator == '**':
            return left_val ** right_val

class StringAccessor:
    """String methods accessor for SymbolicAttr"""
    
    def __init__(self, symbolic_attr):
        self._symbolic_attr = symbolic_attr
    
    def contains(self, pat, case=True, na=None, regex=True):
        """Check if pattern is contained in string"""
        def _evaluate(df):
            col = df[self._symbolic_attr.name]
            return col.str.contains(pat, case=case, na=na, regex=regex)
        
        # Return a ChainedSymbolicAttr-like object that can be used in conditions
        result = ChainedSymbolicAttr(self._symbolic_attr, 'str.contains', (pat,), 
                                     {'case': case, 'na': na, 'regex': regex})
        result._evaluate = _evaluate
        return result
    
    def lower(self):
        """Convert strings to lowercase"""
        def _evaluate(df):
            col = df[self._symbolic_attr.name]
            return col.str.lower()
        
        result = ChainedSymbolicAttr(self._symbolic_attr, 'str.lower', (), {})
        result._evaluate = _evaluate
        return result
    
    def upper(self):
        """Convert strings to uppercase"""
        def _evaluate(df):
            col = df[self._symbolic_attr.name]
            return col.str.upper()
        
        result = ChainedSymbolicAttr(self._symbolic_attr, 'str.upper', (), {})
        result._evaluate = _evaluate
        return result

class SymbolicAttr:
    """
    Intermediate object returned by _.attribute_name
    
    Can become either a Pandas expression or a method call.
    """
    def __init__(self, name):
        self.name = name
        # Store column name 
        self._column_name = name
        
# Drop this - let pandas handle string methods 
#     @property
#     def str(self):
#         """Access string methods"""
#         return StringAccessor(self)
    
    def __call__(self, *args, **kwargs):
        """
        Called when used as _.method_name() in a pipe.
        
        Returns a MethodCall object for piping.
        """
        return MethodCall(self.name, args, kwargs)
    
    def __invert__(self):
        """
        Support deselection with ~ operator.
        
        Usage: df >> select(~_.column_name)
        """
        return DeSelect(self)
    
    def __or__(self, other):
        """
        Support range selection with | operator.
        
        Usage: df >> select(_.col1 | _.col2)
        """
        return ColumnRange(self, other)
    
    def __neg__(self):
        """
        Support negation for descending sort.
    
        Usage: df >> arrange(-_.column_name)
        """
        negated = SymbolicAttr(self.name)
        negated._is_negated = True
        negated._original = self.name
        return negated
    
    def __getattr__(self, attr):
        """
        Forward attribute access to create chained expressions.

        Instead of delegating to _expr, create a new SymbolicAttr
        that represents the chained operation.
        """
        # Special handling for accessor properties (str, dt, cat)
        if attr in ['str', 'dt', 'cat']:
            return ChainedSymbolicAttr(self, attr, (), {})
    
        # Special handling for custom methods
        if attr == 'not_in':
            def not_in_wrapper(values):
                result = ChainedSymbolicAttr(self, 'not_in', (values,), {})
                def _evaluate(df):
                    col_data = df[self.name]
                    return ~col_data.isin(values)
                result._evaluate = lambda df: _evaluate(df)
                return result
            return not_in_wrapper

        if attr == 'not_like':
            def not_like_wrapper(pattern):
                result = ChainedSymbolicAttr(self, 'not_like', (pattern,), {})
                def _evaluate(df):
                    col_data = df[self.name]
                    return ~col_data.str.contains(pattern)
                result._evaluate = lambda df: _evaluate(df)
                return result
            return not_like_wrapper

        # Create a new SymbolicAttr for the chained operation
        def chained_operation(*args, **kwargs):
            # This will be handled when the expression is evaluated
            return ChainedSymbolicAttr(self, attr, args, kwargs)
        return chained_operation
    
    def __add__(self, other):
        """Support + addition"""
        return BinaryOperation(self, '+', other)
    
    def __sub__(self, other):
        """Support - subtraction"""
        return BinaryOperation(self, '-', other)
    
    def __mul__(self, other):
        """Support * multiplication"""
        return BinaryOperation(self, '*', other)
    
    def __truediv__(self, other):
        """Support / division"""
        return BinaryOperation(self, '/', other)
    
    def __floordiv__(self, other):
        """Support // floor division"""
        return BinaryOperation(self, '//', other)
    
    def __mod__(self, other):
        """Support % modulo"""
        return BinaryOperation(self, '%', other)
    
    def __pow__(self, other):
        """Support ** exponentiation"""
        return BinaryOperation(self, '**', other)
    
    # For comparison operators, we need to create expressions
    def __eq__(self, other):
        return ColumnExpression(self.name, '==', other)
    
    def __ne__(self, other):
        return ColumnExpression(self.name, '!=', other)
    
    def __lt__(self, other):
        return ColumnExpression(self.name, '<', other)
    
    def __le__(self, other):
        return ColumnExpression(self.name, '<=', other)
    
    def __gt__(self, other):
        return ColumnExpression(self.name, '>', other)
    
    def __ge__(self, other):
        return ColumnExpression(self.name, '>=', other)

class ColumnExpression:
    """Represents a column comparison expression."""
    def __init__(self, column_name, operator, value):
        self.column_name = column_name
        self.operator = operator
        self.value = value
    
    def _evaluate(self, df):
        """Evaluate the expression on a DataFrame."""
        column = df[self.column_name]
        if self.operator == '==':
            return column == self.value
        elif self.operator == '!=':
            return column != self.value
        elif self.operator == '<':
            return column < self.value
        elif self.operator == '<=':
            return column <= self.value
        elif self.operator == '>':
            return column > self.value
        elif self.operator == '>=':
            return column >= self.value

class ChainedSymbolicAttr:
    """Represents a chained operation like _.column.fillna()"""
    def __init__(self, parent, method_name, args, kwargs):
        self.parent = parent
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        
        # Store the column name for aggregation functions
        if isinstance(parent, SymbolicAttr):
            self.name = parent.name
        elif isinstance(parent, ChainedSymbolicAttr):
            self.name = parent.name
        
        # Find the LAST aggregation function in the chain
        # Walk through the entire chain to find it
        self._agg_func = None
        if method_name in ['count', 'sum', 'mean', 'min', 'max', 'std', 'var', 'first', 'last', 'median']:
            self._agg_func = method_name
        elif isinstance(parent, ChainedSymbolicAttr) and hasattr(parent, '_agg_func') and parent._agg_func:
            # Inherit from parent if we don't have one
            self._agg_func = parent._agg_func
    
    def __getattr__(self, attr):
        """
        Allow further chaining of methods.
    
        This enables patterns like _.column.astype().mean()
        """
        # Special handling for accessor properties
        if attr in ['str', 'dt', 'cat']:
            return ChainedSymbolicAttr(self, attr, (), {})
    
        def chained_operation(*args, **kwargs):
            return ChainedSymbolicAttr(self, attr, args, kwargs)
        return chained_operation
    
    # Add invert method to select()
    def __invert__(self):
        """
        Support deselection with ~ operator.
    
        Usage: df >> select(~_.column_name)
        """
        return DeSelect(self)
    
    # Add or method to select()
    def __or__(self, other):
        """
        Support range selection with | operator.
    
        Usage: df >> select(_.col1 | _.col2)
        """
        return ColumnRange(self, other)
    
    # Patch in custom not_in() method
    def not_in(self, values):
        """
        Check if values are NOT in the given list.
    
        Inverse of is_in()
    
        Usage: df >> filter(_.col.not_in([1, 2, 3]))
        """
        result = ChainedSymbolicAttr(self.parent if hasattr(self, 'parent') else self, 'not_in', (values,), {})
        
        # Bind the evaluation method to the result object
        def _evaluate(df):
            # Get the parent column data
            if hasattr(result.parent, '_evaluate'):
                col_data = result.parent._evaluate(df)
            else:
                col_data = df[result.parent._name]
            return ~col_data.isin(values)
    
        result._evaluate = lambda df: _evaluate(df)
        return result

    # Patch in custom not_like() method
    def not_like(self, pattern):
        """
        Check if string does NOT contain the pattern.
    
        Inverse of str.contains()
    
        Usage: df >> filter(_.col.not_like("pattern"))
        """
        result = ChainedSymbolicAttr(self.parent if hasattr(self, 'parent') else self, 'not_like', (pattern,), {})
    
        # Bind the evaluation method to the result object
        def _evaluate(df):
            # Get the parent column data
            if hasattr(result.parent, '_evaluate'):
                col_data = result.parent._evaluate(df)
            else:
                col_data = df[result.parent._name]
            return ~col_data.str.contains(pattern)
    
        result._evaluate = lambda df: _evaluate(df)
        return result
    
    def __add__(self, other):
        """Support + addition"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__add__(other)

    def __sub__(self, other):
        """Support - subtraction"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__sub__(other)

    def __mul__(self, other):
        """Support * multipdication"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__mul__(other)

    def __truediv__(self, other):
        """Support / division"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__truediv__(other)

    def __floordiv__(self, other):
        """Support // floor division"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__floordiv__(other)

    def __mod__(self, other):
        """Support % modulo"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__mod__(other)

    def __pow__(self, other):
        """Support ** exponentiation"""
        if isinstance(other, SymbolicAttr):
            other = other._expr
        return self._expr.__pow__(other)
    
    def _evaluate(self, df):
        """Evaluate the chained operation on a DataFrame."""
        # First, get the parent column data
        if isinstance(self.parent, SymbolicAttr):
            col_data = df[self.parent.name]
        elif isinstance(self.parent, ChainedSymbolicAttr):
            col_data = self.parent._evaluate(df)
        else:
            col_data = self.parent

        # Check if this is an accessor (str, dt, cat)
        if self.method_name in ['str', 'dt', 'cat']:
            # Return the accessor itself, don't call it
            return getattr(col_data, self.method_name)
    
        # If col_data is already an accessor, get the method from it
        if hasattr(col_data, '__class__') and col_data.__class__.__name__ in ['StringMethods', 'DatetimeProperties', 'CategoricalAccessor']:
            method = getattr(col_data, self.method_name)
            return method(*self.args, **self.kwargs)
    
        # Normal method call
        method = getattr(col_data, self.method_name)
        return method(*self.args, **self.kwargs)
    
# Establish symbolic class for Pandas dataframes
class Symbolic:
    """
    Symbolic column reference object that creates Pandas expressions.
    
    Usage: 
    - _.column_name returns a SymbolicAttr (acts like pd.col("column_name"))
    - _.method() returns a MethodCall for piping to DataFrame methods
    """
    def __getattr__(self, name):
        """
        Intercept attribute access to create SymbolicAttr objects.
    
        name: The column or method name being referenced
    
        Returns a SymbolicAttr that can be used as an expression or called as a method
        """
        return SymbolicAttr(name)
    
# Helper classes for column selection patterns
class ColumnRange:
    """
    Represents a range of columns for selection.
    
    Created using the : operator between two SymbolicAttr objects.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __invert__(self):
        """Support ~ operator for deselection."""
        return DeSelect(self)

class DeSelect:
    """
    Represents columns to exclude from selection.
    
    Created using the ~ operator before a SymbolicAttr or helper function.
    """
    def __init__(self, col):
        self.col = col
    
# Create the global _ object for column references
_ = Symbolic()