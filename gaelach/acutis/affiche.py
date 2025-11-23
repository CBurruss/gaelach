# Define the affiche() method and function 
import pandas as pd
import re
import math

"""
affiche extension for Pandas DataFrames and Series.

This module monkey-patches the affiche() method onto pd.DataFrame and pd.Series.
The patch is applied automatically when this module is imported.

Usage:
    df.affiche()
    df["col"].affiche()
"""
# Define the affiche() method
def affiche(self, align="left", na_color="\033[91;3m", theme="newspaper"):
    """
    Display a Pandas DataFrame or Series with formatted table borders and styling.
    
    Args:
        self: the DataFrame instance
        align: text alignment ("left", "center", "right")
        na_color: ANSI color code for missing values
        theme: border theme ("newspaper")
    
    Usage:
        df.affiche()
        df["col"].affiche()
    """
       
    df = self

    # Convert Series to DataFrame
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
    
    # Handle empty DataFrame
    if df.shape[1] == 0 or df.shape[0] == 0:
        msg = "That table doesn't exist!"
        width = len(msg)
        top = f"╔{'═' * (width + 2)}╗"
        mid = f"║ {msg} ║"
        bot = f"╚{'═' * (width + 2)}╝"
        print(f"{top}\n{mid}\n{bot}")
        return None

    # Border theme
    if theme == "newspaper":
        border = {
            "h": "═", "v": "║",
            "tl": "╔", "tr": "╗",
            "bl": "╚", "br": "╝",
            "jn": "╬",
            "l": "╠", "r": "╣",
            "t": "╦", "b": "╩"
        }
    else:
        raise ValueError("Theme not supported. Try 'newspaper'")

    reset = "\033[0m"

    # Handle color for unique NA types
    def color_na(x):
        if pd.isna(x):
            # Timestamp missing
            if isinstance(x, pd.Timestamp):
                return f"{na_color}NaT{reset}"
            # Everything else (int, bool, str, object, categorical) → NA
            return f"{na_color}NA{reset}"
        return str(x)

    # Width calculator (ignores ANSI codes)
    def display_width(s):
        clean = re.sub(r'\033\[[0-9;]*[mK]', '', str(s))
        return len(clean)

    # Extract index info
    index_values = [str(idx) for idx in df.index]
    index_name = "index"
    index_dtype = str(df.index.dtype)

    # Pull column types
    col_types = [str(dtype) for dtype in df.dtypes]
    
    # Abbreviate common type names
    type_abbrev = {
        "string": "str",
        "categorical": "cat",
        "category": "cat",
        "boolean": "bool",
        "object": "obj",
        "decimal": "dec",
        "int32": "i32",
        "int64": "i64",
        "float32": "f32",
        "float64": "f64",
        "datetime64[ns]": "datetime",
        "timedelta64[ns]": "timedelta"
    }

    col_types = [type_abbrev.get(dtype.lower(), dtype) for dtype in col_types]
    
    # Abbreviate index dtype
    index_dtype_abbrev = type_abbrev.get(str(df.index.dtype).lower(), str(df.index.dtype))
    
    # Prepend index to column names and types
    col_names = [index_name] + list(df.columns)
    col_types = [index_dtype_abbrev] + col_types
    
    # Column widths (starting with index)
    col_widths = []
    
    # Index column width
    header_width = display_width(index_name)
    type_width = display_width(index_dtype_abbrev)
    index_widths = [display_width(val) for val in index_values]
    col_widths.append(max([header_width, type_width] + index_widths))
    
    # Regular column widths
    for i, col in enumerate(df.columns):
        header_width = display_width(col)
        type_width = display_width(col_types[i + 1])
        # Get column values and apply color_na
        col_values = [color_na(val) for val in df[col].tolist()] 
        data_widths = [display_width(val) for val in col_values]
        col_widths.append(max([header_width, type_width] + data_widths))

    # Draw horizontal line
    def draw_hline(connector_left, connector_right, cross):
        line = connector_left
        for i, width in enumerate(col_widths):
            line += border["h"] * (width + 2) + cross
        line = line[:-1] + connector_right
        return line

    top_line = draw_hline(border["tl"], border["tr"], border["t"])
    mid_line = draw_hline(border["l"], border["r"], border["jn"])
    bot_line = draw_hline(border["bl"], border["br"], border["b"])

    # Header
    header_parts = [border["v"]]
    for i, name in enumerate(col_names):
        width = col_widths[i]
        pad_total = width - display_width(name)
    
        if align == "left":
            pad_left = 0
        elif align == "center":
            pad_left = math.floor(pad_total / 2)
        elif align == "right":
            pad_left = pad_total
        else:
            pad_left = 0

        pad_right = pad_total - pad_left
        header_parts.append(f" {' ' * pad_left}{name}{' ' * pad_right} {border['v']}")
    header = "".join(header_parts)

    # Type row
    type_parts = [border["v"]]
    for i, dtype in enumerate(col_types):
        dtype_formatted = f"\033[3m{dtype.lower()}{reset}"
        width = col_widths[i]
        pad_total = width - display_width(dtype)

        if align == "left":
            pad_left = 0
        elif align == "center":
            pad_left = math.floor(pad_total / 2)
        elif align == "right":
            pad_left = pad_total
        else:
            pad_left = 0

        pad_right = pad_total - pad_left
        type_parts.append(f" {' ' * pad_left}{dtype_formatted}{' ' * pad_right} {border['v']}")
    type_row = "".join(type_parts)

    # Data rows
    data_rows = []
    for row_idx in range(len(df)):
        row_parts = [border["v"]]
        
        # Index cell
        index_content = index_values[row_idx]
        width = col_widths[0]
        pad_total = width - display_width(index_content)

        if align == "left":
            pad_left = 0
        elif align == "center":
            pad_left = math.floor(pad_total / 2)
        elif align == "right":
            pad_left = pad_total
        else:
            pad_left = 0

        pad_right = pad_total - pad_left
        row_parts.append(f" {' ' * pad_left}{index_content}{' ' * pad_right} {border['v']}")
        
        # Data cells
        for col_idx, col_name in enumerate(df.columns):
            content = color_na(df.iloc[row_idx][col_name])
            width = col_widths[col_idx + 1]
            pad_total = width - display_width(content)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            row_parts.append(f" {' ' * pad_left}{content}{' ' * pad_right} {border['v']}")
        data_rows.append("".join(row_parts))

    # Print table
    print(top_line)
    print(header)
    print(type_row)
    print(mid_line)
    print("\n".join(data_rows))
    print(bot_line)

    return None

