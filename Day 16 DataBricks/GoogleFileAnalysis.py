# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df_01 = spark.read.csv("/FileStore/gmde1709/googleplaystore.csv")
df_01.display()
df_01.printSchema() 

# COMMAND ----------

df_02 = spark.read.option("header",True).csv("/FileStore/gmde1709/googleplaystore.csv")

# COMMAND ----------

df_02.display()
df_02.printSchema()

# COMMAND ----------

df_03 = spark.read.option("header",True).option("inferschema",True).csv("/FileStore/gmde1709/googleplaystore.csv")
df_03.printSchema()

# COMMAND ----------

sche = StructType().add("App",StringType(),True)\
            .add("Category",StringType(),True)\
            .add("Rating",DoubleType(),True)\
            .add("Reviews",IntegerType(),True)\
            .add("Size",StringType(),True)\
            .add("Installs",StringType(),True)\
            .add("Type",StringType(),True)\
            .add("Price",StringType(),True)\
            .add("Content Rating",StringType(),True)\
            .add("Genres",StringType(),True)\
            .add("Last Updated",StringType(),True)\
            .add("Current Ver",StringType(),True)\
            .add("Android Ver",StringType(),True)

# COMMAND ----------

df_03 = spark.read.option("header",True).schema(sche).csv("/FileStore/gmde1709/googleplaystore.csv")

# COMMAND ----------

df_04=df_03.withColumn("Rate-Review",col("Reviews")*col("Rating"))
df_04.display() #creates a new Rate-Review product
df_05=df_03.withColumn("Genre-Size",concat(col("Genres"),col("Size")))
df_05.display()
df_06=df_03.withColumn("New App",col("App"))
df_06.display() #creates new column and copies existing data
df_07=df_03.withColumn("owner",lit("ram"))
df_07.display() 

# COMMAND ----------

df_04=df_03.withColumn("Rate-Review",col("Reviews")*col("Rating")).withColumn("Genre-Size",concat(col("Genres"),col("Size"))).withColumn("New App",col("App")).withColumn("owner",lit("ram"))
df_04.display()

# COMMAND ----------

df_05=df_04.withColumnRenamed("Rate-Review","My Review Rating")

# COMMAND ----------

df_05=df_04.select("Rating")
df_05.display()
df_05=df_04.selectExpr('cast(Rating as integer) as new_rating')
df_05.display()

# COMMAND ----------

df_05=df_04.sort(col("Rating").desc())
df_05.display(10)
df_05=df_04.orderBy(col("Rating").desc())
df_05.display(10)


# COMMAND ----------

dis_df=df_05.distinct()
dis_df.count()

# COMMAND ----------

dropdub = dis_df.dropDuplicates(["Rating","Category"])
dropdub.display(100)

# COMMAND ----------

nnew = dropdub.withColumn(
    "Rating",
     when((col("Rating") > 4.3) & (col("Rating") <= 4.5), "Average")
    .when((col("Rating") > 4.5) & (col("Rating") <= 4.8), "Good")
    .when(col("Rating") > 4.8, "Excellent")
    .otherwise("Not Upto the mark")
)
nnew.display()

# COMMAND ----------

df_user_review=spark.read.option("header",True).csv("/FileStore/gmde1709/googleplaystore_user_reviews.csv")
df_user_review.display()

# COMMAND ----------

user_sch=StructType().add("App",StringType(),True)\
    .add("Translated_Review",StringType(),True)\
    .add("Sentiment",StringType(),True)\
    .add("Sentiment_Polarity",DoubleType(),True)\
    .add("Sentiment_Subjectivity",DoubleType(),True)

# COMMAND ----------

df_user_review=spark.read.option("header",True).schema(user_sch).csv("/FileStore/gmde1709/googleplaystore.csv")

# COMMAND ----------

final_df=df_user_review.join(nnew,df_user_review.App==nnew.App,how="left").select(nnew["*"],df_user_review["Sentiment"])
final_df.display()


# COMMAND ----------

dropdub = dis_df.dropDuplicates(["Rating","Category"])
final_df=df_user_review.join(dropdub,df_user_review.App==dropdub.App).select(dropdub["*"],df_user_review["Sentiment"])
final_df_groupby=final_df.groupBy("App").avg("Rating")
final_df_groupby.display()
