---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Pandas exercises 

This notebook contains short pandas exercises. 

The goal is to familiarize yourself with some parts of the pandas library that are uncommon, but rather useful. For a lot of these exercises it is common to check the pandas documentation. Try not to use stackoverflow; force yourself towards the pandas documentation instead. 

```python
import pandas as pd
import numpy as np
```

## Filter with a Lag

You have a DataFrame df with a column 'A' containing integers. For example:
```
df = pd.DataFrame({'A': [1, 2, 2, 3, 4, 5, 5, 5, 6, 7, 7]})
```

Filter out all rows that thave the same value as the row immediately above. Hint: google what `shift()` might do in pandas. 

```python
%load answers/filter_above.py
```

## Aggregate Towards Indices

You have the following dataframe: 
```
df = pd.DataFrame(np.random.random(size=(5, 10)), columns=list('abcdefghij'))
```

- Which column of numbers has the smallest sum? 
- Which row of the dataframe has the smallest sum? 

```python
%load answers/smallest_sum.py
```

## Premade Groups

Consider a dataframe with two columns, A and B. 

```
df = pd.DataFrame(np.random.randint(0, 101, size=(10000, 2)), columns=['A', 'B']) 
```

The values in 'A' are between 1 and 100. For each group of 10 consecutive integers in 'A' (i.e. (0, 10], (10, 20], ...), calculate the sum of the corresponding values in column 'B'.

Hint: you may want to google how pandas can `cut` slices out of a column.

```python
%load answers/group_sum.py
```

## Searching for NaN

You have a dataframe containing many NaNs in each row. Find the 7th occurence of a NaN per row.

```
df = (
    pd.DataFrame(np.random.randint(0, 101, size=(10000, 100)))
    .mask(np.random.randint(0, 10, size=(10000, 100)) == 1, other=nan)
)
```

- Hint; if you don't know what `.mask()` does on a dataframe you can learn by typing `?df.mask` in a cell. 
- Hint; you sort of need a `sum` here, but maybe a different kind of `sum`. Try to solve the operations on paper first. 

```python
%load answers/7th_nan.py
```

## Counting Zeros 

Consider a single-column dataframe

```
df = pd.DataFrame({'X': np.random.randint(0, 10, 100)})
```

for each value, count how many steps it is away from the previous 0 or the start of the series.

```python
%load answers/steps_from_zero.py
```

## Imputing Values in Pandas

Per 'group' replace any negative values with the group mean of the positive numbers.

```
df = pd.DataFrame({
    'group': list('aabbabbbabab'),
    'value': [1, -2, 3, -3, 2, 3, -8, 1, 7, 3, -1, 8]})
```

Hint; you *may* want to google `.transform()` and how it is different than `.apply()`. 

```python
%load answers/group_mean.py
```

## Rolling Mean

Implement a rolling mean over 'group' with window size 3, which ignores negative values. E.g. the mean of [1, -2, 2] is 1.5. 

Note: pass min_periods=1 to the method rolling which reduces the minimum required number of valid observations in the window to 1.

```
df = pd.DataFrame({
    'group': list('aabbabbbabab'),
    'value': [1, -2, 3, -3, 2, 3, -8, 1, 7, 3, -1, 8]})
```

```python
%load answers/rolling_mean.py
```

## Some Times

Here we are going to play around with a datetime index. 

First, create a DatetimeIndex that contains each business day of 2018 and use it as an index for a series of random numbers.

```python
%load answers/datetime_index.py
```

Next, find the average value for each monday. Note that you do note need a `.groupby` for this.

```python
%load answers/avg_monday.py
```

Next find the date on which the highest value can be found for each quarter. Note that you might want to use groupby as well as a utility tool that can create groups. 

Hint; have a look around the pandas documentation for things that can group a datetimeindex. 

```python
%load answers/max_quarter.py
```

Next, create a summary per month. We want to see the `max(value)` together with the corresponding date as well as the `mean(value)` per month. Ensure that everything is in a single pandas dataframe. 

Hint; you may want to construct a `pd.Series` object while you are aggregating and it might help to first convert the series object into a dataframe.

```python
%load answers/aggregate_tsindex.py
```

Finally, let's create a chart of the cumsum of our timeseries. To make the serie is pretty you may want to subtract a constant from the value column such that we have a metric that can also go down in value.

While plotting, also plot a moving average and an exponential smoothing average of the cumsum value. Try to play around with the parameters. 

Hint; the smoothing features of pandas do not need a datetime/index reference. Everything is based on the order in which things appear in the dataframe.

```python
%load answers/ts_plots.py
```
