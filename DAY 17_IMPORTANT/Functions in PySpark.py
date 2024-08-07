# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *



# COMMAND ----------

def squared(val):
    return val ** 2

# COMMAND ----------

# MAGIC %md
# MAGIC ###Using utility notebook
# MAGIC
# MAGIC

# COMMAND ----------

# for running and executing,accessing values
%run /Workspace/Users/dondapatiram12@gmail.com/GMDE_Utilities/UtilityNotebook
# for scheduling workflow
# dbutils.notebook.run("path_name","time_to_run")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Functions and how to register
# MAGIC

# COMMAND ----------

# udf registration for pyspark
covert_square_id_udf=udf(squared,IntegerType())
#  udf registration for pyspark sql
spark.udf.register("squared_sql",squared,IntegerType())


# COMMAND ----------

df_csv=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/transaction_usa_23_07_2024.csv")
df_agg=df_csv.groupBy("SalesRepID").max("TransactionAmount")
df_agg = df_agg.withColumnRenamed("max(TransactionAmount)", "TransactionAmount")
df_agg.createOrReplaceTempView("usa_trans_temp")
df_agg.display()

# COMMAND ----------

df_squared=df_agg.withColumn("SquaredCol",covert_square_id_udf(col("SalesRepID")))
df_squared.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select squared_sql(SalesRepID) AS SalesRepID_Squared,*
# MAGIC FROM usa_trans_temp
# MAGIC

# COMMAND ----------

df_mul=df_agg.withColumn("MulCol",covert_mul_udf(col("SalesRepID")))
df_mul.display()

# COMMAND ----------

df_floor=df_agg.withColumn("floorCol",covert_floorValue_udf(col("TransactionAmount")))
df_floor.display()

# COMMAND ----------

df_ceil=df_agg.withColumn("ceilCol",covert_ceilValue_udf(col("TransactionAmount")))
df_ceil.display()

# COMMAND ----------


