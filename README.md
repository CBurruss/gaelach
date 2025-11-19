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

As penguins does with polars, gaelach extends pandas objects with implicitly imported methods. Each of these were originally ported from acutis and provide handy functionality for typical data processsing and handling. And I've also borrowed `glimpse()` from polars.
1. `affiche()` — display a pandas DataFrame with aethetic table borders and styling (from the French *affiche* to display something)
     - As a bonus, this is also provided as a function (import required) 
2. `pasteurize()` — clean a DataFrame by removing empty rows, duplicates, and standardizing column names
3. `count_table()` — create a frequency table with counts and percentages
4. `count_na()` — create a summary table counting `NA` values for each column in a DataFrame
5. `glimpse()` — print a compact overview of a DataFrame with one row per column
6. `not_in()` — perform the inverse of the `isin()` method
7. `not_like()` — perform the inverse of the `str.contains()` method

### 3. Verb functions

As hinted at above, gaelach gains most of its utility from its dplyr-styled functions. While they're covered in the [Examples](#examples) section, here are the verb functions that have currently been ported over:
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

### 4. Helper functions

Included are various helper functions to assist in column selection within `select()` and `mutate()`:
1. `across()` — allows the application of a function across columns
     - Supports pattern matching on column names with `starts_with()`, `ends_with()` and `contains()` 
2. `where()` — for subsetting columns based on one or more conditions
     - Supports `is_boolean`, `is_cat`, `is_float`, `is_integer`, `is_numeric`, `is_string` and `is_temporal` as boolean checks for column data types

## Examples
 
