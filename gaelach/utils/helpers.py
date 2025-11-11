from gaelach.core.symbolic import DeSelect
import pandas as pd
import re

# Selector classes
class StartsWithSelector:
    """Selects columns starting with a prefix."""
    def __init__(self, prefix):
        self.prefix = prefix
        # Check if the suffix contains regex special characters
        self.is_regex = bool(re.search(r'[|()[\]{}^$*+?\\.]', prefix))
    
    def __invert__(self):
        return DeSelect(self)

class EndsWithSelector:
    """Selects columns ending with a suffix or matching a regex pattern."""
    def __init__(self, suffix):
        self.suffix = suffix
        # Check if the suffix contains regex special characters
        self.is_regex = bool(re.search(r'[|()[\]{}^$*+?\\.]', suffix))
    
    def __invert__(self):
        """Support ~ operator for deselection."""
        return DeSelect(self)

class ContainsSelector:
    """Selects columns containing a substring."""
    def __init__(self, substring):
        self.substring = substring
        # Check if the suffix contains regex special characters
        self.is_regex = bool(re.search(r'[|()[\]{}^$*+?\\.]', substring))
    
    def __invert__(self):
        return DeSelect(self)

class WhereSelector:
    """Selects columns based on a predicate function applied to their data type."""
    def __init__(self, predicate):
        self.predicate = predicate

# Pattern selector functions
def starts_with(prefix):
    """Select columns that start with the given prefix."""
    return StartsWithSelector(prefix)

def ends_with(suffix):
    """Select columns that end with the given suffix."""
    return EndsWithSelector(suffix)

def contains(substring):
    """Select columns that contain the given substring."""
    return ContainsSelector(substring)

def where(predicate):
    """Select columns where a predicate function returns True for their data type."""
    return WhereSelector(predicate)

# Type predicate functions
def is_numeric(dtype):
    """Check if a Pandas data type is numeric."""
    return dtype in [
        "int", "int8", "int16", "int32", "int64",
        "float", "float16", "float32", "float64"
    ]

def is_integer(dtype):
    """Check if a Pandas data type is integer."""
    return dtype in [
        "int", "int8", "int16", "int32", "int64"
    ]

def is_float(dtype):
    """Check if a Pandas data type is float."""
    return dtype in ["float", "float16", "float32", "float64"]

def is_string(dtype):
    """Check if a Pandas data type is string."""
    return dtype == "str" or dtype == "obj"

def is_boolean(dtype):
    """Check if a Pandas data type is boolean."""
    return dtype == "bool"

def is_temporal(dtype):
    """Check if a Pandas data type is date/time related."""
    return dtype in ["datetime", "datetime64"]

def is_cat(dtype):
    """Check if a Pandas data type is categorical."""
    return dtype in ["category"]

def all():
    """Select all columns, mimics pl.all() in Polars"""
    return lambda cols: cols