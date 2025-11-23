import pandas as pd

# String transformations
to_lower = lambda x: x.str.lower()
to_upper = lambda x: x.str.upper()
to_strip = lambda x: x.str.strip()
to_title = lambda x: x.str.title()

# Type coercion
to_str = lambda x: x.astype(str)
to_int = lambda x: pd.Series(pd.to_numeric(x, errors="coerce"), dtype="Int64")
to_float = lambda x: pd.Series(pd.to_numeric(x, errors="coerce"), dtype="Float64")
to_date = lambda x: pd.to_datetime(x, exact=False, errors="coerce")
to_cat = lambda x: pd.Series(x, dtype="category")

# Common cleaning operations
to_na = lambda x: x.replace(["", "None", "null", "NA", "N/A"], pd.NA)
to_zero = lambda x: x.fillna(0)

# Rounding helpers
to_round = lambda n: lambda x: x.round(n)  # curried: to_round(2)