We'll start by loading in data on the Solar System's moons (see [Notes](#notes)):

```python
import pandas as pd
import gaelach as gl
from importlib.resources import files

data_path = files('gaelach.data').joinpath('moons.parquet')
moons = pd.read_parquet(data_path)
```

### Methods

#### 1. `affiche()`

<details>
<summary>View examples</summary>

We can use `affiche()` on DataFrames as both a method and as a function:

```python
# Within a method chain
moons[["name", "parent"]].head().affiche()
    
# Or as a function in a pipe chain
moons >> select(_.name, _.parent) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════╗
║ index ║ name   ║ parent  ║
║ i64   ║ obj    ║ obj     ║
╠═══════╬════════╬═════════╣
║ 0     ║ Moon   ║ Earth   ║
║ 1     ║ Phobos ║ Mars    ║
║ 2     ║ Deimos ║ Mars    ║
║ 3     ║ Io     ║ Jupiter ║
║ 4     ║ Europa ║ Jupiter ║
╚═══════╩════════╩═════════╝
```

It also works on pandas Series objects:

```python
# Method
moons["name"].head().affiche()

# Function    
moons >> select(_.name) \
    >> head() \
    >> affiche()
```

```
╔═══════╦════════╗
║ index ║ name   ║
║ i64   ║ obj    ║
╠═══════╬════════╣
║ 0     ║ Moon   ║
║ 1     ║ Phobos ║
║ 2     ║ Deimos ║
║ 3     ║ Io     ║
║ 4     ║ Europa ║
╚═══════╩════════╝
```

</details> 

#### 2. `pasteurize()`

<details>
<summary>View examples</summary>

Since `pasteurize()` fixes column names, we'll use this cleaned version of `moons` moving forward:

```python
moons = moons.pasteurize()

moons.head(5).affiche()
```

```
╔════════╦═══════╦═════════╦═════════╦═══════════════════════════╦════════════════╦════════════════════════════╦═════════════════════════════════╦════════════════╦════════════════╦═══════════════╦═════════════════════╦═══════════════════════════════╦══════════════════╗
║ name   ║ image ║ parent  ║ numeral ║ average_orbital_speed_kms ║ mean_radius_km ║ orbital_semi_major_axis_km ║ sidereal_period_d_r__retrograde ║ discovery_year ║ year_announced ║ discovered_by ║ apparent_magnitudea ║ notes                         ║ refs             ║
║ obj    ║ obj   ║ obj     ║ obj     ║ obj                       ║ obj            ║ f64                        ║ obj                             ║ obj            ║ obj            ║ obj           ║ obj                 ║ obj                           ║ obj              ║
╠════════╬═══════╬═════════╬═════════╬═══════════════════════════╬════════════════╬════════════════════════════╬═════════════════════════════════╬════════════════╬════════════════╬═══════════════╬═════════════════════╬═══════════════════════════════╬══════════════════╣
║ Moon   ║ NA    ║ Earth   ║ I (1)   ║ 1.022                     ║ 1738           ║ 384399.0                   ║ 27.321582                       ║ Prehistoric    ║ Prehistory     ║ Â€”           ║ -12.9 To -2.5       ║ Synchronous Rotation (Binary) ║ [12]             ║
║ Phobos ║ NA    ║ Mars    ║ I (1)   ║ 2.138                     ║ 11.267         ║ 9380.0                     ║ 0.319                           ║ 1877           ║ 1877           ║ Hall          ║ 11.8                ║ Synchronous Rotation          ║ [13][14][15][16] ║
║ Deimos ║ NA    ║ Mars    ║ Ii (2)  ║ 1.351                     ║ 6.2Â±0.18      ║ 23460.0                    ║ 1.262                           ║ 1877           ║ 1877           ║ Hall          ║ 12.89               ║ Synchronous Rotation          ║ [13][14][15][17] ║
║ Io     ║ NA    ║ Jupiter ║ I (1)   ║ 17.334                    ║ 1,821.6Â±0.5   ║ 421800.0                   ║ 1.769                           ║ 1610           ║ 1610           ║ Galileo       ║ 5.02                ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
║ Europa ║ NA    ║ Jupiter ║ Ii (2)  ║ 13.7                      ║ 1,560.8Â±0.5   ║ 671100.0                   ║ 3.551                           ║ 1610           ║ 1610           ║ Galileo       ║ 5.29                ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
╚════════╩═══════╩═════════╩═════════╩═══════════════════════════╩════════════════╩════════════════════════════╩═════════════════════════════════╩════════════════╩════════════════╩═══════════════╩═════════════════════╩═══════════════════════════════╩══════════════════╝
```

</details> 

#### 3. `count_table()`

<details>
<summary>View examples</summary>

```python
moons["parent"].count_table().affiche()
```

```
╔══════════╦═══════╦═════════╗
║ parent   ║ count ║ percent ║
║ obj      ║ i64   ║ obj     ║
╠══════════╬═══════╬═════════╣
║ Saturn   ║ 274   ║ 64%     ║
║ Jupiter  ║ 97    ║ 23%     ║
║ Uranus   ║ 29    ║ 7%      ║
║ Neptune  ║ 16    ║ 4%      ║
║ Pluto    ║ 5     ║ 1%      ║
║ Haumea   ║ 2     ║ <1%     ║
║ Mars     ║ 2     ║ <1%     ║
║ Earth    ║ 1     ║ <1%     ║
║ Orcus    ║ 1     ║ <1%     ║
║ Quaoar   ║ 1     ║ <1%     ║
║ Makemake ║ 1     ║ <1%     ║
║ Gonggong ║ 1     ║ <1%     ║
║ Eris     ║ 1     ║ <1%     ║
╚══════════╩═══════╩═════════╝
```

</details> 

#### 4. `count_na()`

<details>
<summary>View examples</summary>

```python
moons.count_na().affiche()
```

```
╔═════════════════════════════════╦══════════╦════════════╗
║ col                             ║ na_count ║ na_percent ║
║ obj                             ║ i64      ║ obj        ║
╠═════════════════════════════════╬══════════╬════════════╣
║ image                           ║ 431      ║ 100%       ║
║ average_orbital_speed_kms       ║ 408      ║ 95%        ║
║ apparent_magnitudea             ║ 257      ║ 60%        ║
║ orbital_semi_major_axis_km      ║ 6        ║ 1%         ║
║ orbital_semi_major_axis_km      ║ 6        ║ 1%         ║
║ refs                            ║ 1        ║ <1%        ║
║ notes                           ║ 1        ║ <1%        ║
║ mean_radius_km                  ║ 0        ║ 0%         ║
║ numeral                         ║ 0        ║ 0%         ║
║ mean_radius_km                  ║ 0        ║ 0%         ║
║ numeral                         ║ 0        ║ 0%         ║
║ parent                          ║ 0        ║ 0%         ║
║ name                            ║ 0        ║ 0%         ║
║ year_announced                  ║ 0        ║ 0%         ║
║ discovery_year                  ║ 0        ║ 0%         ║
║ sidereal_period_d_r__retrograde ║ 0        ║ 0%         ║
║ discovered_by                   ║ 0        ║ 0%         ║
╚═════════════════════════════════╩══════════╩════════════╝
```
</details> 

#### 5. `glimpse()`

<details>
<summary>View examples</summary>

```python
moons.glimpse()
```
```
Rows: 431
Columns: 14
$ name                           <obj> 'Moon', 'Phobos', 'Deimos', 'Io', 'Europa', 'Ganymede', 'Callisto', 'Amalthea', 'Himalia', 'Elara'
$ image                          <obj> null, null, null, null, null, null, null, null, null, null
$ parent                         <obj> 'Earth', 'Mars', 'Mars', 'Jupiter', 'Jupiter', 'Jupiter', 'Jupiter', 'Jupiter', 'Jupiter', 'Jupiter'
$ numeral                        <obj> 'I (1)', 'I (1)', 'Ii (2)', 'I (1)', 'Ii (2)', 'Iii (3)', 'Iv (4)', 'V (5)', 'Vi (6)', 'Vii (7)'
$ average_orbital_speed_kms      <obj> '1.022', '2.138', '1.351', '17.334', '13.7', '10.9', '8.2', '26.47', '3.34', '3.29'
$ mean_radius_km                 <obj> '1738', '11.267', '6.2Â±0.1…, '1,821.6Â…, '1,560.8Â…, '2,634.1Â…, '2,410.3Â…, '83.5Â±2', '69.8', '39.95'
$ orbital_semi_major_axis_km     <f64> 384399.0, 9380.0, 23460.0, 421800.0, 671100.0, 1070400.0, 1882700.0, 181400.0, 11461000.0, 11741000.0
$ sidereal_period_d_r__retrogra… <obj> '27.32158…, '0.319', '1.262', '1.769', '3.551', '7.155', '16.69', '0.498', '250.56', '259.64'
$ discovery_year                 <obj> 'Prehisto…, '1877', '1877', '1610', '1610', '1610', '1610', '1892', '1904', '1905'
$ average_orbital_speed_kms      <obj> '1.022', '2.138', '1.351', '17.334', '13.7', '10.9', '8.2', '26.47', '3.34', '3.29'
$ mean_radius_km                 <obj> '1738', '11.267', '6.2Â±0.1…, '1,821.6Â…, '1,560.8Â…, '2,634.1Â…, '2,410.3Â…, '83.5Â±2', '69.8', '39.95'
$ average_orbital_speed_kms      <obj> '1.022', '2.138', '1.351', '17.334', '13.7', '10.9', '8.2', '26.47', '3.34', '3.29'
$ mean_radius_km                 <obj> '1738', '11.267', '6.2Â±0.1…, '1,821.6Â…, '1,560.8Â…, '2,634.1Â…, '2,410.3Â…, '83.5Â±2', '69.8', '39.95'
$ orbital_semi_major_axis_km     <f64> 384399.0, 9380.0, 23460.0, 421800.0, 671100.0, 1070400.0, 1882700.0, 181400.0, 11461000.0, 11741000.0
$ sidereal_period_d_r__retrogra… <obj> '27.32158…, '0.319', '1.262', '1.769', '3.551', '7.155', '16.69', '0.498', '250.56', '259.64'
$ discovery_year                 <obj> 'Prehisto…, '1877', '1877', '1610', '1610', '1610', '1610', '1892', '1904', '1905'
$ year_announced                 <obj> 'Prehisto…, '1877', '1877', '1610', '1610', '1610', '1610', '1892', '1905', '1905'
$ discovered_by                  <obj> 'Â€”', 'Hall', 'Hall', 'Galileo', 'Galileo', 'Galileo', 'Galileo', 'Barnard', 'Perrine', 'Perrine'
$ apparent_magnitudea            <obj> '-12.9 To…, '11.8', '12.89', '5.02', '5.29', '4.61', '5.65', '14.1', '14.6', '16.6'
$ notes                          <obj> 'Synchron…, 'Synchron…, 'Synchron…, 'Main-Gro…, 'Main-Gro…, 'Main-Gro…, 'Main-Gro…, 'Inner Mo…, 'Prograde…, 'Prograde…
$ refs                           <obj> '[12]', '[13][14]…, '[13][14]…, '[15][18]…, '[15][18]…, '[15][18]…, '[15][18]…, '[14][15]…, '[14][15]…, '[14][15]…
```
</details> 

#### 6. `not_in()`

<details>
<summary>View examples</summary>

We'll define a list of items to exclude inside of `filter()`, `select()` only the relevant columns, return only the first 10 rows, then use `affiche()` as a function:  

```python
list = ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

moons >> filter(_.parent.not_in(list)) \
    >> select(_.name, _.parent) \
    >> head(10) \
    >> affiche()
```

```
╔═══════════════════╦══════════╗
║ name              ║ parent   ║
║ obj               ║ obj      ║
╠═══════════════════╬══════════╣
║ Vanth             ║ Orcus    ║
║ Hiê»Iaka          ║ Haumea   ║
║ Namaka            ║ Haumea   ║
║ Weywot            ║ Quaoar   ║
║ S/2015 (136472) 1 ║ Makemake ║
║ Xiangliu          ║ Gonggong ║
║ Dysnomia          ║ Eris     ║
╚═══════════════════╩══════════╝
```

</details> 

#### 7. `not_like()`

<details>
<summary>View examples</summary>

Natively, `not_like()` supports regex string matching:

```python
moons >> filter(_.discovery_year.not_like("^16|17|18|19|20")) \
    >> select(_.name, _.parent, _.discovery_year) \
    >> affiche()
```

```
╔══════╦════════╦════════════════╗
║ name ║ parent ║ discovery_year ║
║ obj  ║ obj    ║ obj            ║
╠══════╬════════╬════════════════╣
║ Moon ║ Earth  ║ Prehistoric    ║
╚══════╩════════╩════════════════╝
```
</details> 

### Functions

#### 1. `select()`

<details>
<summary>View examples</summary>

The simplest way of using `select()` is to specify columns with the underscore accessor `_`:

```python
moons >> select(_.name, _.mean_radius_km, _.discovered_by) \
    >> head() \
    >> affiche()
```

```
╔═══════╦════════╦════════════════╦═══════════════╗
║ index ║ name   ║ mean_radius_km ║ discovered_by ║
║ int64 ║ obj    ║ obj            ║ obj           ║
╠═══════╬════════╬════════════════╬═══════════════╣
║ 0     ║ Moon   ║ 1738           ║ Â€”           ║
║ 1     ║ Phobos ║ 11.267         ║ Hall          ║
║ 2     ║ Deimos ║ 6.2Â±0.18      ║ Hall          ║
║ 3     ║ Io     ║ 1,821.6Â±0.5   ║ Galileo       ║
║ 4     ║ Europa ║ 1,560.8Â±0.5   ║ Galileo       ║
╚═══════╩════════╩════════════════╩═══════════════╝
```

We can also use the inverse operator `~` for de-selecting columns:

```python
moons >> select(~_.average_orbital_speed_kms, ~_.mean_radius_km, ~_.orbital_semi_major_axis_km, 
             ~_.sidereal_period_d_r__retrograde, ~_.discovery_year, ~_.year_announced, ~_.notes) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═══════╦═════════╦═════════╦═══════════════╦═════════════════════╦══════════════════╗
║ index ║ name   ║ image ║ parent  ║ numeral ║ discovered_by ║ apparent_magnitudea ║ refs             ║
║ int64 ║ obj    ║ obj   ║ obj     ║ obj     ║ obj           ║ obj                 ║ obj              ║
╠═══════╬════════╬═══════╬═════════╬═════════╬═══════════════╬═════════════════════╬══════════════════╣
║ 0     ║ Moon   ║ NA    ║ Earth   ║ I (1)   ║ Â€”           ║ -12.9 To -2.5       ║ [12]             ║
║ 1     ║ Phobos ║ NA    ║ Mars    ║ I (1)   ║ Hall          ║ 11.8                ║ [13][14][15][16] ║
║ 2     ║ Deimos ║ NA    ║ Mars    ║ Ii (2)  ║ Hall          ║ 12.89               ║ [13][14][15][17] ║
║ 3     ║ Io     ║ NA    ║ Jupiter ║ I (1)   ║ Galileo       ║ 5.02                ║ [15][18][19]     ║
║ 4     ║ Europa ║ NA    ║ Jupiter ║ Ii (2)  ║ Galileo       ║ 5.29                ║ [15][18][19]     ║
╚═══════╩════════╩═══════╩═════════╩═════════╩═══════════════╩═════════════════════╩══════════════════╝
```

As well as the column range operator `|` for specifying a range of columns:

```python
moons >> select(_.name | _.average_orbital_speed_kms) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═══════╦═════════╦═════════╦═══════════════════════════╗
║ index ║ name   ║ image ║ parent  ║ numeral ║ average_orbital_speed_kms ║
║ int64 ║ obj    ║ obj   ║ obj     ║ obj     ║ obj                       ║
╠═══════╬════════╬═══════╬═════════╬═════════╬═══════════════════════════╣
║ 0     ║ Moon   ║ NA    ║ Earth   ║ I (1)   ║ 1.022                     ║
║ 1     ║ Phobos ║ NA    ║ Mars    ║ I (1)   ║ 2.138                     ║
║ 2     ║ Deimos ║ NA    ║ Mars    ║ Ii (2)  ║ 1.351                     ║
║ 3     ║ Io     ║ NA    ║ Jupiter ║ I (1)   ║ 17.334                    ║
║ 4     ║ Europa ║ NA    ║ Jupiter ║ Ii (2)  ║ 13.7                      ║
╚═══════╩════════╩═══════╩═════════╩═════════╩═══════════════════════════╝
```

We can also use the unpacking operator `*` in `select()`:

```python
cols = ["name", "numeral", "apparent_magnitudea"]

moons >> select(*cols) \
    >> head(5) \
    >> affiche()
```
```
╔═══════╦════════╦═════════╦═════════════════════╗
║ index ║ name   ║ numeral ║ apparent_magnitudea ║
║ int64 ║ obj    ║ obj     ║ obj                 ║
╠═══════╬════════╬═════════╬═════════════════════╣
║ 0     ║ Moon   ║ I (1)   ║ -12.9 To -2.5       ║
║ 1     ║ Phobos ║ I (1)   ║ 11.8                ║
║ 2     ║ Deimos ║ Ii (2)  ║ 12.89               ║
║ 3     ║ Io     ║ I (1)   ║ 5.02                ║
║ 4     ║ Europa ║ Ii (2)  ║ 5.29                ║
╚═══════╩════════╩═════════╩═════════════════════╝
```

Further, `select()` allows for various selector functions: `starts_with()`, `ends_with()` and `contains()` 

```python
moons >> select(ends_with("km")) \
    >> head(5) \
    >> affiche()
```
```
╔═══════╦════════════════╦════════════════════════════╗
║ index ║ mean_radius_km ║ orbital_semi_major_axis_km ║
║ int64 ║ obj            ║ float64                    ║
╠═══════╬════════════════╬════════════════════════════╣
║ 0     ║ 1738           ║ 384399.0                   ║
║ 1     ║ 11.267         ║ 9380.0                     ║
║ 2     ║ 6.2Â±0.18      ║ 23460.0                    ║
║ 3     ║ 1,821.6Â±0.5   ║ 421800.0                   ║
║ 4     ║ 1,560.8Â±0.5   ║ 671100.0                   ║
╚═══════╩════════════════╩════════════════════════════╝
```

As well as using the inverse operator `~` on these helpers:

```python
moons >> select(~(_.image | _.year_announced), ~ends_with("by")) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════════════════╦═══════════════════════════════╦══════════════════╗
║ index ║ name   ║ apparent_magnitudea ║ notes                         ║ refs             ║
║ int64 ║ obj    ║ obj                 ║ obj                           ║ obj              ║
╠═══════╬════════╬═════════════════════╬═══════════════════════════════╬══════════════════╣
║ 0     ║ Moon   ║ -12.9 To -2.5       ║ Synchronous Rotation (Binary) ║ [12]             ║
║ 1     ║ Phobos ║ 11.8                ║ Synchronous Rotation          ║ [13][14][15][16] ║
║ 2     ║ Deimos ║ 12.89               ║ Synchronous Rotation          ║ [13][14][15][17] ║
║ 3     ║ Io     ║ 5.02                ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
║ 4     ║ Europa ║ 5.29                ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
╚═══════╩════════╩═════════════════════╩═══════════════════════════════╩══════════════════╝
```

</details> 

#### 2. `filter()`

<details>
<summary>View examples</summary>

Intuitively, `filter()` takes one or more arguments for finding rows that match certain conditions:

```python
moons >> filter(_.parent == "Saturn", _.orbital_semi_major_axis_km >= 2500000) \
    >> select(_.parent, _.orbital_semi_major_axis_km) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦════════════════════════════╗
║ index ║ parent ║ orbital_semi_major_axis_km ║
║ int64 ║ obj    ║ float64                    ║
╠═══════╬════════╬════════════════════════════╣
║ 107   ║ Saturn ║ 3560840.0                  ║
║ 108   ║ Saturn ║ 12947780.0                 ║
║ 118   ║ Saturn ║ 23140400.0                 ║
║ 119   ║ Saturn ║ 15200000.0                 ║
║ 120   ║ Saturn ║ 17983000.0                 ║
╚═══════╩════════╩════════════════════════════╝
```

There's also a helper function `row_contains()` for filtering for any rows that match any given value[s]:

```python
moons >> filter(row_contains("Â")) \
    >> select(_.mean_radius_km, _.discovered_by) \
    >> head(10) \
    >> affiche()
```
```
╔═══════╦════════════════╦═══════════════════════════════╗
║ index ║ mean_radius_km ║ discovered_by                 ║
║ int64 ║ obj            ║ obj                           ║
╠═══════╬════════════════╬═══════════════════════════════╣
║ 0     ║ 1738           ║ Â€”                           ║
║ 2     ║ 6.2Â±0.18      ║ Hall                          ║
║ 3     ║ 1,821.6Â±0.5   ║ Galileo                       ║
║ 4     ║ 1,560.8Â±0.5   ║ Galileo                       ║
║ 5     ║ 2,634.1Â±0.3   ║ Galileo                       ║
║ 6     ║ 2,410.3Â±1.5   ║ Galileo                       ║
║ 7     ║ 83.5Â±2        ║ Barnard                       ║
║ 16    ║ 49.3Â±2.0      ║ Synnott (Voyager 1)           ║
║ 17    ║ 8.2Â±2.0       ║ Jewitt, Danielson (Voyager 1) ║
║ 18    ║ 21.5Â±2.0      ║ Synnott (Voyager 1)           ║
╚═══════╩════════════════╩═══════════════════════════════╝
```

</details> 

#### 3. `mutate()`

<details>
<summary>View examples</summary>

Conventionally, `mutate()` can be used to either modify columns in place or create new columns:

```python
moons >> mutate(prehistoric = _.discovery_year == "Prehistoric") \
    >> select(_.name, _.discovery_year, _.prehistoric) \
    >> distinct(_.name, _.discovery_year) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦════════════════╦═════════════╗
║ index ║ name   ║ discovery_year ║ prehistoric ║
║ int64 ║ obj    ║ obj            ║ bool        ║
╠═══════╬════════╬════════════════╬═════════════╣
║ 0     ║ Moon   ║ Prehistoric    ║ True        ║
║ 1     ║ Phobos ║ 1877           ║ False       ║
║ 2     ║ Deimos ║ 1877           ║ False       ║
║ 3     ║ Io     ║ 1610           ║ False       ║
║ 4     ║ Europa ║ 1610           ║ False       ║
╚═══════╩════════╩════════════════╩═════════════╝
```

But we can also specify `_before` or `_after` positional arguments: 

```python
moons >> mutate(color = None, _after = "parent") \
    >> select(_.name | _.color) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═══════╦═════════╦═══════╗
║ index ║ name   ║ image ║ parent  ║ color ║
║ int64 ║ obj    ║ obj   ║ obj     ║ obj   ║
╠═══════╬════════╬═══════╬═════════╬═══════╣
║ 0     ║ Moon   ║ NA    ║ Earth   ║ NA    ║
║ 1     ║ Phobos ║ NA    ║ Mars    ║ NA    ║
║ 2     ║ Deimos ║ NA    ║ Mars    ║ NA    ║
║ 3     ║ Io     ║ NA    ║ Jupiter ║ NA    ║
║ 4     ║ Europa ║ NA    ║ Jupiter ║ NA    ║
╚═══════╩════════╩═══════╩═════════╩═══════╝
```

Importantly, `mutate()` allows for applying transformations across multiple columns with `across()`:

```python
cols = ["name", "parent", "discovered_by"]

moons >> mutate(across(cols, lambda x: x.str.upper())) \
    >> select(*cols) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════╦═══════════════╗
║ index ║ name   ║ parent  ║ discovered_by ║
║ int64 ║ obj    ║ obj     ║ obj           ║
╠═══════╬════════╬═════════╬═══════════════╣
║ 0     ║ MOON   ║ EARTH   ║ Â€”           ║
║ 1     ║ PHOBOS ║ MARS    ║ HALL          ║
║ 2     ║ DEIMOS ║ MARS    ║ HALL          ║
║ 3     ║ IO     ║ JUPITER ║ GALILEO       ║
║ 4     ║ EUROPA ║ JUPITER ║ GALILEO       ║
╚═══════╩════════╩═════════╩═══════════════╝
```

We can even use the selector helpers — `starts_with()`, `ends_with()` and `contains()` — within our `across()` call:

```python
moons >> mutate(across(ends_with("km|kms"), lambda x: pd.to_numeric(x, errors = "coerce"))) \
    >> select(ends_with("km|kms")) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═══════════════════════════╦════════════════╦════════════════════════════╗
║ index ║ average_orbital_speed_kms ║ mean_radius_km ║ orbital_semi_major_axis_km ║
║ int64 ║ float64                   ║ float64        ║ float64                    ║
╠═══════╬═══════════════════════════╬════════════════╬════════════════════════════╣
║ 0     ║ 1.022                     ║ 1738.0         ║ 384399.0                   ║
║ 1     ║ 2.138                     ║ 11.267         ║ 9380.0                     ║
║ 2     ║ 1.351                     ║ NA             ║ 23460.0                    ║
║ 3     ║ 17.334                    ║ NA             ║ 421800.0                   ║
║ 4     ║ 13.7                      ║ NA             ║ 671100.0                   ║
╚═══════╩═══════════════════════════╩════════════════╩════════════════════════════╝
```

We also have access to the following helper functions within `where()`: `is_numeric`, `is_integer`, `is_float`, `is_object`, `is_boolean`, `is_temporal` and `is_cat`:

```python
moons >> mutate(across(where(is_object), lambda x: x.str.lower())) \
    >> select(where(is_object), ~_.image, ~ends_with("km|kms")) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════╦═════════╦═════════════════════════════════╦════════════════╦════════════════╦═══════════════╦═════════════════════╦═══════════════════════════════╦══════════════════╗
║ index ║ name   ║ parent  ║ numeral ║ sidereal_period_d_r__retrograde ║ discovery_year ║ year_announced ║ discovered_by ║ apparent_magnitudea ║ notes                         ║ refs             ║
║ int64 ║ obj    ║ obj     ║ obj     ║ obj                             ║ obj            ║ obj            ║ obj           ║ obj                 ║ obj                           ║ obj              ║
╠═══════╬════════╬═════════╬═════════╬═════════════════════════════════╬════════════════╬════════════════╬═══════════════╬═════════════════════╬═══════════════════════════════╬══════════════════╣
║ 0     ║ moon   ║ earth   ║ i (1)   ║ 27.321582                       ║ prehistoric    ║ prehistory     ║ â€”           ║ -12.9 to -2.5       ║ synchronous rotation (binary) ║ [12]             ║
║ 1     ║ phobos ║ mars    ║ i (1)   ║ 0.319                           ║ 1877           ║ 1877           ║ hall          ║ 11.8                ║ synchronous rotation          ║ [13][14][15][16] ║
║ 2     ║ deimos ║ mars    ║ ii (2)  ║ 1.262                           ║ 1877           ║ 1877           ║ hall          ║ 12.89               ║ synchronous rotation          ║ [13][14][15][17] ║
║ 3     ║ io     ║ jupiter ║ i (1)   ║ 1.769                           ║ 1610           ║ 1610           ║ galileo       ║ 5.02                ║ main-group moon (galilean)    ║ [15][18][19]     ║
║ 4     ║ europa ║ jupiter ║ ii (2)  ║ 3.551                           ║ 1610           ║ 1610           ║ galileo       ║ 5.29                ║ main-group moon (galilean)    ║ [15][18][19]     ║
╚═══════╩════════╩═════════╩═════════╩═════════════════════════════════╩════════════════╩════════════════╩═══════════════╩═════════════════════╩═══════════════════════════════╩══════════════════╝
```

`mutate()` also allows for arithmetic operators (e.g. `+`, `*`, `/`) to be used across columns:

```python
moons >> mutate(across(contains("year"), lambda x: pd.to_numeric(x, errors = "coerce"))) \
    >> mutate(announcement_lag = _.year_announced - _.discovery_year, 
                _after = "year_announced") \
    >> select(_.name, _.discovery_year | _.announcement_lag) \
    >> distinct(_.announcement_lag) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════════╦════════════════╦════════════════╦══════════════════╗
║ index ║ name        ║ discovery_year ║ year_announced ║ announcement_lag ║
║ int64 ║ obj         ║ float64        ║ float64        ║ float64          ║
╠═══════╬═════════════╬════════════════╬════════════════╬══════════════════╣
║ 0     ║ Moon        ║ NA             ║ NA             ║ NA               ║
║ 1     ║ Phobos      ║ 1877.0         ║ 1877.0         ║ 0.0              ║
║ 8     ║ Himalia     ║ 1904.0         ║ 1905.0         ║ 1.0              ║
║ 64    ║ Valetudo    ║ 2016.0         ║ 2018.0         ║ 2.0              ║
║ 82    ║ S/2003 J 24 ║ 2003.0         ║ 2021.0         ║ 18.0             ║
╚═══════╩═════════════╩════════════════╩════════════════╩══════════════════╝
```

Additionally, we can use `if_else()` for conditional column modification:

```python
moons >> mutate(
    synchronous = if_else(
        condition = _.notes.str.contains("Synchronous", case = False),
        true = True,
        false = False
    ), after = "notes") \
    >> select(_.name, _.notes, _.synchronous) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═══════════════════════════════╦═════════════╗
║ index ║ name   ║ notes                         ║ synchronous ║
║ int64 ║ obj    ║ obj                           ║ bool        ║
╠═══════╬════════╬═══════════════════════════════╬═════════════╣
║ 0     ║ Moon   ║ Synchronous Rotation (Binary) ║ True        ║
║ 1     ║ Phobos ║ Synchronous Rotation          ║ True        ║
║ 2     ║ Deimos ║ Synchronous Rotation          ║ True        ║
║ 3     ║ Io     ║ Main-Group Moon (Galilean)    ║ False       ║
║ 4     ║ Europa ║ Main-Group Moon (Galilean)    ║ False       ║
╚═══════╩════════╩═══════════════════════════════╩═════════════╝
```

As well as `case_when()` for multiple conditionals:

```python
moons >> mutate(
    orbit = case_when(
        (_.notes.str.contains("Retrograde", case = False), "Retrograde"),
        (_.notes.str.contains("Prograde", case = False), "Prograde"),
        (_.notes.str.contains("Synchronous", case = False), "Synchronous"),
        (_.notes.str.contains("Main-Group", case = False), "Main-Group"),
        (_.notes.str.contains("Chaotic", case = False), "Chaotic"),
        (_.notes.isna(), None),
        default = "Other"
    ), _after = "parent") \
    >> select(_.name, _.notes, _.orbit) \
    >> distinct(_.orbit) \
    >> head() \
    >> affiche()
```
```
╔═══════╦══════════╦═════════════════════════════════╦═════════════╗
║ index ║ name     ║ notes                           ║ orbit       ║
║ int64 ║ obj      ║ obj                             ║ obj         ║
╠═══════╬══════════╬═════════════════════════════════╬═════════════╣
║ 0     ║ Moon     ║ Synchronous Rotation (Binary)   ║ Synchronous ║
║ 3     ║ Io       ║ Main-Group Moon (Galilean)      ║ Main-Group  ║
║ 7     ║ Amalthea ║ Inner Moon (Amalthea)           ║ Other       ║
║ 8     ║ Himalia  ║ Prograde Irregular (Himalia)    ║ Prograde    ║
║ 10    ║ Pasiphae ║ Retrograde Irregular (Pasiphae) ║ Retrograde  ║
╚═══════╩══════════╩═════════════════════════════════╩═════════════╝
```

</details> 

#### 4. `group_by()` + `summarize()`

<details>
<summary>View examples</summary>

```python
moons >> group_by(_.parent) \
    >> summarize(avg_orbital_semi_major_axis_km = _.orbital_semi_major_axis_km.mean().round()) \
    >> affiche()
```

```
╔═══════╦══════════╦════════════════════════════════╗
║ index ║ parent   ║ avg_orbital_semi_major_axis_km ║
║ int64 ║ obj      ║ float64                        ║
╠═══════╬══════════╬════════════════════════════════╣
║ 0     ║ Earth    ║ 384399.0                       ║
║ 1     ║ Eris     ║ NA                             ║
║ 2     ║ Gonggong ║ NA                             ║
║ 3     ║ Haumea   ║ 37768.0                        ║
║ 4     ║ Jupiter  ║ 19273786.0                     ║
║ 5     ║ Makemake ║ NA                             ║
║ 6     ║ Mars     ║ 16420.0                        ║
║ 7     ║ Neptune  ║ 14823105.0                     ║
║ 8     ║ Orcus    ║ NA                             ║
║ 9     ║ Pluto    ║ 46616.0                        ║
║ 10    ║ Quaoar   ║ NA                             ║
║ 11    ║ Saturn   ║ 17831573.0                     ║
║ 12    ║ Uranus   ║ 4271309.0                      ║
╚═══════╩══════════╩════════════════════════════════╝
```

</details> 

#### 5. `group_by()` + `reframe()`

<details>
<summary>View examples</summary>

Unlike `summarize()`, `reframe()` in a `group_by()` creates new rows based on group summaries:

```python
moons >> group_by(_.parent) \
    >> reframe(
        avg_orbital_semi_major_axis_km = _.orbital_semi_major_axis_km.mean().round(),
        avg_orbital_speed_kms = _.average_orbital_speed_kms.replace("(Unsure)", 0) \
            .astype("Float64", errors = "ignore").mean().astype("Float64", errors = "ignore") \
                .round()
        ) \
    >> affiche()
```
```
╔══════════╦════════════════════════════════╦═══════════════════════╗
║ index    ║ avg_orbital_semi_major_axis_km ║ avg_orbital_speed_kms ║
║ obj      ║ float64                        ║ float64               ║
╠══════════╬════════════════════════════════╬═══════════════════════╣
║ Earth    ║ 384399.0                       ║ 1.0                   ║
║ Eris     ║ NA                             ║ NA                    ║
║ Gonggong ║ NA                             ║ NA                    ║
║ Haumea   ║ 37768.0                        ║ NA                    ║
║ Jupiter  ║ 19273786.0                     ║ 12.0                  ║
║ Makemake ║ NA                             ║ NA                    ║
║ Mars     ║ 16420.0                        ║ 2.0                   ║
║ Neptune  ║ 14823105.0                     ║ NA                    ║
║ Orcus    ║ NA                             ║ NA                    ║
║ Pluto    ║ 46616.0                        ║ NA                    ║
║ Quaoar   ║ NA                             ║ NA                    ║
║ Saturn   ║ 17831573.0                     ║ 9.0                   ║
║ Uranus   ║ 4271309.0                      ║ NA                    ║
╚══════════╩════════════════════════════════╩═══════════════════════╝
```

</details> 

#### 6. `pull()`

<details>
<summary>View examples</summary>

Similar to `R`, we can use `pull()` to retrieve a single value or a list:


```python
# Pull the number of moons around Jupiter
n = moons >> filter(_.parent == "Jupiter") \
    >> summarize(count = _.name.count()) \
    >> pull(_.count)

# Return it in a formatted string
print(f"The number of moons around Jupiter is: {n}")
```
```
The number of moons around Jupiter is: 97
```

</details> 

#### 7. `join()`

<details>
<summary>View examples</summary>

We can specify the type of join in the "how" argument:

```python
# First, define a new dataframe
df = pd.DataFrame({
    "name": ["Moon", "Phobos", "Deimos", "Io", "Europa"], 
    "designation": ["Moon", "Mars I", "Mars II", "Jupiter I", "Jupiter II"],
    "periapsis_km": [363300, 9234, 23445, 420000, 664862]
})

# Perform a right join between the two
df2 = moons >> join(
    df, 
    left_on = "name",
    right_on = "name",
    how = "right"
)   >> select(_.name, _.parent, _.designation, _.periapsis_km) \
    >> affiche()
```
```
╔═══════╦════════╦═════════╦═════════════╦══════════════╗
║ index ║ name   ║ parent  ║ designation ║ periapsis_km ║
║ int64 ║ obj    ║ obj     ║ obj         ║ int64        ║
╠═══════╬════════╬═════════╬═════════════╬══════════════╣
║ 0     ║ Moon   ║ Earth   ║ Moon        ║ 363300       ║
║ 1     ║ Phobos ║ Mars    ║ Mars I      ║ 9234         ║
║ 2     ║ Deimos ║ Mars    ║ Mars II     ║ 23445        ║
║ 3     ║ Io     ║ Jupiter ║ Jupiter I   ║ 420000       ║
║ 4     ║ Europa ║ Jupiter ║ Jupiter II  ║ 664862       ║
╚═══════╩════════╩═════════╩═════════════╩══════════════╝
```

</details> 

#### 8. `pivot_wider()`

<details>
<summary>View examples</summary>

By default, `pivot_wider()` fills empty cells with `NA`:

```python
moons_wide = moons >> \
    pivot_wider(names_from = _.parent, 
                  values_from=_.mean_radius_km, 
                  id_cols = _.name) 

moons_wide.head(10).affiche()
```
```
╔═══════╦══════════╦═══════╦══════╦══════════╦════════╦══════════╦══════════╦══════╦═════════╦═══════╦═══════╦════════╦════════╦════════╗
║ index ║ name     ║ Earth ║ Eris ║ Gonggong ║ Haumea ║ Jupiter  ║ Makemake ║ Mars ║ Neptune ║ Orcus ║ Pluto ║ Quaoar ║ Saturn ║ Uranus ║
║ i64   ║ obj      ║ obj   ║ obj  ║ obj      ║ obj    ║ obj      ║ obj      ║ obj  ║ obj     ║ obj   ║ obj   ║ obj    ║ obj    ║ obj    ║
╠═══════╬══════════╬═══════╬══════╬══════════╬════════╬══════════╬══════════╬══════╬═════════╬═══════╬═══════╬════════╬════════╬════════╣
║ 0     ║ Adrastea ║ NA    ║ NA   ║ NA       ║ NA     ║ 8.2Â±2.0 ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ NA     ║ NA     ║
║ 1     ║ Aegaeon  ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 0.33   ║ NA     ║
║ 2     ║ Aegir    ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 3      ║ NA     ║
║ 3     ║ Aitne    ║ NA    ║ NA   ║ NA       ║ NA     ║ 1.5      ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ NA     ║ NA     ║
║ 4     ║ Albiorix ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 14.3   ║ NA     ║
║ 5     ║ Alvaldi  ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 6      ║ NA     ║
║ 6     ║ Amalthea ║ NA    ║ NA   ║ NA       ║ NA     ║ 83.5Â±2  ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ NA     ║ NA     ║
║ 7     ║ Ananke   ║ NA    ║ NA   ║ NA       ║ NA     ║ 14.55    ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ NA     ║ NA     ║
║ 8     ║ Angrboda ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 3      ║ NA     ║
║ 9     ║ Anthe    ║ NA    ║ NA   ║ NA       ║ NA     ║ NA       ║ NA       ║ NA   ║ NA      ║ NA    ║ NA    ║ NA     ║ 0.9    ║ NA     ║
╚═══════╩══════════╩═══════╩══════╩══════════╩════════╩══════════╩══════════╩══════╩═════════╩═══════╩═══════╩════════╩════════╩════════╝
```

</details> 

#### 9. `pivot_longer()`

<details>
<summary>View examples</summary>

By default, `pivot_longer()` pivots all columns:

```python
# Pivot all columns except name
moons_wide >> pivot_longer(cols = ~_.name, 
                   names_to = "parent", 
                   values_to = "mean_radius_km") \
    >> filter(_.mean_radius_km.notna()) \
    >> head(10) \
    >> affiche()
```
```
╔═══════╦══════════╦══════════╦════════════════╗
║ index ║ name     ║ parent   ║ mean_radius_km ║
║ int64 ║ obj      ║ obj      ║ obj            ║
╠═══════╬══════════╬══════════╬════════════════╣
║ 108   ║ Moon     ║ Earth    ║ 1738           ║
║ 470   ║ Dysnomia ║ Eris     ║ 350Â±60[8]     ║
║ 1291  ║ Xiangliu ║ Gonggong ║ <100[171]      ║
║ 1369  ║ Hiê»Iaka ║ Haumea   ║ Â‰ˆ160         ║
║ 1404  ║ Namaka   ║ Haumea   ║ Â‰ˆ85          ║
║ 1724  ║ Adrastea ║ Jupiter  ║ 8.2Â±2.0       ║
║ 1727  ║ Aitne    ║ Jupiter  ║ 1.5            ║
║ 1730  ║ Amalthea ║ Jupiter  ║ 83.5Â±2        ║
║ 1731  ║ Ananke   ║ Jupiter  ║ 14.55          ║
║ 1734  ║ Aoede    ║ Jupiter  ║ 2              ║
╚═══════╩══════════╩══════════╩════════════════╝
```

</details> 

#### 10. `unite()`

<details>
<summary>View examples</summary>

By default, `unite()` drops the "from" columns:

```python
moons >> unite("combined", ["name", "parent"], sep=", ") \
    >> select(_.combined) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════════════╗
║ index ║ combined        ║
║ int64 ║ obj             ║
╠═══════╬═════════════════╣
║ 0     ║ Moon, Earth     ║
║ 1     ║ Phobos, Mars    ║
║ 2     ║ Deimos, Mars    ║
║ 3     ║ Io, Jupiter     ║
║ 4     ║ Europa, Jupiter ║
╚═══════╩═════════════════╝
```

</details> 

#### 11. `separate()`

<details>
<summary>View examples</summary>

Similarly, `separate()` drops the "from" column by default:

```python
moons >> unite("combined", ["name", "parent"], sep=", ") \
    >> separate(_.combined, into = ["name", "parent"], sep=", ") \
    >> select(_.name, _.parent) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦═════════╗
║ index ║ name   ║ parent  ║
║ int64 ║ obj    ║ obj     ║
╠═══════╬════════╬═════════╣
║ 0     ║ Moon   ║ Earth   ║
║ 1     ║ Phobos ║ Mars    ║
║ 2     ║ Deimos ║ Mars    ║
║ 3     ║ Io     ║ Jupiter ║
║ 4     ║ Europa ║ Jupiter ║
╚═══════╩════════╩═════════╝
```

</details> 

#### 12. `bind_cols()`

<details>
<summary>View examples</summary>

The default behavior of `bind_cols()` is to append `_2` to columns with conflicting names:

```python
df = pd.DataFrame({
    "name": ["Moon", "Phobos", "Deimos", "Io", "Europa"], 
    "designation": ["Moon", "Mars I", "Mars II", "Jupiter I", "Jupiter II"],
    "periapsis_km": [363300, 9234, 23445, 420000, 664862]
})

moons >> bind_cols(df) \
    >> select(_.name, _.parent, _.designation, _.periapsis_km) \
    >> head(10) \
    >> affiche()
```

```
╔═══════╦══════════╦═════════╦═════════════╦══════════════╗
║ index ║ name     ║ parent  ║ designation ║ periapsis_km ║
║ int64 ║ obj      ║ obj     ║ obj         ║ float64      ║
╠═══════╬══════════╬═════════╬═════════════╬══════════════╣
║ 0     ║ Moon     ║ Earth   ║ Moon        ║ 363300.0     ║
║ 1     ║ Phobos   ║ Mars    ║ Mars I      ║ 9234.0       ║
║ 2     ║ Deimos   ║ Mars    ║ Mars II     ║ 23445.0      ║
║ 3     ║ Io       ║ Jupiter ║ Jupiter I   ║ 420000.0     ║
║ 4     ║ Europa   ║ Jupiter ║ Jupiter II  ║ 664862.0     ║
║ 5     ║ Ganymede ║ Jupiter ║ NA          ║ NA           ║
║ 6     ║ Callisto ║ Jupiter ║ NA          ║ NA           ║
║ 7     ║ Amalthea ║ Jupiter ║ NA          ║ NA           ║
║ 8     ║ Himalia  ║ Jupiter ║ NA          ║ NA           ║
║ 9     ║ Elara    ║ Jupiter ║ NA          ║ NA           ║
╚═══════╩══════════╩═════════╩═════════════╩══════════════╝
```

</details> 

#### 13. `bind_rows()`

<details>
<summary>View examples</summary>

By default, `bind_rows()` fills missing cells with `NA`:

```python
df = pd.DataFrame({
    "name": ["Moon", "Phobos", "Deimos", "Io", "Europa"], 
    "designation": ["Moon", "Mars I", "Mars II", "Jupiter I", "Jupiter II"],
    "periapsis_km": [363300, 9234, 23445, 420000, 664862]
})

moons >> bind_rows(df) \
    >> select(_.name, _.parent, _.designation, _.periapsis_km) \
    >> tail(10) \
    >> affiche()
```

```
╔═══════╦═══════════════════╦══════════╦═════════════╦══════════════╗
║ index ║ name              ║ parent   ║ designation ║ periapsis_km ║
║ int64 ║ obj               ║ obj      ║ obj         ║ float64      ║
╠═══════╬═══════════════════╬══════════╬═════════════╬══════════════╣
║ 426   ║ Namaka            ║ Haumea   ║ NA          ║ NA           ║
║ 427   ║ Weywot            ║ Quaoar   ║ NA          ║ NA           ║
║ 428   ║ S/2015 (136472) 1 ║ Makemake ║ NA          ║ NA           ║
║ 429   ║ Xiangliu          ║ Gonggong ║ NA          ║ NA           ║
║ 430   ║ Dysnomia          ║ Eris     ║ NA          ║ NA           ║
║ 431   ║ Moon              ║ NA       ║ Moon        ║ 363300.0     ║
║ 432   ║ Phobos            ║ NA       ║ Mars I      ║ 9234.0       ║
║ 433   ║ Deimos            ║ NA       ║ Mars II     ║ 23445.0      ║
║ 434   ║ Io                ║ NA       ║ Jupiter I   ║ 420000.0     ║
║ 435   ║ Europa            ║ NA       ║ Jupiter II  ║ 664862.0     ║
╚═══════╩═══════════════════╩══════════╩═════════════╩══════════════╝
```

</details> 

#### 14. `head()`

<details>
<summary>View examples</summary>

The default is 5 rows, but can be specified:

```python
moons >> select(_.parent, _.notes) \
    >> head(10) \
    >> affiche()
```
```
╔═══════╦═════════╦═══════════════════════════════╗
║ index ║ parent  ║ notes                         ║
║ int64 ║ obj     ║ obj                           ║
╠═══════╬═════════╬═══════════════════════════════╣
║ 0     ║ Earth   ║ Synchronous Rotation (Binary) ║
║ 1     ║ Mars    ║ Synchronous Rotation          ║
║ 2     ║ Mars    ║ Synchronous Rotation          ║
║ 3     ║ Jupiter ║ Main-Group Moon (Galilean)    ║
║ 4     ║ Jupiter ║ Main-Group Moon (Galilean)    ║
║ 5     ║ Jupiter ║ Main-Group Moon (Galilean)    ║
║ 6     ║ Jupiter ║ Main-Group Moon (Galilean)    ║
║ 7     ║ Jupiter ║ Inner Moon (Amalthea)         ║
║ 8     ║ Jupiter ║ Prograde Irregular (Himalia)  ║
║ 9     ║ Jupiter ║ Prograde Irregular (Himalia)  ║
╚═══════╩═════════╩═══════════════════════════════╝
```

</details> 

#### 15. `tail()`

<details>
<summary>View examples</summary>

Similar to `head()`, default of 5 with an optional argument:

```python
moons >> select(_.parent, _.notes) \
    >> tail(2) \
    >> affiche()
```
```
╔═══════╦══════════╦═══════════════════════════════╗
║ index ║ parent   ║ notes                         ║
║ int64 ║ obj      ║ obj                           ║
╠═══════╬══════════╬═══════════════════════════════╣
║ 429   ║ Gonggong ║ Assuming A Prograde Orbit     ║
║ 430   ║ Eris     ║ Synchronous Rotation (Binary) ║
╚═══════╩══════════╩═══════════════════════════════╝
```

</details> 

#### 16. `slice()`

<details>
<summary>View examples</summary>

With one argument, `slice()` accesses rows at that position — here, the last five rows (-5):

```python
moons >> select(_.name | _.numeral) \
    >> slice(-5) \
    >> affiche()
```
```
╔═══════╦═══════════════════╦═══════╦══════════╦═════════╗
║ index ║ name              ║ image ║ parent   ║ numeral ║
║ int64 ║ obj               ║ obj   ║ obj      ║ obj     ║
╠═══════╬═══════════════════╬═══════╬══════════╬═════════╣
║ 426   ║ Namaka            ║ NA    ║ Haumea   ║ Ii (2)  ║
║ 427   ║ Weywot            ║ NA    ║ Quaoar   ║ I (1)   ║
║ 428   ║ S/2015 (136472) 1 ║ NA    ║ Makemake ║ Â€”     ║
║ 429   ║ Xiangliu          ║ NA    ║ Gonggong ║ I (1)   ║
║ 430   ║ Dysnomia          ║ NA    ║ Eris     ║ I (1)   ║
╚═══════╩═══════════════════╩═══════╩══════════╩═════════╝
```

But with two arguments, it grabs the starting position (100), followed by the number of rows (5):

```python
moons >> select(_.name | _.numeral) \
    >> slice(100, 5) \
    >> affiche()
```
```
╔═══════╦═══════════╦═══════╦════════╦═════════╗
║ index ║ name      ║ image ║ parent ║ numeral ║
║ int64 ║ obj       ║ obj   ║ obj    ║ obj     ║
╠═══════╬═══════════╬═══════╬════════╬═════════╣
║ 100   ║ Mimas     ║ NA    ║ Saturn ║ I (1)   ║
║ 101   ║ Enceladus ║ NA    ║ Saturn ║ Ii (2)  ║
║ 102   ║ Tethys    ║ NA    ║ Saturn ║ Iii (3) ║
║ 103   ║ Dione     ║ NA    ║ Saturn ║ Iv (4)  ║
║ 104   ║ Rhea      ║ NA    ║ Saturn ║ V (5)   ║
╚═══════╩═══════════╩═══════╩════════╩═════════╝
```

</details> 

#### 17. `sample()`

<details>
<summary>View examples</summary>

By default, `sample()` returns rows without replacement:

```python
moons >> select(_.name | _.numeral) \
    >> sample(10) \
    >> affiche()
```
```
╔═══════╦═════════════╦═══════╦═════════╦═══════════╗
║ index ║ name        ║ image ║ parent  ║ numeral   ║
║ int64 ║ obj         ║ obj   ║ obj     ║ obj       ║
╠═══════╬═════════════╬═══════╬═════════╬═══════════╣
║ 387   ║ Belinda     ║ NA    ║ Uranus  ║ Xiv (14)  ║
║ 311   ║ S/2020 S 32 ║ NA    ║ Saturn  ║ Â€”       ║
║ 143   ║ Hyrrokkin   ║ NA    ║ Saturn  ║ Xliv (44) ║
║ 409   ║ Larissa     ║ NA    ║ Neptune ║ Vii (7)   ║
║ 95    ║ S/2021 J 5  ║ NA    ║ Jupiter ║ Â€”       ║
║ 163   ║ S/2004 S 34 ║ NA    ║ Saturn  ║ Lxiv (64) ║
║ 94    ║ S/2021 J 4  ║ NA    ║ Jupiter ║ Â€”       ║
║ 212   ║ S/2006 S 16 ║ NA    ║ Saturn  ║ Â€”       ║
║ 371   ║ S/2023 S 48 ║ NA    ║ Saturn  ║ Â€”       ║
║ 220   ║ S/2006 S 24 ║ NA    ║ Saturn  ║ Â€”       ║
╚═══════╩═════════════╩═══════╩═════════╩═══════════╝
```

</details> 

#### 18. `distinct()`

<details>
<summary>View examples</summary>

The default behavior of `distinct()` is application to all columns, but can be specified: 

```python
moons >> select(_.parent, _.numeral) \
    >> distinct(_.numeral) \
    >> head(10) \
    >> affiche()
```
```
╔═══════╦═════════╦══════════╗
║ index ║ parent  ║ numeral  ║
║ int64 ║ obj     ║ obj      ║
╠═══════╬═════════╬══════════╣
║ 0     ║ Earth   ║ I (1)    ║
║ 2     ║ Mars    ║ Ii (2)   ║
║ 5     ║ Jupiter ║ Iii (3)  ║
║ 6     ║ Jupiter ║ Iv (4)   ║
║ 7     ║ Jupiter ║ V (5)    ║
║ 8     ║ Jupiter ║ Vi (6)   ║
║ 9     ║ Jupiter ║ Vii (7)  ║
║ 10    ║ Jupiter ║ Viii (8) ║
║ 11    ║ Jupiter ║ Ix (9)   ║
║ 12    ║ Jupiter ║ X (10)   ║
╚═══════╩═════════╩══════════╝
```

</details> 

#### 19. `arrange()`

<details>
<summary>View examples</summary>

By default, `arrange()` sorts ascending:

```python
moons >> select(_.name, _.orbital_semi_major_axis_km) \
    >> arrange(_.orbital_semi_major_axis_km) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦════════════════════════════╗
║ index ║ name   ║ orbital_semi_major_axis_km ║
║ int64 ║ obj    ║ float64                    ║
╠═══════╬════════╬════════════════════════════╣
║ 1     ║ Phobos ║ 9380.0                     ║
║ 420   ║ Charon ║ 19591.0                    ║
║ 2     ║ Deimos ║ 23460.0                    ║
║ 426   ║ Namaka ║ 25657.0                    ║
║ 424   ║ Styx   ║ 42393.0                    ║
╚═══════╩════════╩════════════════════════════╝
```

But we can use the `-` operator to sort descending:

```python
moons >> select(_.name, _.orbital_semi_major_axis_km) \
    >> arrange(-_.orbital_semi_major_axis_km) \
    >> head() \
    >> affiche()
```
```
╔═══════╦═════════════╦════════════════════════════╗
║ index ║ name        ║ orbital_semi_major_axis_km ║
║ int64 ║ obj         ║ float64                    ║
╠═══════╬═════════════╬════════════════════════════╣
║ 418   ║ S/2021 N 1  ║ 50623600.0                 ║
║ 415   ║ Neso        ║ 48387000.0                 ║
║ 412   ║ Psamathe    ║ 46695000.0                 ║
║ 323   ║ S/2020 S 44 ║ 28043800.0                 ║
║ 278   ║ S/2019 S 43 ║ 27185300.0                 ║
╚═══════╩═════════════╩════════════════════════════╝
```

</details> 

#### 20. `relocate()`

<details>
<summary>View examples</summary>

Like `mutate()`, we have optional `after` and `before` arguments:

```python
moons >> relocate(_.notes, _.refs, after = "name") \
    >> select(_.name | _.refs) \
    >> head() \
    >> affiche()
```

```
╔═══════╦════════╦═══════════════════════════════╦══════════════════╗
║ index ║ name   ║ notes                         ║ refs             ║
║ int64 ║ obj    ║ obj                           ║ obj              ║
╠═══════╬════════╬═══════════════════════════════╬══════════════════╣
║ 0     ║ Moon   ║ Synchronous Rotation (Binary) ║ [12]             ║
║ 1     ║ Phobos ║ Synchronous Rotation          ║ [13][14][15][16] ║
║ 2     ║ Deimos ║ Synchronous Rotation          ║ [13][14][15][17] ║
║ 3     ║ Io     ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
║ 4     ║ Europa ║ Main-Group Moon (Galilean)    ║ [15][18][19]     ║
╚═══════╩════════╩═══════════════════════════════╩══════════════════╝
```

</details> 

#### 21. `rename()`

<details>
<summary>View examples</summary>

Like siuba, `rename()` expects `new_name = _.old_name`

```python
moons >> rename(apparent_magnitude = _.apparent_magnitudea) \
    >> select(_.name, _.apparent_magnitude) \
    >> head() \
    >> affiche()
```
```
╔═══════╦════════╦════════════════════╗
║ index ║ name   ║ apparent_magnitude ║
║ int64 ║ obj    ║ obj                ║
╠═══════╬════════╬════════════════════╣
║ 0     ║ Moon   ║ -12.9 To -2.5      ║
║ 1     ║ Phobos ║ 11.8               ║
║ 2     ║ Deimos ║ 12.89              ║
║ 3     ║ Io     ║ 5.02               ║
║ 4     ║ Europa ║ 5.29               ║
╚═══════╩════════╩════════════════════╝
```

</details> 

#### 22. `round()`

<details>
<summary>View examples</summary>

By default, `round()` reduces all numeric columns to two decimal places — where both can be specified:

```python
cols = ["average_orbital_speed_kms", "sidereal_period_d_r__retrograde"]

moons >> mutate(across(cols, lambda x: pd.to_numeric(x, errors = "coerce"))) \
    >> select(_.name, *cols) \
    >> head() \
    >> round(decimals = 0) \
    >> affiche()
```
```
╔═══════╦════════╦═══════════════════════════╦═════════════════════════════════╗
║ index ║ name   ║ average_orbital_speed_kms ║ sidereal_period_d_r__retrograde ║
║ int64 ║ obj    ║ float64                   ║ float64                         ║
╠═══════╬════════╬═══════════════════════════╬═════════════════════════════════╣
║ 0     ║ Moon   ║ 1.0                       ║ 27.0                            ║
║ 1     ║ Phobos ║ 2.0                       ║ 0.0                             ║
║ 2     ║ Deimos ║ 1.0                       ║ 1.0                             ║
║ 3     ║ Io     ║ 17.0                      ║ 2.0                             ║
║ 4     ║ Europa ║ 14.0                      ║ 4.0                             ║
╚═══════╩════════╩═══════════════════════════╩═════════════════════════════════╝
```

</details> 

#### 23. `drop_na()`

<details>
<summary>View examples</summary>

By default, `drop_na()` drops rows where any column's values are `NA`:

```python
moons.count_na().affiche()
```
```
╔═══════╦═════════════════════════════════╦══════════╦════════════╗
║ index ║ col                             ║ na_count ║ na_percent ║
║ i64   ║ obj                             ║ i64      ║ obj        ║
╠═══════╬═════════════════════════════════╬══════════╬════════════╣
║ 0     ║ image                           ║ 431      ║ 100%       ║
║ 1     ║ average_orbital_speed_kms       ║ 408      ║ 95%        ║
║ 2     ║ apparent_magnitudea             ║ 257      ║ 60%        ║
║ 3     ║ orbital_semi_major_axis_km      ║ 6        ║ 1%         ║
║ 4     ║ refs                            ║ 1        ║ <1%        ║
║ 5     ║ notes                           ║ 1        ║ <1%        ║
║ 6     ║ mean_radius_km                  ║ 0        ║ 0%         ║
║ 7     ║ numeral                         ║ 0        ║ 0%         ║
║ 8     ║ parent                          ║ 0        ║ 0%         ║
║ 9     ║ name                            ║ 0        ║ 0%         ║
║ 10    ║ year_announced                  ║ 0        ║ 0%         ║
║ 11    ║ discovery_year                  ║ 0        ║ 0%         ║
║ 12    ║ sidereal_period_d_r__retrograde ║ 0        ║ 0%         ║
║ 13    ║ discovered_by                   ║ 0        ║ 0%         ║
╚═══════╩═════════════════════════════════╩══════════╩════════════╝
```

```python
# Now, we'll exclude the image column and call drop_na()
moons_drop = moons \
    >> select(~_.image) \
    >> drop_na() 

# And we see that all rows with any NAs were dropped
moons_drop.count_na().affiche()
```
```
╔═══════╦═════════════════════════════════╦══════════╦════════════╗
║ index ║ col                             ║ na_count ║ na_percent ║
║ i64   ║ obj                             ║ i64      ║ obj        ║
╠═══════╬═════════════════════════════════╬══════════╬════════════╣
║ 0     ║ name                            ║ 0        ║ 0%         ║
║ 1     ║ parent                          ║ 0        ║ 0%         ║
║ 2     ║ numeral                         ║ 0        ║ 0%         ║
║ 3     ║ average_orbital_speed_kms       ║ 0        ║ 0%         ║
║ 4     ║ mean_radius_km                  ║ 0        ║ 0%         ║
║ 5     ║ orbital_semi_major_axis_km      ║ 0        ║ 0%         ║
║ 6     ║ sidereal_period_d_r__retrograde ║ 0        ║ 0%         ║
║ 7     ║ discovery_year                  ║ 0        ║ 0%         ║
║ 8     ║ year_announced                  ║ 0        ║ 0%         ║
║ 9     ║ discovered_by                   ║ 0        ║ 0%         ║
║ 10    ║ apparent_magnitudea             ║ 0        ║ 0%         ║
║ 11    ║ notes                           ║ 0        ║ 0%         ║
║ 12    ║ refs                            ║ 0        ║ 0%         ║
╚═══════╩═════════════════════════════════╩══════════╩════════════╝
```

However, we can also specify `how = "all"` — where all values in a row must be `NA` to be dropped:

```python
# We'll still exclude the image column, and specify "all"
moons_drop = moons \
    >> select(~_.image) \
    >> drop_na(how = "all") 

# Since no rows are completely `NA`, nothing gets dropped
moons_drop.count_na().affiche()
```
```
╔═══════╦═════════════════════════════════╦══════════╦════════════╗
║ index ║ col                             ║ na_count ║ na_percent ║
║ i64   ║ obj                             ║ i64      ║ obj        ║
╠═══════╬═════════════════════════════════╬══════════╬════════════╣
║ 0     ║ average_orbital_speed_kms       ║ 408      ║ 95%        ║
║ 1     ║ apparent_magnitudea             ║ 257      ║ 60%        ║
║ 2     ║ orbital_semi_major_axis_km      ║ 6        ║ 1%         ║
║ 3     ║ refs                            ║ 1        ║ <1%        ║
║ 4     ║ notes                           ║ 1        ║ <1%        ║
║ 5     ║ mean_radius_km                  ║ 0        ║ 0%         ║
║ 6     ║ numeral                         ║ 0        ║ 0%         ║
║ 7     ║ parent                          ║ 0        ║ 0%         ║
║ 8     ║ name                            ║ 0        ║ 0%         ║
║ 9     ║ year_announced                  ║ 0        ║ 0%         ║
║ 10    ║ discovery_year                  ║ 0        ║ 0%         ║
║ 11    ║ sidereal_period_d_r__retrograde ║ 0        ║ 0%         ║
║ 12    ║ discovered_by                   ║ 0        ║ 0%         ║
╚═══════╩═════════════════════════════════╩══════════╩════════════╝
```

</details> 

## Dependencies

For a detailed list of gaelach's dependencies, consult the dependencies list in `pyproject.toml`.

## Notes

Data on moons in the Solar System was scraped from the [Wikipedia](https://en.wikipedia.org/wiki/List_of_natural_satellites) page on natural satellites.

**Disclaimer**: This project was created with assistance from generative AI tools.