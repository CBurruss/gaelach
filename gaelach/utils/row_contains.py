import pandas as pd

def row_contains(*values):
    """
    Check if any rows in a DataFrame contain any of the specified values.
    """
    values_list = [str(v) for v in values]
    
    def _row_contains(df):
        # Check if any value is a substring of any column
        return df.astype(str).apply(
            lambda row: any(any(val in cell for val in values_list) for cell in row),
            axis=1
        )
    
    return _row_contains