import pandas as pd
from io import StringIO
from typing import Literal


def glimpse(
    self,
    *,
    max_items_per_column: int = 10,
    max_colname_length: int = 30,
    max_value_length: int = 10,
    return_type: Literal["frame", "self", "string"] | None = None,
) -> str | pd.DataFrame | None:
    """
    Print a compact overview of the DataFrame with one row per column.
    
    Parameters
    ----------
    max_items_per_column : int, default 10
        Maximum number of values to show per column
    max_colname_length : int, default 30
        Maximum length of column names before truncation
    max_value_length : int, default 10
        Maximum length of individual values before truncation
    return_type : {'frame', 'self', 'string', None}, default None
        - None: prints output and returns None
        - 'string': returns output as string
        - 'frame': returns glimpse data as DataFrame
        - 'self': prints output and returns original DataFrame
    
    Returns
    -------
    str, DataFrame, or None
        Depends on return_type parameter
    """
    # Validate return_type
    return_frame = False
    if return_type is not None:
        return_frame = return_type == "frame"
        if not return_frame and return_type not in ("self", "string"):
            raise ValueError(
                f"invalid `return_type`; found {return_type!r}, "
                "expected one of 'string', 'frame', 'self', or None"
            )
    
    # Limit number of values to display
    max_n_values = min(max_items_per_column, len(self))
    
    def _column_to_row_output(col_name: str, dtype) -> tuple[str, str, list]:
        """Convert column info to row format for glimpse output."""
        # Use repr for object/string types, str for others
        fn = repr if dtype == object else str
        
        # Get first n values
        values = self[col_name].iloc[:max_n_values].tolist()
        
        # Truncate column name if needed
        if len(col_name) > max_colname_length:
            col_name = col_name[: (max_colname_length - 1)] + "…"
        
        # Format dtype string with abbreviations
        dtype_str = str(dtype)
        
        # Abbreviate common type names
        type_abbrev = {
            "string": "str",
            "categorical": "cat",
            "boolean": "bool",
            "object": "obj",
            "decimal": "dec",
            "int32": "i32",
            "int64": "i64",
            "float32": "f32",
            "float64": "f64",
            "datetime64[ns]": "datetime"
        }
        
        dtype_str = type_abbrev.get(dtype_str.lower(), dtype_str)
        
        if not return_frame:
            dtype_str = f"<{dtype_str}>"
        
        # Apply formatting function to values
        formatted_values = [
            (fn(v) if pd.notna(v) else None) for v in values
        ]
        
        return (col_name, dtype_str, formatted_values)
    
    # Process all columns
    data = [
        _column_to_row_output(col, self[col].dtype)
        for col in self.columns
    ]
    
    # Return as DataFrame if requested
    if return_frame:
        return pd.DataFrame(
            data,
            columns=["column", "dtype", "values"]
        )
    
    # Determine layout widths for alignment
    max_col_name = max((len(col_name) for col_name, _, _ in data))
    max_col_dtype = max((len(dtype_str) for _, dtype_str, _ in data))
    
    # Build output string
    output = StringIO()
    output.write(f"Rows: {len(self)}\nColumns: {len(self.columns)}\n")
    
    for col_name, dtype_str, values in data:
        # Format values, replacing None with "null" and truncating long values
        formatted_vals = []
        for v in values:
            if v is None:
                # ANSI codes: \033[3;31m = red italic, \033[0m = reset
                formatted_vals.append("\033[3;31mnull\033[0m")
            else:
                # Truncate if value exceeds max_value_length
                if len(v) > max_value_length:
                    v = v[: (max_value_length - 1)] + "…"
                formatted_vals.append(v)
        
        val_str = ", ".join(formatted_vals)
        output.write(
            f"$ {col_name:<{max_col_name}} {dtype_str:>{max_col_dtype}} {val_str}\n"
        )
    
    s = output.getvalue()
    
    # Return based on return_type
    if return_type == "string":
        return s
    
    print(s, end="")
    
    if return_type == "self":
        return self
    
    return None


# Add method to pandas DataFrame
pd.DataFrame.glimpse = glimpse