# gaelach <img src="./hex/gaelach-hex.png" align="right" width="120" alt="Hexagonal logo for the penguins package" /> 

a siuba alternative providing extended methods and functions to pandas for tidy data manipulation

## About gaelach 

This project originally started as a port of my [acutis](https://github.com/CBurruss/acutis) R package for pandas—providing some extended methods for data analysis—but it's turned into a full port of my [penguins](https://github.com/CBurruss/penguins) package, which itself is a port of [siuba](https://github.com/machow/siuba/blob/main/README.md) for polars. In turn, gaelach has become a fairly capable alternative to siuba as a tidy-style wrapper for pandas methods and functions, albeit with slight differences in function behavior and arguments. 

## Installation

You can install the dev version of gaelach with:

```bash
pip install git+https://github.com/CBurruss/gaelach.git
```

## What's Inside

In parallel to penguins, we can group gaelach's utilities into four main categories — 1) core functionality, 2) acutis methods, 3) verb functions, and 4) helper functions. 

### 1. Core functionality

At its core, gaelach provides a dplyr-flavored interface for pandas through two main features:

 - The pipe operator `>>` — enables function function chaining akin to R's `|>` pipe
 - The symbolic placeholder `_` — acts as a helper by standing in for two main use cases:
      1. DataFrame references in method calls — e.g. `df >> _.head(5)`
      2. Column references in verb expressions — e.g. `df >> select(_.col)`

### 2. Acutis methods

As penguins does with polars, gaelach extends polars objects with both implicit and explicit methods. Each of these were originally ported from acutis and provide handy functionality for typical data processsing and handling. 

**Explicit import required:**
 - `affiche()` — display a pandas DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
     - As a bonus, this is also provided as a function! 
 - `count_na()` — create a summary table counting `NA` values for each column in a DataFrame
 - `count_table()` — create a frequency table with counts and percentages
 - `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names

### 3. Verb functions

As hinted at above, gaelach gains most of its utility from its dplyr-styled functions. While they're covered in the [Examples](#examples) section, here are the verb functions that have currently been ported over:
1. `select()` — select specific columns from the DataFrame
2. `filter()` — filter rows based on boolean conditions
3. `mutate()` — create new columns or modify existing ones

### 4. Helper functions

Included are various helper functions to assist in column selection within `select()` and `mutate()`:
1. `across()` — allows the application of a function across columns
     - Supports pattern matching on column names with `starts_with()`, `ends_with()` and `contains()` 
2. `where()` — for subsetting columns based on one or more conditions
     - Supports `is_boolean`, `is_cat`, `is_float`, `is_integer`, `is_numeric`, `is_string` and `is_temporal` as boolean checks for column data types

## Examples
 
For starters, we'll load in lunar craters data from the Lunar and Plantery Institute (see [Notes](#notes)):

```python
import pandas as pd
import gaelach as gl
from importlib.resources import files

data_path = files('gaelach.data').joinpath('lunar-craters.parquet')
df = pd.read_parquet(data_path)
```

## Dependencies

For a detailed list of gaelach's dependencies, consult the dependencies list in `pyproject.toml`.

## Notes

Lunar crater data provided by the [Lunar and Planetary Institute](https://www.lpi.usra.edu/scientific-databases/).