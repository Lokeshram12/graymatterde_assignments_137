# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df_customer=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/raw/CustomerInfo.csv")
df_orders=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/raw/orders.csv")
df_products=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/raw/products.csv")
df_sales=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/raw/Sales.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ### In orders table total column is added based on quantity and price
# MAGIC

# COMMAND ----------

df_orders_enriched = df_orders.withColumn("Total", col("Quantity") * col("Price"))

# COMMAND ----------

df_sales_added=df_sales.withColumn("month",month(df_sales["SalesDate"]))
df_orders_enriched_added=df_orders_enriched.withColumn("month",month(df_orders_enriched["OrderDate"]))

# COMMAND ----------

df_sales_added.write.mode("overwrite").parquet("/mnt/mount/silver/sales.parquet")
df_orders_enriched_added.write.mode("overwrite").parquet("/mnt/mount/silver/orders_enriched.parquet") 
df_products.write.mode("overwrite").parquet("/mnt/mount/silver/products.parquet") 
df_customer.write.mode("overwrite").parquet("/mnt/mount/silver/customer.parquet") 
