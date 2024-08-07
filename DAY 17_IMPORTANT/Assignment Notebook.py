# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql import functions as F

# COMMAND ----------

jdbc_url="jdbc:sqlserver://server1709.database.windows.net:1433;database=db_FirstDatabase"
jdbc_properties ={
    "user":"admin1709",
    "password":"",
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

table_name = "saleslt.customer"
table_name2 = "saleslt.SalesOrderDetail"
table_name3 = "saleslt.SalesOrderHeader"

dfCustomer=spark.read.jdbc(url=jdbc_url,table=table_name,properties=jdbc_properties)
dfSalesOrderDetail=spark.read.jdbc(url=jdbc_url,table=table_name2,properties=jdbc_properties)
dfSalesOrderHeader=spark.read.jdbc(url=jdbc_url,table=table_name3,properties=jdbc_properties)

# COMMAND ----------

dfSales=dfSalesOrderDetail.join(dfSalesOrderHeader,on='SalesOrderID')

# COMMAND ----------


startDate = dbutils.widgets.get("startDate")
endDate = dbutils.widgets.get("endDate")

dfSales_filtered = dfSales.filter(
    (col('OrderDate') >= to_date(lit(startDate), 'yyyy-MM-dd')) &
    (col('OrderDate') <= to_date(lit(endDate), 'yyyy-MM-dd'))
)

# COMMAND ----------

dfSales_filtered.display()

# COMMAND ----------

# Dropped specified columns from dfSales_filtered
# dfSales_filtered_cleaned = dfSales_filtered.drop('CreditCardApprovalCode', 'Comment')
# dfSales_filtered_cleaned = dfSales_filtered.dropna()
dfSales_filtered_cleaned.display()


# COMMAND ----------

dfSales_filtered_enriched= dfSales_filtered_cleaned.withColumn(
    'TotalSales',
    col('OrderQty') * col('UnitPrice')
)


# COMMAND ----------

dfSales_filtered_enriched.display()

# COMMAND ----------

aggregated_df = dfSales_filtered_enriched.groupBy('CustomerID').agg(
    F.count('SalesOrderID').alias('NumberOfOrders'),  
    F.sum('TotalSales').alias('TotalSales')     
)

# COMMAND ----------

aggregated_df.display()

# COMMAND ----------

totalSales_Customer2=aggregated_df.join(dfCustomer,on='CustomerID')

# COMMAND ----------

totalSales_Customer2.display()

# COMMAND ----------

totalSales_Customer = totalSales_Customer2.withColumn(
    'FullName',
    concat(
        coalesce(col('Title'), lit('')),       
        lit(' '),                              
        coalesce(col('FirstName'), lit('')),   
        lit(', '),                             
        coalesce(col('MiddleName'), lit('')),  
        lit(', '),                             
        coalesce(col('LastName'), lit(''))     
    )
)

# COMMAND ----------

totalSales_Customer.display()

# COMMAND ----------

totalSales_Customer = totalSales_Customer.drop('Title', 'Firstname','MiddleName','LastName')
totalSales_Customer.display()

# COMMAND ----------

totalSales_Customer.write.format("delta").saveAsTable("final_sales_per_customer")

# COMMAND ----------

# MAGIC %sql
# MAGIC select  * from final_sales_per_customer
# MAGIC order by TotalSales desc
# MAGIC limit 5

# COMMAND ----------

totalSales_Customer.write.format("delta").save("/mnt/mount/final_transaction_02/")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE final_transaction_02
# MAGIC USING DELTA
# MAGIC OPTIONS  (path 'abfss://inputmount@adlsgmde1709.dfs.core.windows.net/final_transaction_02')

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE final_transaction_02 
# MAGIC ZORDER BY (CustomerID)

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history final_transaction_02 
