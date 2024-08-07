# Databricks notebook source
# from pyspark.sql import functions as F
from pyspark.sql.functions import *

# COMMAND ----------

from pyspark.sql import SparkSession
spark = SparkSession \
 .builder \
 .appName("Python Spark SQL basic example") \
 .config("spark.some.config.option", "some-value") \
 .getOrCreate()
 

# COMMAND ----------


data = [("A", 1), ("B", 2), ("C", 3)]
df = spark.createDataFrame(data, ["Name", "Id"])
df.show()
df.createOrReplaceTempView("people")
result = spark.sql("SELECT * FROM people WHERE Id > 1")
result.show()


# COMMAND ----------

# df.head(2)
df.schema

# COMMAND ----------

 df.select("Id",
 F.when(df.Id > 1, 1) 
 .otherwise(0)) \
 .show()


# COMMAND ----------

df.select(df.Id.between(2, 3)).show() 

# COMMAND ----------

# add columns
df_new = df.withColumn("Id_squared", col("Id") * col("Id"))
df_new.show()

# COMMAND ----------

df_new.describe().show() 
df_new.count() 
df_new.distinct().count() 
df_new.printSchema() 
df_new.explain() 

# COMMAND ----------

df_new.filter(df_new["Id_squared"]>4).show() 

# COMMAND ----------

rdd1 = df_new.rdd 
df_new.toJSON().first() 
df_new.toPandas() 

# COMMAND ----------

df_new.select("Name", "id","id_squared") \
 .write \
 .save("customer.json",format="json")
