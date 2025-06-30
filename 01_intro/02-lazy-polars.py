
## Create a LazyFrame
## Understand the differences between DataFrame and LazyFrame

## - Eager mode: each line of code is run as soon as it appears
## - Lazy mode: helps us to take advantage of the query optimization. Each line
## of code is added to a query plan which is optimized before running

# 1. Load packages -----------------

import polars as pl

# 2. Load data ---------------------

## convert to lazyframe
pl.read_csv('00_data\\titanic.csv').lazy()

## read in lazy mode
pl.scan_csv('00_data\\titanic.csv'). \
    group_by('Survived', 'Pclass'). \
    agg(
        pl.col('PassengerId').count().alias('counts')
    )

## view the query optimizer
pl.scan_csv('00_data\\titanic.csv'). \
    filter(pl.col('Age') > 50). \
    group_by('Survived', 'Pclass'). \
    agg(
        pl.col('PassengerId').count().alias('counts')
    ). \
    explain()

## evaluate the query, and retrieve the results
pl.scan_csv('00_data\\titanic.csv'). \
    filter(pl.col('Age') > 50). \
    group_by('Survived', 'Pclass'). \
    agg(
        pl.col('PassengerId').count().alias('counts')
    ). \
    collect()
