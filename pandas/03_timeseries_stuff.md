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

# Time Utilities in Pandas 

It is worth to mention that pandas has some *amazing* utilities when dealing with timestamps. In this notebook we will demonstrate some of them.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
```

```python
dates = pd.date_range("2015-01-01", "2018-01-01")
values = np.random.normal(0, 1, len(dates)).cumsum()
df = pd.DataFrame({"dates": dates, "values": values}).set_index("dates")
df.iloc[30:60]
```

```python
df.plot(figsize=(16,4));
```

## Easy Aggregations 

If you have a dataframe that has a datetime-index you can use the `.resample()` method to perform a "groupby"-like grouping based on the index.

For example, we can easily calculate the mean per year by running:

```python
df.resample("Y").mean()
```

You can also run the same aggregation per month `M`, week `W` or quarter `Q`. If the index is a datetime stamp that also includes times then you can aggregate per hour. The script below demonstrates this by calulating the mean per hour.

```python
seconds = pd.date_range("2015-01-01 00:00:00", "2015-01-02 00:00:00", freq="s")
values_s = np.random.normal(0, 1, len(seconds)).cumsum()
df_seconds = pd.DataFrame({"time": seconds, "value": values_s}).set_index("time")

df_seconds.resample("H").mean().head(6)
```

See [here] for a more comprehensive list of offsets

[here]: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects


Note that we can also use a general `.transform` method here as well.

```python
(
    df_seconds
    .resample("H")
    .transform(np.mean)
    .head()
)
```

# Assignment

Let's simulate the profit of a hypothetical business for a couple of years:

```python
np.random.seed(42)
dates = pd.date_range("2015-01-01", "2018-01-01")
values = np.random.normal(0, 1, len(dates)).cumsum()
random_growth_df = pd.DataFrame({"dates": dates, "profit": values}).set_index("dates")

(
    random_growth_df
    .resample("5D")
    .mean()
    .head()
)
```

```python
random_growth_df.plot(figsize=(16,4));
```

```python
(
    random_growth_df
    .resample("5D")[["profit"]]
    .transform("sum")
    .loc[lambda d: d["profit"] == d["profit"].max()]
)
```

```python
(
    random_growth_df
    .resample("5D")
    .transform("min")
    .loc[lambda d: d["profit"] > 0]
)
```

Using everything you learned so far, try to answer the following:

- Within which 5-day period did the highest growth of profit take place?
- Which 5-day periods made a profit on every day (ignoring the first day of the period)?

```python
# %load answers/profit_growth.py
random_growth_df.resample('5d').apply(lambda df: pd.Series({
    'net_growth': df['profit'].iat[-1] - df['profit'].iat[0],
    'all_growth': (df['profit'].diff().dropna() > 0).all()
})).sort_values('net_growth', ascending=False)

```

```python
for i in range(5):
    df = (
        random_growth_df
        .shift(i)
        .resample("5d")
        .sum()
        .assign(prev_value=(lambda d: d['profit'].shift(1)))
        .assign(profit_5d=(lambda d: d['profit'] - d['prev_value']))
         )
    
    print(df.iloc[df['profit_5d'].argmax()])
    
```

```python
df = (
    random_growth_df
    .assign(profit_diff=(lambda d: d['profit'].diff()))
    .assign(rolling_mean_d=lambda d: d['profit_diff'].rolling("5D").sum())
    .assign(all_profit=lambda d: d['profit_diff'].rolling("5D").min() > 0)
    .loc[lambda d: d['all_profit']]
)
df.sort_values("rolling_mean_d", ascending=False)
```

Hint: the integer-based indexers/accessors [iloc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html) and [iat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iat.html) may be useful for this exercise.


## Time Based Features 

Any column in pandas that is of dtype `datetime` has a module attached that can be used to perform vectorised datetime operations. This is very similar to the `.str` module attached to string columns. It is a good thing to explore since the alternative is non-vectorised and much slower.

Below is an example of getting the `weekofyear`. Feel free to explore other properties and methods.

```python
dates = pd.date_range("2015-01-01", "2018-01-01")
df = pd.DataFrame({"date": dates})

df.apply(lambda d: d.dt.weekofyear).head(10)
```

# Assignment

Using `random_growth_df` from above, which month shows the highest mean profit?

```python
(
    random_growth_df
    .assign(month=lambda d: d.index.month) 
    .groupby("month")
    .mean()
    .sort_values("profit", ascending=False)
)
```

```python
# %load answers/profit_by_month.py
(
    random_growth_df
    .assign(date_time=lambda df: df.index)
    .assign(month=lambda df: df['date_time'].dt.month)
    .groupby('month')['profit']
    .mean()
)

