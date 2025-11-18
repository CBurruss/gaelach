# Changelog

All notable changes to `gaelach` will be documented in this changelog

## *0.1.0* — 2025-11-18

Initial package release

### Features
- Included methods:
  1. `affiche()` — display a pandas DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
  2. `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names
  3. `count_table()` — create a frequency table with counts and percentages
  4. `count_na()` — create a summary table counting `NA` values for each column in a DataFrame
  5. `glimpse()` — print a compact overview of a DataFrame with one row per column
  6. `not_in()` — perform the inverse of the `isin()` method
  7. `not_like()` — perform the inverse of the `str.contains()` method
- Verb functions:
  1. `select()` — select specific columns from the DataFrame
  2. `filter()` — filter rows based on boolean conditions
  3. `mutate()` — create new columns or modify existing ones
  4. `group_by()` — group DataFrame by one or more columns
  5. `summarize()` — aggregate data, typically after `group_by()`
  6. `reframe()` — create new rows based on group summaries, also typically used after `group_by()`
  7. `pull()` — extract a single column as a series or scalar value
  8. `join()` — join two tables on a matching column
      - How: "inner", "left", "right", "outer", "cross", "semi", "anti"
  9. `pivot_wider()` — pivot a DataFrame from long to wide format
  10. `pivot_longer()` — pivot a DataFrame from wide to long format
  11. `unite()` — combine multiple columns into one column
  12. `separate()` — split a column into multiple columns
  13. `bind_cols()` — bind the columns of two DataFrames together
  15. `bind_rows()` — bind the rows of two DataFrames together
  16. `head()` — return first n rows
  17. `tail()` — return last n rows 
  18. `slice()` — select rows by position
  19. `sample()` — return a sample of rows from a DataFrame
  20. `distinct()` — keep only unique rows based on specified columns
  21. `arrange()` — sort rows by column expressions
  22. `relocate()` — reorder columns in a DataFrame
  23. `rename()` — rename columns
  24. `round()` — round numeric columns to specified decimal places
  25. `drop_null()` — remove rows with `null` values
- Helper functions
  1. `across()` — allows the application of a function across columns
     - Supports pattern matching on column names with `starts_with()`, `ends_with()` and `contains()` 
  2. `where()` — for subsetting columns based on one or more conditions
     - Supports `is_boolean`, `is_cat`, `is_float`, `is_integer`, `is_numeric`, `is_string` and `is_temporal` as boolean checks for column data types
