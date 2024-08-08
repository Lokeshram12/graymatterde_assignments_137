-- Databricks notebook source
-- MAGIC %python
-- MAGIC from pyspark.sql.functions import *
-- MAGIC

-- COMMAND ----------

show tables

-- COMMAND ----------

select * from store_trans

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### deep clone

-- COMMAND ----------

CREATE TABLE delta.`abfss://inputmount@adlsgmde1709.dfs.core.windows.net/store_transaction_deepCopy` CLONE delta.`abfss://inputmount@adlsgmde1709.dfs.core.windows.net/store_transaction/`

-- COMMAND ----------

SELECT * FROM delta.`abfss://inputmount@adlsgmde1709.dfs.core.windows.net/store_transaction_deepCopy`

-- COMMAND ----------

INSERT INTO delta.`abfss://inputmount@adlsgmde1709.dfs.core.windows.net/store_transaction_deepCopy`
VALUES (8, 8.08)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###shallow clone

-- COMMAND ----------

CREATE TABLE shallow_copy2 SHALLOW CLONE store_trans

-- COMMAND ----------

select * from shallow_copy2 

-- COMMAND ----------

describe history shallow_copy2

-- COMMAND ----------

describe history store_transaction_deepCopy 
