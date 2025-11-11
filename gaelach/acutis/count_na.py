import pandas as pd
import numpy as np

# Define a custom method count_na() for counting NA values for each column
def count_na(self):
    """
    count_na extension for Pandas DataFrame.

    This module monkey-patches the count_na() method onto pd.DataFrame.
    The patch is applied automatically when this module is imported.

    Usage: df.count_na()
    """
    # Count NAs for each column
    na_counts = self.isna().sum().reset_index()
    na_counts.columns = ["col", "na_count"]

    # Calculate percentages
    na_counts["na_percent"] = (
        (na_counts["na_count"] / len(self) * 100)
        .round(0)
        .astype(int)
        .astype(str) + "%"
    )

    # Handle 0% and <1% cases
    na_counts["na_percent"] = np.where(
        na_counts["na_count"] == 0,
        "0%",
        np.where(
            (na_counts["na_count"] / len(self)) <= 0.0099,
            "<1%",
            na_counts["na_percent"]
        )
    )

    # Sort by missing count
    na_counts = na_counts.sort_values("na_count", ascending=False).reset_index(drop=True)
    return na_counts

# Monkey patch the method onto DataFrame
pd.DataFrame.count_na = count_na