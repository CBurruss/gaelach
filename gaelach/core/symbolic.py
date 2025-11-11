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

class SymbolicAttr:
    """
    Intermediate object returned by _.attribute_name
    
    Can become either a Pandas expression or a method call.
    """
    def __init__(self, name):
        self.name = name
        # Don't create a circular reference - store column name instead
        self._column_name = name
    
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
    
    def __getattr__(self, attr):
        """
        Forward attribute access to create chained expressions.
        
        Instead of delegating to _expr, create a new SymbolicAttr
        that represents the chained operation.
        """
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
        return ~self._expr.is_in(values)
    
    # Patch in custom not_like() method
    def not_like(self, pattern):
        """
        Check if string does NOT contain the pattern.
        
        Inverse of str.contains()
        
        Usage: df >> filter(_.col.not_like("pattern"))
        """
        return ~self._expr.str.contains(pattern)
    
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