```

## Rolling and Smoothing

Sometimes you might want to create a rolling average. Pandas also supports this via the `.rolling()` method which can be called both on a dataframe as well as a series object. It can be used to calculate multiple properties too.

```python
dates = pd.date_range("2015-01-01", "2018-01-01")
values = np.random.normal(0, 1, len(dates)).cumsum()
df = pd.DataFrame({"dates": dates, "values": values}).set_index("dates")
```

```python
df.plot(figsize=(16,4));
```

```python
(
    df
    .assign(rolling_mean=lambda d: d['values'].rolling(20).mean())
    .plot(figsize=(16, 4))
)
```

Note that this rolling property can be centered but can also be tasked with taking a rolling value over a week; pandas is able to recognize datetime values in the index on which to base the roller. 

You can see the effect of the centering below, pay attention to the fact that the red line does not lag anymore. The green and the red lines overlap - those are two ways of doing the same thing. 

Note that this method requires information from the future - so we cannot use the red/green lines in forecasting.

```python
(
    df
    .assign(rolling_mean_d=lambda d: d['values'].rolling("30D").mean())
    .assign(rolling_mean_center=lambda d: d['values'].rolling(30, center=True).mean())
    .assign(manual_center=lambda d: d['rolling_mean_d'].shift(-15))
    .plot(figsize=(16,4))
)
```

Also note that you can do more than just "calculating the mean" you can also compute other statistics.

```python
(
    df
    .assign(rolling_var_d=lambda d: d['values'].rolling("30D").var())
    .assign(rolling_var_center=lambda d: d['values'].rolling(30, center=True).var())
    .plot(figsize=(16,4))
)
```

An alternative to calculating the rolling statistics is to smooth the timeseries exponentially with the following formula:

$$\hat{y_t} = \alpha y_t + (1-\alpha) \hat{y}_{t-1}$$

The idea is to recursively smooth the series by averaging the current average with the current value. If the alpha value is high then the smoothing will be low but the average can respond quicker to changes and if it is low it will result in something much more flat.

```python
(
    df
    .assign(smoothed1=lambda d: d['values'].ewm(alpha=0.01).mean())
    .assign(smoothed2=lambda d: d['values'].ewm(alpha=0.1).mean())
    .plot(figsize=(16, 4))
)
```

See more about ewm (exponentially weighted function) on the pandas [docs].

[docs]: https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows


# Fill NA

Note that these smoothing functions can be especially nice when you have missing data.

```python
import random
random.seed(42)
```

```python
df_nan = (
    df
    .head(40)
    .assign(missing=lambda d: [_ if random.random() < 0.6 else np.nan for _ in d['values']])
    .assign(smooth=lambda d: d['values'].ewm(alpha=0.5).mean().fillna(method="ffill"))
    .assign(interpolate_smooth=lambda d: d['missing'].combine_first(d['smooth']))
)
```

```python
plt.figure(figsize=(16, 4))
plt.subplot(131)
plt.scatter(range(len(df_nan)), df_nan['values'])
plt.scatter(range(len(df_nan)), df_nan['missing'], c='red')
plt.title("the red values are missing");

plt.subplot(132)
plt.scatter(range(len(df_nan)), df_nan['values'])
plt.scatter(range(len(df_nan)), df_nan['smooth'], c='red')
plt.title("the red values are interpolated");

plt.subplot(133)
plt.scatter(range(len(df_nan)), df_nan['interpolate_smooth'], c='red')
plt.scatter(range(len(df_nan)), df_nan['values'])
plt.title("the red values are the smoothed interpolated values");
```

## Convolutional Pandas

One interpretation of a rolling window is that you are smoothing the original time series; in other words, we might be 'de-noiseing' the dataset. One advanced setting that is worth mentioning is the window type. By setting the window type to be "gaussian" you can make the smoothing weighted. This way points that are further away have less influence. Another interpretation of this method is that we apply a convolution on the timeseries.

Extra documentation on this topic can be found [here](http://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#rolling-windows) and a demo can be seen below.

Be sure to check the [Wikipedia] page on the topic.

[Wikipedia]: https://en.wikipedia.org/wiki/Window_function#Gaussian_window

```python
(
    df
    .assign(
        rolling_gaussian_mean_d=lambda d: (
            d['values']
            .rolling(30, center=True, win_type="gaussian")
            .mean(std=5)
        )
    )
    .plot(figsize=(16, 4))
);
```

## Expanding NA

A final method worth mentioning is `.expanding()`. In essense this allows you to write functions like `cumsum()` but with more customisation options.

```python
(
    df
    .assign(cumsum=lambda d: d['values'].cumsum())
    .assign(expanding=lambda d: d.expanding()['values'].sum())
    .head(6)
)
```

You can write your own aggregation functions as you wish, to show what to expect in the `apply()` we print the results below.

```python
def print_and_mean(d):
    print(d)
    return np.mean(d)

df.head(4).expanding().apply(print_and_mean, raw=True)
```

```python

```
