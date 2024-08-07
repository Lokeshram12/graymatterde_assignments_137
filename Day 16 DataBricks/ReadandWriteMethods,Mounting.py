# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

sche = StructType().add("ID",IntegerType(),True)\
            .add("Name",StringType(),True)\
            .add("Age",IntegerType(),True)

# COMMAND ----------

df_02 = spark.read.option("header",True).schema(sche).csv("/FileStore/details.csv")
df_02.display()

# COMMAND ----------

df_03 = spark.read.option("header",True).option("mode","failfast").csv("/FileStore/details.csv")
df_03.display()

# COMMAND ----------

df_04 = spark.read.option("header",True).option("mode","dropmalformed").csv("/FileStore/details.csv")
df_04.display()

# COMMAND ----------

dbutils.fs.ls("/mnt/mount")

# COMMAND ----------

dbutils.fs.mount(source = "wasbs://inputmount@adlsgmde1709.blob.core.windows.net",
                 mount_point ="/mnt/mount",
                 extra_configs = {"fs.azure.account.key.adlsgmde1709.blob.core.windows.net":dbutils.secrets.get(scope = "mount", key ="mntInput")})

# COMMAND ----------

df_csv=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/sales_asisa_24_07_2024.csv")

# COMMAND ----------

df_csv.display()

# COMMAND ----------

df_agg=df_csv.groupBy("SaleID").max("SaleAmount")
df_agg = df_agg.withColumnRenamed("max(SaleAmount)", "MaxSaleAmount")
df_agg.display()

# COMMAND ----------

df_agg.write.parquet("mnt/mount/parquet/")

# COMMAND ----------

df_agg.write.mode("overwrite").format("delta").saveAsTable("store_trans")

# COMMAND ----------

dbutils.fs.ls("/mnt/input")

# COMMAND ----------

df_agg.write.format("delta").save("/mnt/mount/store_transaction_02/")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a external data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE ext_store_trans_02
# MAGIC USING DELTA
# MAGIC OPTIONS  (path 'abfss://inputmount@adlsgmde1709.dfs.core.windows.net/store_transaction_02')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ext_store_trans_02

# COMMAND ----------

# MAGIC %sql
# MAGIC delete from ext_store_trans_02 where SaleID=19

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into ext_store_trans_02 values(48,17)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- OPTIMIZE ext_store_trans_02 
# MAGIC OPTIMIZE ext_store_trans_02 
# MAGIC ZORDER BY (SaleID)

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history ext_store_trans_02 

# COMMAND ----------


