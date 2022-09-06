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

# Modern Pipelines

In the previous notebooks we've discussed a lot about what pandas has to offer. It offers a lot of details but it hasn't discussed yet how you may want to use pandas in practice. In this notebook we will demonstrate a problem with certain workflows and we will conclude with a workflow that should be adopted instead. 

## Why it Matters 

A lot of notebooks become these long scripts of scrolling and it might get hard to figure out what you're doing. It also makes it harder for others to pick up. You want to make clean code, this needs to be a base attitude.

## Bad Code Smells

Let's demonstrate some bad pandas code and let's also talk about **why** it is bad. We'll start with some imports and a `DataFrame`.

```python
import numpy as np
import pandas as pd
```

```python
df = pd.DataFrame({"v1": [1,2,3,4,5,6,7,8], "v2": [8,7,6,5,4,3,2,1]})
```

```python
df
```

Suppose now that I want to filter out rows, this bit of code will do that:

```python
df["v2"] <= 3
```

```python
df[(df["v1"] % 2) == 0][df["v2"] <= 3]
```

The output is fine, but we do get a warning. You can choose to ignore the warning, but something that is potentially very dangerous is happening here:
If you think about it though, this operation is quite scary: we're subsetting an array using a different length
index than the original length of the array.

This is because Pandas by default uses the `index` to align recoreds before operating on them.

```python
df[(df["v1"] % 2) == 0] \
.reset_index() \
[df["v2"] <= 3]
```

If we reset the index, then suddenly our filtering no longer works. Pandas is trying to help you under the hood to make sure that this error does not happen, but from a mechanical perspective this is a bit crazy. We are trying to merely filter on the **values** of a column. The index should have no influence. 

There're other things that you might be tempted to do that makes this way of "writing pandas" a bit tricky. You may have seen code like this instead:

```python
df = df[(df["v1"] % 2) == 0]
df = df.reset_index()
df = df[df["v2"] <= 3]
df
```

Again, this is suboptimal. For starters, we gain a column `index` that nobody wanted and also (and this is the part that might cause errors) we are overwriting our raw data. Overwriting raw data makes it very hard to reproduce steps and it makes it even more tricky to find bugs. This is especially true when you are writing long notebooks.

Another alternative is that you might consider writing something like this:

```python
df = pd.DataFrame({"v1": [1,2,3,4,5,6,7,8], "v2": [8,7,6,5,4,3,2,1]})
```

```python
df2 = df[(df["v1"] % 2) == 0]
df3 = df2.reset_index()
df4 = df3[df3["v2"] <= 3]
df4
```

But this also leads to junk code. Knowing the difference between `df2` and `df4` is still an effort.

# A Path Forward 

Maybe we should lay down the ground rules for writing pandas. 

1. Operations should never change the original dataset. 
2. We need to be able to seperate concerns in our code so that we don't just want to know **what** code is running but also **when**. 
4. We want to make small changes easily to test the effects of certain parameters in our analysis. 

Let's adress these three points.

## Point 1: Never Change the Original Data

The code we had before can be rewritten as follows:

```python
df = pd.DataFrame({"v1": [1,2,3,4,5,6,7,8], "v2": [8,7,6,5,4,3,2,1]})
```

```python
(
    df
    .loc[lambda d: (d["v1"] % 2 == 0)]
    .loc[lambda d: d["v2"] <= 3]
)
```

You'll notice that the original dataset has not changed. 

```python
df
```

Another benefit of this way of writing code is that you can clearly see from top to bottom from left to right what is happening. 

You might be tempted to think that you are limited by this way of writing code, but you actually get to still do nearly everything. 

- add/overwrite columns `.assign()`
- filter rows `.loc[]`
- make a grouped object `.groupby()`
- shorthand aggregation for groupby `.agg()`
- general aggregation for groupby `.apply()`
- sorting rows `.sort_values()`
- reset the index `.reset_index()`
- select top/bottom rows `.head()/.tail()`

Note that all these methods do not change the original dataset as base behaviour.

An example of a set of chainable commands is listed below.

```python
(df
 .loc[lambda d: (d["v1"] % 2 == 0)]
 .assign(v3=lambda d: d["v1"] * d["v2"])
 .loc[lambda d: d["v3"] >= 10]
 .head(2))
```

## Point 2: Separate Concerns

We can expand this lesson to another level of abstraction. Let's pretend that we've read in a timeseries and that this is the new data.

```python
def make_ts_df():
    dates = [str(_) for _ in pd.date_range("2018-01-01", "2019-01-01")]
    values = [np.nan if np.random.random() < 0.05 else _ for _ in np.random.normal(0, 1, 366)]
    return pd.DataFrame({"date": dates, "value": values})

date_df = make_ts_df()
```

