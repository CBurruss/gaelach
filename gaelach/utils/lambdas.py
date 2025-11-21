import pandas as pd

# String transformations
to_lower = lambda x: x.str.lower()
to_upper = lambda x: x.str.upper()
to_strip = lambda x: x.str.strip()
to_title = lambda x: x.str.title()

# Type coercion
to_str = lambda x: x.astype(str)
to_int = lambda x: pd.to_numeric(x, errors="coerce").astype("Int64")  # nullable integer
to_bool = lambda x: x.astype(bool)
to_date = lambda x: pd.to_datetime(x, exact=False, errors="coerce")

# Common cleaning operations
to_na = lambda x: x.replace(["", "None", "null", "NA", "N/A"], pd.NA)
to_zero = lambda x: x.fillna(0)

# Rounding helpers
to_round = lambda n: lambda x: x.round(n)  # curried: to_round(2)