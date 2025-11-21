import pandas as pd
import re

# Define the pasteurize() method
def pasteurize(df):
    """
    This module monkey-patches the pasteurize() method onto pd.DataFrame.
    The patch is applied automatically when this module is imported.
    
    Clean a Pandas DataFrame by:
        Removing empty and duplicate rows
        Standardizing column names (lowercase with underscores)
        Stripping whitespace from strings
        Converting "NA" and "NULL" char strings to true `null`s
        Converting strings to titlecase
        
    Usage: df.pasteurize()
    """
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Clean column names first
    def clean_name(name):
        name = str(name).lower()
        name = re.sub(r"[\s-]+", "_", name)
        name = re.sub(r"[^\w_]", "", name)
        return name.strip('_')
    
    # Rename columns
    df.columns = [clean_name(col) for col in df.columns]
    
    # Identify string/object columns
    string_cols = df.select_dtypes(include=['object', 'string']).columns
    
    # Clean string columns: strip whitespace, replace NA variants, apply title case
    for col in string_cols:
        try:
            # Only process if we can safely use string methods
            if df[col].notna().any():  # Check if column has any non-null values
                df[col] = (df[col]
                           .astype(str)
                           .str.strip()
                           .replace(['NA', 'NULL', 'nan', 'NaN', ''], pd.NA)
                           .str.title())
        except (AttributeError, TypeError):
            # If string operations fail, skip this column
            print(f"Warning: Could not process column '{col}' with string methods")
            continue
    
    # Remove empty and duplicate rows
    df = df.dropna(how='all').drop_duplicates()
    
    return df

# Monkey patch onto Pandas DataFrame
pd.DataFrame.pasteurize = pasteurize