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

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
```

# Advanced Chickweight 

- joins/merges/concatenations 
- dealing with missing values
- transformations instead of aggregations 

```python
chickweight = (
    pd.read_csv('data/chickweight.csv')
    .rename(str.lower, axis='columns')
)
```

## Combining Datasets 

<img src="images/join.png" width="240" height="240" align="center"/>


```python
(
    chickweight
    .set_index('diet')
    .head()
)
```

```python
def my_func(x: pd.Series) -> pd.Series:
    return pd.Series(np.mean(x))
    
```

```python
agg = (
    chickweight
    .groupby('diet')
    # .agg(mean_weight=("weight", my_func))
    .apply(lambda df: pd.Series({"mean_weight": np.mean(df['weight'])}))
)

agg
```

```python
agg = (
    chickweight
    .groupby('diet')
    .agg(mean_weight=("weight", "mean"))
)

agg
```

```python
(
    chickweight
    .set_index("diet")
    .join(agg)
    .sample(6)
)
```

```python
(
    chickweight
    .merge(agg.reset_index())
    .sample(6)
)
```

You may notice that there is overlap in the functionality of `.join()` and `.merge()`. The difference is minor;

- **join** will merge based on the indices as base behavior
- **merge** will join based on overlapping column names as base behavior 

You don't have to use these functions implicitly though, you can also use them explicitly to describe what columns should be merged on what other columns.

```python
agg.reset_index()
```

```python
chickweight.head(4)
```

```python
(
    chickweight
    .merge(agg.reset_index(), on="diet")
    .sample(3)
)
```

# Assignment 

Suppose that we have an extra dataframe with some information we'd like to get joined to our original dataframe.

```python
agg = (
    chickweight
    .groupby(['diet', 'time'])
    .apply(lambda df: pd.Series({
      "weight": df['weight'].mean(), 
      "variance": df['weight'].var()}))
    .reset_index()
    .rename(columns={"time": "tijd"})
)

agg.head(3)
```

```python
(
    chickweight
    .merge(agg, left_on=["diet","time"], right_on=["diet", "tijd"], suffixes=("", "_agg"))
)

#chickweight.merge(agg, how="left", left_on=["diet", "time"], right_on=["diet", "tijd"], suffixes=("", "_agg"))
```

Write a statement that will join the two dataframes using the `chickweight.merge()` command. Make sure that you join on both the diet as well as the time (even though the column names do not overlap). To make it a nice join you might want to read the documentation of `pandas.DataFrame.merge()` in order to figure out what the suffix settings might do and what other `on` settings exist.

Note that you should use a **single** `.merge()` command for the join and little else.

## Bonus Points 

Can you also perform the join using `agg.merge()`? 

```python
# %load answers/joined_frames.py
# the base setting 
df1 = chickweight.merge(agg, how="left", left_on=["diet", "time"], right_on=["diet", "tijd"], suffixes=("", "_agg"))

# the other way around
df2 = agg.merge(chickweight, how="right", right_on=["diet", "time"], left_on=["diet", "tijd"], suffixes=("_agg", ""))

# note that in this case it might have been a better idea to instead 
# make sure that the column names are correct *beforehand* 


```

## Computation Time 

<img src="images/alternative.png" width="140" height="140" align="center"/>

In principle the operation we just did is quite common. You want to group by some information (things like say, average session length) and add this information to a raw dataset. To perform the aggregation first makes sense but especially for large dataframes the join operation that follows after can be a bit expensive. There is an alternative.

There's also a `.transform()` method. This method will do the aggregation as well as the join in one go. To demonstrate how this works, let us first check what the mean weight is per diet.

```python
(
    chickweight
    .groupby("diet")
    .mean()
    .loc[:, 'weight']
)
```

```python
(
    chickweight
    .groupby("diet")
    .mean()
    .drop(columns=["rownum", "chick"])
)

# agg.reset_index().merge(chickweight, on="diet", suffixes=("_mean", ""))
```

Next up we will use the `.transform()` method on the grouped object. We will first check the shape.

```python
transformed = (
    chickweight
    .loc[:, ["diet", "weight"]]
    .groupby("diet")
    .transform(np.mean)

)

transformed.shape
```

We note that what comes out has the same shape as what came in. Next we check if the value corresponds with the 1st diet.

```python
transformed.head()
```

It is indeed so.


# Assignment

Take the original `chickweight` dataframe and create these columns on the raw data without performing a join: 

1. **mean_weight_diet**: which calculates the mean weight per diet 
2. **mean_weight_diet_time**: which calculates the mean weight per diet at a given time
3. **num_chickens_diet**: which calculates the total number of chickens per diet

```python
# %load answers/transforms.py
(
    chickweight
    .assign(mean_weight_diet=lambda d: d.groupby("diet")['weight'].transform(np.mean))
    .assign(mean_weight_diet_time=lambda d: d.groupby(["diet", "time"])['weight'].transform(np.mean))
    .assign(num_chickens_diet=lambda d: d.groupby("diet")["chick"].transform(lambda d: d.nunique()))

)
```

# Analysis Assignment 

When do chickens grow the most? Does the growth per time depend on the diet? Is there even a difference?

- **Hint 1**: google the `shift` function on a series and note that it works differently when a `groupby` is active.
- **Hint 2**: there is also an alternative function you can use for this, can you find it in the documentation? 

```python
(
    chickweight
    .assign(prev_weight=lambda d: d.groupby('chick')['weight'].shift())
    .assign(weight_increase=lambda d: d['weight'] - d['prev_weight'])
    .assign(weight_increase2=lambda d: d.groupby("chick")["weight"].diff())
    .fillna(0)
    .groupby('time')
    ['weight_increase']
    .mean()
    .plot(kind="bar")
)
```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

```python
# %load answers/chicken_growth.py
# here we use the plot functionality that comes naturally with pandas 
(
    chickweight
    .assign(previous_weight = lambda x: x.groupby('chick')['weight'].shift(1))
    .assign(weight_increase = lambda x: x['weight']- x['previous_weight'])
    .fillna(0)
    .groupby('time')
    ['weight_increase'].mean()
    .plot(title='Average growth over time')
)

```

```python
# %load answers/analysis.py

pltr = (
    chickweight
    .assign(delta=lambda df: df.groupby('chick')['weight'].transform(lambda df: df.diff()))
    .dropna()
)

agg = (
    pltr
    .groupby(['time', 'diet'])
    .apply(lambda df: pd.Series({'mean_delta': np.mean(df['delta'])})).reset_index()
)


fig, ax = plt.subplots(figsize=(10, 8))

pltr.plot('time', 'delta', kind='scatter', legend=False, ax=ax)

for diet, diet_df in agg.groupby('diet'): 
    diet_df.plot('time', 'mean_delta', label=f'diet {diet}', ax=ax, legend=False)

ax.set_xticks(range(2, 22, 2))
ax.set_xlabel('time')
ax.set_ylabel('weight gain')
ax.set_title('something really strange occurs at timestep 14')
ax.legend(loc='upper left');

```

```python

```
