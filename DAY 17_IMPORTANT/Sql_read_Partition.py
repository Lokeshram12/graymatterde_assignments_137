# Databricks notebook source
# [SalesLT].[Customer]
jdbc_url="jdbc:sqlserver://server1709.database.windows.net:1433;database=db_FirstDatabase"
jdbc_properties ={
    "user":"admin1709",
    "password":"",
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

table_name = "saleslt.customer"
df=spark.read.jdbc(url=jdbc_url,table=table_name,properties=jdbc_properties)

# COMMAND ----------

df.display()

# COMMAND ----------

df.rdd.getNumPartitions()

# COMMAND ----------

# increase partitions
df=df.repartition(2)
# df=df.coalesce(2) reduce partitions

# COMMAND ----------

df.rdd.getNumPartitions()


# COMMAND ----------

spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

df.cache()

# COMMAND ----------

df.count()