```python
date_df
```

This `date_df` needs parsing before we can do something useful with it. In particular:

- we need to make sure that the types are set 
- we might want to clean the `nan` values
- potentially we also want to remove outliers. 

This gives us to opportunity to learn about `pipe`

```python
def parse_types(dataf):
    return (dataf
            .assign(date=lambda d: pd.to_datetime(d.date)))

def clean_nan(dataf):
    return (dataf.dropna())

def remove_outliers(dataf, min_value=-2.0, max_value=2.0):
    """"""
    logger.info(f"Removing outliers below {min_value} and above {max_value}")
    
    return (dataf
            .loc[lambda d: d.value > min_value]
            .loc[lambda d: d.value < max_value])


def prep_dataframe(date_df):
    return (date_df
           .pipe(parse_types)
           .pipe(clean_nan)
           .pipe(remove_outliers, min_value=-3.0))



```

The `.pipe()` method allows us to pass a function that accepts a dataframe as its first argument. This is a very nice flow. Note:

- We can give the function a descriptive name and on a pipeline level this allows us to see "what" is happening "when". 
- If there is ever a bug this pipeline will make it easier for us to figure out where it is. Since every step is merely a function. 
- We can write unit tests for these small pipeline steps such that we can test for expected behavior. 
- We can automate logging a bit. 

To demonstrate this last point. Let's add a decorator. 

```python
from functools import wraps


def log_pandas_pipefunc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        shape_before = args[0].shape
        shape_after = result.shape
        print(f"{func.__name__} => before shape:{shape_before} after shape:{shape_after}")
        return result
    return wrapper

@log_pandas_pipefunc
def parse_types(dataf):
    return (
        dataf
        .assign(date=lambda d: pd.to_datetime(d.date))
    )

@log_pandas_pipefunc
def clean_nan(dataf):
    return (dataf.dropna())

@log_pandas_pipefunc
def remove_outliers(dataf):
    return (
        dataf
        .loc[lambda d: d.value > -2.0]
        .loc[lambda d: d.value < 2.0]
    )

prep_df = (
    date_df
    .pipe(parse_types)
    .pipe(clean_nan)
    .pipe(remove_outliers)
)
```

Note the benefit of having a standard decorator that can log pandas steps: 

1. When writing code, this might help you in discovering what is happening. If you see rows dissapear while they shouldn't this log might give you a proxy. 
2. When this pandas code goes to production you will have some logging for free in airflow. If something goes wrong there you may also be able to debug more easily.


### Caveats 

We should be careful when we are writing `.pipe`-lines. The function going into a `.pipe()` might not be stateless. Here's an example:

```python
date_df = make_ts_df()
date_df
```

```python
def rename_columns(dataf):
    dataf.columns = ["a", "b"]
    return dataf 

rename_columns(date_df)
```

```python
date_df
```

```python
def rename_columns(dataf):
    dataf.columns = ["a", "b"]
    return dataf 

date_df = make_ts_df()
date_df.pipe(rename_columns).columns, date_df.columns
```

In such a situation it is best to include a `.copy()` command. 

```python
def rename_columns(dataf):
    dataf = dataf.copy()
    dataf.columns = ["a", "b"]
    return dataf 

date_df = make_ts_df()
date_df.pipe(rename_columns).columns, date_df.columns
```

Be careful with this. We want our functions to be stateless or otherwise we lose our benefits.

## Point 3: Abstraction on Higher Levels

To fully appreciate what the pandas pipelines can do let us rewrite one function.

```python
@log_pandas_pipefunc
def remove_outliers(dataf, min_value=-2.0, max_value=2.0):
    return (
        dataf
        .loc[lambda d: (d.value > min_value) & (d.value < max_value)]
    )

prep_df = (
    date_df
    .pipe(parse_types)
    .pipe(clean_nan)
    .pipe(remove_outliers, max_value=0.5)
)
```

The `.pipe()` can accept keyword arguments. This allows you to change, say, threshold values on a high level. No need to change the original function, you can change things from a higher level. This is great because it will encourage you to write functions that are general. 

<!-- #region -->
# Conclusion 

> **"Pipelines are the only correct way to write pandas."** 


Even if you take this statement with a grain of salt, it is important to write your code in such a way that your notebook remains clear. Take this serious. If it takes a lot of effort to understand the code of your colleagues, then your team will be slower than you want it to be. 

A notebook is a great scratchpad, but that is no excuse to write unclear code.
<!-- #endregion -->

```python

```
