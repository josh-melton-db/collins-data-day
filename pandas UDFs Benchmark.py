# Databricks notebook source
from pyspark.sql.types import *
from pyspark.sql.functions import col, count, rand, collect_list, explode, struct, count, lit
from pyspark.sql.functions import pandas_udf, PandasUDFType

# COMMAND ----------

df = spark.range(0, 10 * 1000 * 1000).withColumn('id', (col('id') / 10000).cast('integer')).withColumn('v', rand())
df.cache()
df.count()

df.show()

# COMMAND ----------

@udf('double')
def plus_one(v):
    return v + 1

%timeit df.withColumn('v', plus_one(df.v)).agg(count(col('v'))).show()

# COMMAND ----------

import pandas as pd

@pandas_udf("double")
def pandas_plus_one(v: pd.Series) -> pd.Series:
    return v + 1

%timeit df.withColumn('v', pandas_plus_one(df.v)).agg(count(col('v'))).show()

# COMMAND ----------

from scipy import stats

@udf('double')
def cdf(v):
    return float(stats.norm.cdf(v))

%timeit df.withColumn('cumulative_probability', cdf(df.v)).agg(count(col('cumulative_probability'))).show()

# COMMAND ----------

@pandas_udf('double')
def pandas_cdf(v: pd.Series) -> pd.Series:
    return pd.Series(stats.norm.cdf(v))

%timeit df.withColumn('cumulative_probability', pandas_cdf(df.v)).agg(count(col('cumulative_probability'))).show()

# COMMAND ----------

from pyspark.sql import Row
@udf(ArrayType(df.schema))
def substract_mean(rows):
    vs = pd.Series([r.v for r in rows])
    vs = vs - vs.mean()
    return [Row(id=rows[i]['id'], v=float(vs[i])) for i in range(len(rows))]
  
%timeit df.groupby('id').agg(collect_list(struct(df['id'], df['v'])).alias('rows')).withColumn('new_rows', substract_mean(col('rows'))).withColumn('new_row', explode(col('new_rows'))).withColumn('id', col('new_row.id')).withColumn('v', col('new_row.v')).agg(count(col('v'))).show()

# COMMAND ----------

# Input/output are both a pandas.DataFrame
def subtract_mean(pdf: pd.DataFrame) -> pd.DataFrame:
	return pdf.assign(v=pdf.v - pdf.v.mean())
%timeit df.groupby('id').applyInPandas(subtract_mean, schema=df.schema).agg(count(col('v'))).show()

# COMMAND ----------

df2 = df.withColumn('y', rand()).withColumn('x1', rand()).withColumn('x2', rand()).select('id', 'y', 'x1', 'x2')
df2.show()                                                               

# COMMAND ----------

import statsmodels.api as sm
# df has four columns: id, y, x1, x2
group_column = 'id'
y_column = 'y'
x_columns = ['x1', 'x2']
schema = df2.select(group_column, *x_columns).schema
# Input/output are both a pandas.DataFrame
def ols(pdf: pd.DataFrame) -> pd.DataFrame:
    group_key = pdf[group_column].iloc[0]
    y = pdf[y_column]
    X = pdf[x_columns]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return pd.DataFrame([[group_key] + [model.params[i] for i in   x_columns]], columns=[group_column] + x_columns)
beta = df2.groupby(group_column).applyInPandas(ols, schema=schema)
beta.show()
