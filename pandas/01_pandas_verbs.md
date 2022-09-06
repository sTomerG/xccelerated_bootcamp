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
import pandas as pd
import numpy as np

#%matplotlib inline
```

# Data Wrangling

The goal of this notebook is to explain how to write proper pandas code. To get where we want to be, though, we need to explain something about language. 


## Kitchen Metaphor

Suppose that you want to cook a meal and you explain what you do. You'd probably describe the process in a way like below:

```
Take the chicken -> 
   Then season it, with spices -> 
   Then season it, with gravy -> 
   Then put it in the oven, at 210 celsius -> 
   Then serve it, on a plate
```

You wouldn't dare describe this task with this grammar:

```
Serve -> the thing that(
    PutInOven( -> the thing that 
        Season( -> the thing that
            Season( -> the thing that 
                Chicken, with spices),
        with gravy),
    at 210 celsius), 
on a plate)
```

It sounds crazy, but a lot of people write code in this latter style. Seriously, it's crazy.


## Grammar 

<img src="images/language.png" width="240" height="240" align="center"/>

Notice that when we describe our cooking code that each command has different parts:

```
Take the chicken -> 
   Then season it, with spices -> 
   Then season it, with gravy -> 
   Then put it in the oven, at 210 celsius -> 
   Then serve it, on a plate
```

We can abstract this into:

```
Take the chicken
   Then (season)::verb/what, (with spices)::argument/how
   Then (season)::verb/what, (with gravy)::argument/how
   Then (heat)::verb/what, (at 210 celsius)::argument/how
   Then (serve)::verb/what, (on a plate)::argument/how
```

Notice that every step has a *verb* that explains **what** we are doing and we have an *argument* with that verb that explains **how** we are doing it. The combination of these two is what we like to call a `grammar`. The nice thing about being able to use a grammar this way is that it is relatively easy to build a pipeline of steps that together form your analysis.

<img src="images/pipeline.png" width="240" height="240" align="center"/>

Our goal in this document is to show the basic verbs and grammar of pandas. In later notebooks we will focus a bit more on how to combine parts into a nice language.


# The Goal 

Pandas is going to be the goal now, but later pandas will become a mere tool. We will also practice a little bit with "the act of analysis". To do this we'll grab a dataset about chickens.

```python
chickweight = (
    pd.read_csv('data/chickweight.csv')
    .rename(str.lower, axis='columns')
)
```

# Assignment

### What could we do? 

<img src="images/chick.png" width="240" height="240" align="center"/>

Imagine that we are a farm and we have the following dataset available; what would we do with the dataset?

```python
chickweight.head()
```

```python
# solution 

# 1. we might discover which diet is best for our chickens 
# 2. we might estimate how big the chickens get if it lives longer
# 3. we might learn if chickens grow quicker during certain weeks 
```

The main use case we will want to focus on is to figure out which diet is best, but it is good to take a moment to think if there are also other usecases.


## Verbs on a Dataframe 

The goal of this notebook is to show and demonstrate all the "verbs" on a dataframe. If a dataframe is a noun then verbs are actions that can be performed. Typically a dataframe needs to be able to: 

1. select the columns 
2. select the rows 
3. rename the columns 
4. sort the rows 
5. summarise statistics 
6. create new columns 

Whatever analysis that you are doing, about 80% of them can be described with these "verbs". In this notebook we will demonstrate these commands on the chickweight dataframe such that we can later use it to do analysis.


## Guessing Game 

In order to get familiar with all possible commands, try to run the following cells and try to predict what is happening before you run it. The goal of the document is that you understand how to translate a data operation you have in your head into python code.

# Verbs for Filtering 

```python
chickweight.head(4)
```

```python
chickweight.tail(4)
```

```python
(
    chickweight
    .head(5)
    .tail(2)
)
```

```python
(
    chickweight
    .loc[lambda df: df['time'] < 3]
    .head(4)
)
```

```python
( 
    chickweight
    .loc[lambda df: df['time'] < 3]
    .loc[lambda df: df['chick'] == 1]
    .head(4)
)
```



```python jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}

