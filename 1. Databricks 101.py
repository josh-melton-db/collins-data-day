# Databricks notebook source
# MAGIC %md
# MAGIC # Data
# MAGIC To view information about tables, check the Data tab

# COMMAND ----------

# MAGIC %md
# MAGIC # Clusters
# MAGIC For the compute options that are available to you, check the compute tab

# COMMAND ----------

# MAGIC %md
# MAGIC # Notebooks
# MAGIC For more about how to use notebooks within a workspace or a repo, continue on in this notebook!

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reading data

# COMMAND ----------

df = spark.read.table('josh_melton.train_delta')

# COMMAND ----------

display(df)

# COMMAND ----------

df2 = spark.sql('''
select *
from josh_melton.train_delta
''')

df2.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select instant_bookable, count(*)
# MAGIC from josh_melton.train_delta
# MAGIC group by instant_bookable

# COMMAND ----------

# MAGIC %md
# MAGIC Now that we've read in and explored our data, we can apply the desired transformations to our dataset. We can define our business logic using the Spark APIs to leverage the power of Spark's distributed processing engine. For even more powerful processing, use a <a href='https://www.databricks.com/product/photon'>Photon</a> enabled cluster. Photon is Databricks' new vectorized query engine which provides a 3x-8x speedup when compared to open source Apache Spark

# COMMAND ----------

from pyspark.sql.functions import *

# More complex transformations could go here, but for now we'll simply add a new column concatenating the lat/long coordinates
final_df = df2.withColumn('latlong', concat(col('latitude'), lit(', '), col('longitude')))

# COMMAND ----------

final_df.write.mode('overwrite').saveAsTable('josh_melton.databricks_101')

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from josh_melton.databricks_101

# COMMAND ----------

# MAGIC %md
# MAGIC # Orchestration
# MAGIC To schedule this notebook to run automatically, we can use the __Workflows__ tab or the schedule button in the top right

# COMMAND ----------

# MAGIC %md
# MAGIC # Git
# MAGIC To sync this notebook this notebook with a <a href='https://github.com/databricks-academy/data-engineering-with-databricks.git'>git client</a>, we can use the __Repos__ tab </br>

# COMMAND ----------


