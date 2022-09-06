# Pandas
You all know and love(?) Pandas, but there's probably some things you don't know about it yet.
In this session we'll discuss some of those things, as well as how to structure your pandas projects.

There are recordings as well as notebooks available. The recordings go over the material in the notebooks, but
they also add information here and there. There are small exercises spread throughout the notebooks, as 
well as a larger exercise at the end.

# Exercise: World of Churn

If you go to [this](https://www.kaggle.com/mylesoneill/warcraft-avatar-history) link you'll find a kaggle dataset about world of warcraft. The assignment is to download this kaggle dataset to do some churn analysis. 

Alternatively, you can download the dataset from: https://xcc-training-sample-data.s3-eu-west-1.amazonaws.com/world-of-churn/world-of-churn.zip

The primary goal is to learn how to write proper pandas functions such that the students appreciate the structured approach. In particular though, the students need to:

- add a "session" indicator to the dataset indicating consecutive logs in a play session
- how much play time does it take to get to the max level (assume level 60)?
- What is the current churn rate
- does reaching the max level have any influence on churn?
- are there other factors indicative of churn behaviour?
- extra: is there anything else thats interesting in the dataset?