```

<!-- #region pycharm={"name": "#%% md\n"} -->
### Lessons 

You'll notice that whenever we use `<dataframe>.<verb>` that the output of this operation is yet again a dataframe. This means that we can chain commands together to form the `-then->` style of programming. 

Note that we are using a `lambda` function here to describe how we are using the `.loc` command. The `.loc` tells us **what** we are doing (filtering) and the function tells us **how**.

Note that the `.loc` is a tricky and inconsistent thing to remember (apologies for that). The main thing to remember is that `.loc[]` requires **square** brackets.
<!-- #endregion -->

# Verbs for Selection

You can use square brackets to select columns. We've used it before within `.loc` but you can also use it outside of it.

```python
chickweight[['weight', 'time']].head()
```

If you prefer using `.loc` to select columns, you can use the following syntax. You will keep things consistent

```python
(
    chickweight
    .loc[:, ['weight', 'time']]
    .loc[lambda df: df['weight'] < 50]
    .head(3)
)
```

```python
(
    chickweight
    .drop(columns=['chick'])
    .loc[lambda df: df['weight'] < 50]
    .head(3)
)
```

```python
chickweight[['weight']].head()
```

Note that the output of this next command is a little bit different.

```python
chickweight['weight'].head()  # or chickweight.loc[:, 'weight']
```

There is a subtle difference at work here. 

- `chickweight[['weight']].head()` returns a table with one column (`pd.DataFrame`)
- `chickweight['weight'].head()` selects the column from the table (`pd.Series`)

A lot of verbs that work on dataframes will also work on series objects but not all of them. You've actually used series before in `.loc` when using the lambda function.


## Exercise 1:

Select only the part of `chickweight df` where:

- **weight** is above 50 but below 100
- **diet** is either 1 or 2 (*optional*: either 1 or 3)
- only columns `weight` and `diet`

```python
#your code here

(
    chickweight
    .loc[lambda d: (d['weight'] > 50) & (d['weight'] < 100)]
    .loc[lambda d: (d['diet'] == 1) | (d['diet'] == 3)]
    .loc[:, ['weight', 'diet']]
    .reset_index()
)

```

# Verbs for Sorting

Sort is super useful, but keep in mind that the order in which you run the commands matter!

```python
chickweight
```

```python
(
    chickweight
    .sort_values('weight', ascending=False)
    .head(3)
)
```

```python
(
    chickweight
    .head(3)
    .sort_values('chick', ascending=False)
)
```

```python
(
    chickweight
    .sort_values(['chick', 'weight'], ascending=[False, True])
    .head(3)
)
```

# Verbs for Aggregation

Aggregation is the act of splitting up your original dataset to calculate statistics on sub-dataframes.

<img src="images/split-groupby-combine.png" width="440" height="440" align="center"/>

There are a couple of ways to do this in pandas but we need to pay close attention to the data types. 

```python
chickweight.describe()
```

```python
chickweight.mean()
```

```python
(
    chickweight
    .groupby('diet')
    .mean()
)
```

```python
chickweight.groupby('diet')
```

This is another type of object.

A groupby object is esentially a collection of dataframes. The idea is that later we can calculate something per dataframe.

```python
(
    chickweight
    .groupby(['diet', 'time'])
    .agg(number_rows = pd.NamedAgg(column='rownum', aggfunc=len),
         weight_mean = pd.NamedAgg(column='weight', aggfunc='mean')
    )
    .head(4)
)
```

A dataframe in pandas has an index. When you aggegate and get multiple columns as a result pandas will automatically put the grouped columns in the index. Sometimes this is fine, but usually you want to undo this operation by resetting the index. Note that the index of a dataframe typically has different behavior than a column.

Note that an index can also be used to do fancy things (for example with timeseries).

```python
df = chickweight.groupby('chick')['weight']
```

```python

```

```python
(
    chickweight
    .groupby('time')
    .agg(number_rows=pd.NamedAgg(column='rownum', aggfunc=len),
         weight_mean=pd.NamedAgg(column='weight', aggfunc='mean'),
         weight_var=pd.NamedAgg(column='weight', aggfunc='var')
    )
)
```

```python
chickweight.shape
```

## Exercise 2:

Determine the following aggregate information **per diet** (*optional*: per diet and time):

- maximum chick id
- median weight
- std (standard deviation) of weight

- any extras of your choice

**bonus points:** use a custom function

```python
#your code here

