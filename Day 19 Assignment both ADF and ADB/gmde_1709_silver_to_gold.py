# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
df_sales= spark.read.parquet("/mnt/mount/silver/sales.parquet")
df_orders_enriched=spark.read.parquet("/mnt/mount/silver/orders_enriched.parquet") 
df_products=spark.read.parquet("/mnt/mount/silver/products.parquet") 
df_customer=spark.read.parquet("/mnt/mount/silver/customer.parquet") 



# COMMAND ----------

# MAGIC %md
# MAGIC Total Sales by Product and Customer:
# MAGIC Calculate the total sales amount by product and customer.
# MAGIC Include only sales where the quantity is greater than 1.
# MAGIC

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

sales_with_product = df_sales.join(df_products, on="ProductID", how="inner")
filtered_sales = sales_with_product.filter(col("Quantity") > 1)

# Join filtered sales with df_customer to get customer names
sales_with_customer = filtered_sales.join(df_customer, on="CustomerID", how="inner")

total_sales = sales_with_customer.groupBy("ProductName", "CustomerName").agg(
    spark_sum("TotalAmount").alias("TotalSalesAmount")
)

total_sales.display()

#total sales for each product need to be added


# COMMAND ----------


total_sales.write.mode("overwrite").format("delta").save("/mnt/mount/gold/total_sales/")
total_sales.write.mode("overwrite").format("delta").saveAsTable("total_sales")

# COMMAND ----------

# MAGIC %md
# MAGIC Customer Purchase History:
# MAGIC  Generate a summary of purchases for each
# MAGIC customer.
# MAGIC  Include details such as the total amount spent,
# MAGIC number of orders, and average order value.
# MAGIC

# COMMAND ----------


sales_summary = df_sales.groupBy("CustomerID").agg(
    F.sum("TotalAmount").alias("TotalAmountSpent"),
    F.count("SalesID").alias("NumberOfSales"),
    F.avg("TotalAmount").alias("AverageSaleValue")
)

orders_summary = df_orders_enriched.groupBy("CustomerID").agg(
    F.sum("Total").alias("TotalAmountSpent"),
    F.count("OrderID").alias("NumberOfOrders"),
    F.avg("Total").alias("AverageOrderValue")
)

# Combine the summaries
combined_summary = sales_summary.alias("s").join(
    orders_summary.alias("o"),
    on="CustomerID",
    how="outer"
).select(
    F.coalesce(F.col("s.CustomerID"), F.col("o.CustomerID")).alias("CustomerID"),
    (F.coalesce(F.col("s.TotalAmountSpent"), F.lit(0)) + F.coalesce(F.col("o.TotalAmountSpent"), F.lit(0))).alias("TotalAmountSpent"),
    (F.coalesce(F.col("s.NumberOfSales"), F.lit(0)) + F.coalesce(F.col("o.NumberOfOrders"), F.lit(0))).alias("NumberOfTransactions"),
    (F.coalesce(F.col("s.AverageSaleValue"), F.lit(0)) + F.coalesce(F.col("o.AverageOrderValue"), F.lit(0))).alias("AverageTransactionValue")
)

combined_summary.show()


# COMMAND ----------

combined_summary.write.mode("overwrite").format("delta").save("/mnt/mount/gold/combined_summary/")
combined_summary.write.mode("overwrite").format("delta").saveAsTable("combined_summary")

# COMMAND ----------

# MAGIC %md
# MAGIC Top Products by Sales:
# MAGIC  Identify the top 5 products with the highest total
# MAGIC sales.
# MAGIC  Include details such as total quantity sold and
# MAGIC total sales amount.

# COMMAND ----------

# Aggregate sales data by product
product_sales_summary = df_sales.groupBy("ProductID").agg(F.sum("Quantity").alias("TotalQuantitySold"),F.sum("TotalAmount").alias("TotalSalesAmount")
)

#Join 
product_details = df_products.select("ProductID", "ProductName", "Category")
top_products = product_sales_summary.join(product_details,on="ProductID",how="inner"
).orderBy(F.col("TotalSalesAmount").desc())

top_5_products = top_products.limit(5)

top_5_products.show()


# COMMAND ----------

top_5_products.write.mode("overwrite").format("delta").save("/mnt/mount/gold/top_5_products/")
top_5_products.write.mode("overwrite").format("delta").saveAsTable("top_5_products")

# COMMAND ----------

# MAGIC %md
# MAGIC Monthly Sales Trend:
# MAGIC  Create a monthly trend of total sales.
# MAGIC  Include the total sales amount and number of
# MAGIC orders for each month.
# MAGIC

# COMMAND ----------

# Aggregate sales data by month
monthly_sales_data = df_sales.withColumn("YearMonth", F.date_format("SalesDate", "yyyy-MM")
).groupBy("YearMonth").agg(
    F.sum("TotalAmount").alias("TotalSalesAmount"),
    F.count("SalesID").alias("NumberOfOrders")
)

# Aggregate orders data by month
monthly_orders_data = df_orders_enriched.withColumn(
    "YearMonth", F.date_format("OrderDate", "yyyy-MM")
).groupBy("YearMonth").agg(
    F.sum("Total").alias("TotalSalesAmount"),
    F.count("OrderID").alias("NumberOfOrders")
)

# Combine results from both sources
combined_monthly_trend = monthly_sales_data.alias("s").join(
    monthly_orders_data.alias("o"),
    on="YearMonth",
    how="inner"
).select(
    F.coalesce(F.col("s.YearMonth"), F.col("o.YearMonth")).alias("YearMonth"),
    (F.coalesce(F.col("s.TotalSalesAmount"), F.lit(0)) + F.coalesce(F.col("o.TotalSalesAmount"), F.lit(0))).alias("TotalSalesAmount"),
    (F.coalesce(F.col("s.NumberOfOrders"), F.lit(0)) + F.coalesce(F.col("o.NumberOfOrders"), F.lit(0))).alias("NumberOfOrders")
).orderBy("YearMonth")

combined_monthly_trend.show()


# COMMAND ----------

combined_monthly_trend.write.mode("overwrite").format("delta").save("/mnt/mount/gold/combined_monthly_trend/")
combined_monthly_trend.write.mode("overwrite").format("delta").saveAsTable("combined_monthly_trend")

# COMMAND ----------

# MAGIC %md
# MAGIC
