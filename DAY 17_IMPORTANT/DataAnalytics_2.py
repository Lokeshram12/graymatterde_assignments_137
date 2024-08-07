# Databricks notebook source
dbutils.fs.ls("/mnt/mount") 

# COMMAND ----------

df_csv=spark.read.option("header",True).option("Inferschema",True).csv("/mnt/mount/transaction_usa_23_07_2024.csv")

# COMMAND ----------

df_csv.display() 

# COMMAND ----------

df_agg=df_csv.groupBy("SalesRepID").max("TransactionAmount")
df_agg = df_agg.withColumnRenamed("max(TransactionAmount)", "TransactionAmount")
df_agg.display()

# COMMAND ----------

df_agg.write.format("delta").save("/mnt/mount/usa_transaction/")

# COMMAND ----------

# MAGIC %md
# MAGIC ###External

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE ext_usa_trans
# MAGIC USING DELTA
# MAGIC OPTIONS  (path 'abfss://inputmount@adlsgmde1709.dfs.core.windows.net/usa_transaction')

# COMMAND ----------

# MAGIC %sql 
# MAGIC select * from ext_usa_trans
# MAGIC select *

# COMMAND ----------

# MAGIC %md
# MAGIC ###Managed 

# COMMAND ----------

df_agg.write.format("delta").saveAsTable("_usa_store_trans")

# COMMAND ----------

# MAGIC %md
# MAGIC ###Widgets

# COMMAND ----------

dbutils.widgets.text("w_text","abc")
dbutils.widgets.dropdown("w_dropdown","app",["abc","app"])
dbutils.widgets.combobox("w_combobox","abb",["abc","app"])
dbutils.widgets.multiselect("w_multiselect","abc",["abc","app","def"])

# COMMAND ----------

df_agg.createOrReplaceTempView("usa_trans_temp")
df_agg.display()

# COMMAND ----------

dbutils.widgets.text("widget_text", "100")
store_var=dbutils.widgets.get("widget_text")
print(store_var)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from usa_trans_temp

# COMMAND ----------

result=spark.sql(f"""select * from usa_trans_temp where SalesRepID='{store_var}'""")
result.display()

# COMMAND ----------

dbutils.widgets.getAll()

# COMMAND ----------

store_multi_var=dbutils.widgets.get("widget_multiselect")
print(store_multi_var)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from usa_trans_temp where SalesRepID in (${widget_multiselect}) --some syntax issue

# COMMAND ----------

result=spark.sql(f"""select * from usa_trans_temp where SalesRepID in ({store_multi_var})""")
result.display()
