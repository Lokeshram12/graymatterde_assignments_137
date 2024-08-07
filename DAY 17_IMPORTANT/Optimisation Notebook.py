# Databricks notebook source
# MAGIC %md
# MAGIC ###USE THIS FOR SYNTAX PURPOSE BUT DO NOT EXECUTE

# COMMAND ----------

# MAGIC %md
# MAGIC ###utility notebook

# COMMAND ----------

#how to use utility notebook and execute in any other notebook 
%run <fileURL>

# COMMAND ----------

# MAGIC %md
# MAGIC ####WIDGETS

# COMMAND ----------

# CAN USE UI BUTTONS OR USE CODE
dbutils.widgets.text("w_text","abc")
dbutils.widgets.text("widget_text", "100")
store_var=dbutils.widgets.get("widget_text")
result=spark.sql(f"""select * from usa_trans_temp where SalesRepID='{store_var}'""")
result.display()
print(store_var)

# COMMAND ----------

# MAGIC %md
# MAGIC ###PARTITION

# COMMAND ----------

jdbc_url="jdbc:sqlserver://server1709.database.windows.net:1433;database=db_FirstDatabase"
jdbc_properties ={
    "user":"admin1709",
    "password":"",
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

table_name = "saleslt.customer"
df=spark.read.jdbc(url=jdbc_url,table=table_name,properties=jdbc_properties)

df.rdd.getNumPartitions()
# increase partitions
df=df.repartition(2)
# df=df.coalesce(2) reduce partitions

spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

# MAGIC %md
# MAGIC ###CACHE AND PERSIST

# COMMAND ----------

df.cache()

from pyspark.storagelevel import StorageLevel
df.persist(StorageLevel.DISK_ONLY)

# COMMAND ----------