(
    chickweight
    .groupby('diet')
    .apply(lambda d: pd.Series({
        "cick_max": d['chick'].max(),
        "median_weight": d['weight'].median(),
        "weight_std": d["weight"].std()
    }))
    
)

(
    chickweight
    .groupby('diet')
    .agg(max_chick_id=('chick', 'max'),
         median_weight=('weight', 'median'),
         std_weight=('weight', 'std')
    )
)

```

# Verbs for New Columns

We can tell pandas to make a new column (or overwrite an old one) with `.assign` and **how** this is done is determined by the lambda going in.

```python
(
    chickweight
    .assign(weight2=lambda d: d['weight'] * 2)
    .head()
)
```

```python
(
    chickweight
    .assign(weight=lambda df: df['weight'] * 2)
    .head()
)
```

We can do something really fancy too. The `df` variable inside of our `lambda` function refers to the previous dataframe so any verb that works on a dataframe can be used there. This means that we can do `groupby` type things in there.

```python
(
    chickweight
    .assign(rank=lambda df: df.groupby('chick').cumcount() + 1)
    .loc[lambda d: d["chick"] == 2]
)
```

```python
(
    chickweight
    .assign(rank=lambda df: df.groupby('chick').cumcount() + 1)
    .loc[lambda df: df['rank'] < 5]
    .loc[:, ['time', 'chick', 'rank']]
    .head(11)
)

```

# Other Verbs

The main verbs thusfar you'll use on a hourly basis but there are other, lesser known verbs, that are also useful to have seen.

```python
(
    chickweight
    .rename(str.upper, axis="columns")
    .head(3)
)
```

```python
(
    chickweight
    .rename({"chick": "chicken_id"}, axis="columns")
    .head(3)
)
```

```python
(
    chickweight
    .assign(previous_weight=lambda df: df['weight'].shift())
    .head(15)
)  # check what happens when we go from chick 1 to chick 2!!
```

The following solves the problem noted above:

```python
(
    chickweight
    .assign(previous_weight=lambda df: df.groupby('chick')['weight'].shift())
    .head(14)
)
```

```python
(
    chickweight
    .assign(previous_weight=lambda df: df['weight'].shift())
    .dropna()
    .head()
)
```

```python
res
```

```python
(
    chickweight
    [['chick', 'diet']]
    .drop_duplicates()
    .reset_index(drop=True)
)
```

```python
chickweight.sample(3)
```

# Combined Assignment

<img src="images/assignment.png" width="240" height="240" align="center"/>



## 1. Find the dead chickens

There are some chickens that died prematurely. Find them! 

*Hint*: use `describe` to find some clues - how long do these chickens normally live?

Can you also find which diet they were on?

```python
chickweight.describe()
```

```python
(
    chickweight
    .assign(died=lambda df: df.groupby('chick')['time'].transform("count") < 12)
    .loc[lambda d: d['died'] == True]
    ['chick']
    .unique()
)
```

```python
(
    chickweight
    .groupby('chick')
    .agg(count=("time", "count"))
    .loc[lambda d: d['count'] != d['count'].max()]
    
)
```

```python
(
    chickweight
    .assign(week=lambda df: df.groupby('chick').cumcount()+1)
    .loc[lambda df: df['week'] == 12]
    ['chick']
    .unique()
)
```

```python
np.where(chickweight.groupby('chick').size() < 12, 0, 1)
```

```python
(
    chickweight
    .assign(previous_weight=lambda df: df.groupby('chick')['weight'].shift())
    # .loc[lambda df: df['weight'] == df['previous_weight']]
)
```

```python
# %load answers/dead_chickens.py
(
    chickweight
    .groupby('chick')
    [['time']]
    .max()
    .loc[lambda df: df['time'] < chickweight['time'].max()]
)

```

## 2. Find the fattest chicken per diet

*Hint*: use `groupby`

```python
(
    chickweight.groupby('diet')
    .where(lambda x: x.loc[x['weight'] == x['weight'].max()])
)
```

```python
(
    chickweight.groupby('diet')
    .apply(lambda x: x['weight'].max())
    
)
```

```python

```

```python
# %load answers/fattest_chicken.py
(
    chickweight
    .groupby('diet')
    .apply(lambda x: x.loc[x['weight'] == x['weight'].max()])
)

```

```python

```