# Monkey-patch Pandas DataFrame and LazyFrame
pd.DataFrame.affiche = affiche
pd.Series.affiche = affiche

# Define the affiche() function
# Define the affiche() function
def affiche(align="left", na_color="\033[91;3m", theme="newspaper"):
    """
    Display a Pandas DataFrame or LazyFrame with formatted table borders and styling.
    
    Args:
        align: text alignment ("left", "center", "right")
        na_color: ANSI color code for missing values
        theme: border theme ("newspaper")
    
    Usage:
        df >> affiche()
    """
    def _affiche(df):
   
        # Handle empty DataFrame
        if df.shape[1] == 0 or df.shape[0] == 0:
            msg = "That table doesn't exist!"
            width = len(msg)
            top = f"╔{'═' * (width + 2)}╗"
            mid = f"║ {msg} ║"
            bot = f"╚{'═' * (width + 2)}╝"
            print(f"{top}\n{mid}\n{bot}")
            return None

        # Border theme
        if theme == "newspaper":
            border = {
                "h": "═", "v": "║",
                "tl": "╔", "tr": "╗",
                "bl": "╚", "br": "╝",
                "jn": "╬",
                "l": "╠", "r": "╣",
                "t": "╦", "b": "╩"
            }
        else:
            raise ValueError("Theme not supported. Try 'newspaper'")

        reset = "\033[0m"

        # Handle color for unique NA types
        def color_na(x):
            if pd.isna(x):
                # Timestamp missing
                if isinstance(x, pd.Timestamp):
                    return f"{na_color}NaT{reset}"
                # Everything else (int, bool, str, object, categorical) → NA
                return f"{na_color}NA{reset}"
            return str(x)

        # Width calculator (ignores ANSI codes)
        def display_width(s):
            clean = re.sub(r'\033\[[0-9;]*[mK]', '', str(s))
            return len(clean)

        # Extract index info
        index_values = [str(idx) for idx in df.index]
        index_name = "index"
        index_dtype = str(df.index.dtype)

        # Pull column data types
        col_types = [str(dtype) for dtype in df.dtypes]
        
        # Abbreviate common type names
        type_abbrev = {
            "string": "str",
            "categorical": "cat",
            "category": "cat",
            "boolean": "bool",
            "object": "obj",
            "decimal": "dec",
            "int32": "i32",
            "int64": "i64",
            "float32": "f32",
            "float64": "f64",
            "datetime64[ns]": "datetime",
            "timedelta64[ns]": "timedelta"
        }

        col_types = [type_abbrev.get(str(dtype), str(dtype)) for dtype in df.dtypes]
        
        # Abbreviate index dtype
        index_dtype_abbrev = type_abbrev.get(str(df.index.dtype), str(df.index.dtype))
        
        # Prepend index to column names and types
        col_names = [index_name] + list(df.columns)
        col_types = [index_dtype_abbrev] + col_types
    
        # Column widths (starting with index)
        col_widths = []
        
        # Index column width
        header_width = display_width(index_name)
        type_width = display_width(index_dtype_abbrev)
        index_widths = [display_width(val) for val in index_values]
        col_widths.append(max([header_width, type_width] + index_widths))
        
        # Regular column widths
        for i, col in enumerate(df.columns):
            header_width = display_width(col)
            type_width = display_width(col_types[i + 1])
            # Get column values and apply color_na
            col_values = [color_na(val) for val in df[col].tolist()]
            data_widths = [display_width(val) for val in col_values]
            col_widths.append(max([header_width, type_width] + data_widths))

        # Draw horizontal line
        def draw_hline(connector_left, connector_right, cross):
            line = connector_left
            for i, width in enumerate(col_widths):
                line += border["h"] * (width + 2) + cross
            line = line[:-1] + connector_right
            return line

        top_line = draw_hline(border["tl"], border["tr"], border["t"])
        mid_line = draw_hline(border["l"], border["r"], border["jn"])
        bot_line = draw_hline(border["bl"], border["br"], border["b"])

        # Header
        header_parts = [border["v"]]
        for i, name in enumerate(col_names):
            width = col_widths[i]
            pad_total = width - display_width(name)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            header_parts.append(f" {' ' * pad_left}{name}{' ' * pad_right} {border['v']}")
        
        header = "".join(header_parts)

        # Type row
        type_parts = [border["v"]]
        for i, dtype in enumerate(col_types):
            dtype_formatted = f"\033[3m{dtype.lower()}{reset}"
            width = col_widths[i]
            pad_total = width - display_width(dtype)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            type_parts.append(f" {' ' * pad_left}{dtype_formatted}{' ' * pad_right} {border['v']}")
        type_row = "".join(type_parts)

        # Data rows
        data_rows = []
        for row_idx in range(len(df)):
            row_parts = [border["v"]]
            
            # Index cell
            index_content = index_values[row_idx]
            width = col_widths[0]
            pad_total = width - display_width(index_content)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            row_parts.append(f" {' ' * pad_left}{index_content}{' ' * pad_right} {border['v']}")
            
            # Data cells
            for col_idx, col_name in enumerate(df.columns):
                content = color_na(df.iloc[row_idx][col_name])
                width = col_widths[col_idx + 1]
                pad_total = width - display_width(content)

                if align == "left":
                    pad_left = 0
                elif align == "center":
                    pad_left = math.floor(pad_total / 2)
                elif align == "right":
                    pad_left = pad_total
                else:
                    pad_left = 0

                pad_right = pad_total - pad_left
                row_parts.append(f" {' ' * pad_left}{content}{' ' * pad_right} {border['v']}")
            
            data_rows.append("".join(row_parts))

        # Print table
        print(top_line)
        print(header)
        print(type_row)
        print(mid_line)
        print("\n".join(data_rows))
        print(bot_line)
    
    return _affiche

# Export both for different use cases
__all__ = ['affiche']  # The function version for piping