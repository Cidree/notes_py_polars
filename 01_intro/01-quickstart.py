
# 1. Load packages -----------------

import polars as pl

# 2. Load data ---------------------

titanic_pl = pl.read_csv('00_data\\titanic.csv')

# 3. Quickstart --------------------

## 3.1. Global options ------

pl.Config.set_tbl_rows(6)
pl.Config.set_fmt_str_lengths(100)

## 3.2. Explore data --------

titanic_pl.head(5)
titanic_pl.describe()
titanic_pl.glimpse()

## 3.3. Select cols ---------

## select one by one
titanic_pl. \
    select(
        pl.col('Pclass'),
        pl.col('Name'),
        pl.col('Age')
    )

## select by data type
titanic_pl. \
    select(pl.col(pl.Int64))

## expressions on selection and rename
titanic_pl. \
    select(
        pl.col('Pclass'),
        pl.col('Name').str.to_lowercase(),
        pl.col('Age').round(2).alias('Edad')
    )

## 3.4. Filters --------------

## filter by one column
titanic_pl. \
    filter(pl.col('Age') > 70)

## 3.5. Aggregations ---------

## frequency counts
titanic_pl['Sex'].value_counts()

## group by and aggregation
titanic_pl. \
    group_by(['Survived', 'Sex']). \
    agg(
        pl.col('PassengerId').count().alias('Number of passengers'),
        pl.col('Age').mean().round(1).alias('Mean age')
    )

# 4. Visualization ----------------------------

## scatter plot
titanic_pl. \
    plot.scatter(
        x = 'Age',
        y = 'Fare'
    )

# 5. Lazy mode --------------------------------

## Lazy mode: polars uses a query graph to optimize the query
## to do so, we have to 'scan' the data instead of read it

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
