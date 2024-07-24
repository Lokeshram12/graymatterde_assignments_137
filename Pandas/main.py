# import pandas as pd 

# df=pd.read_csv("fileName.csv")

 # df = dataframe - a kind of data structure
# print(df.to_string())

# It has functions for analyzing, cleaning, exploring, and manipulating data.

# Pandas are also able to delete rows that are not relevant, or contains wrong values, like empty or NULL values. 
# This is called cleaning the data.

import pandas

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pandas.DataFrame(mydataset)

print(myvar)

# A Pandas Series is like a column in a table.

# It is a one-dimensional array holding data of any type.

# A Pandas DataFrame is a 2 dimensional data structure,
# like a 2 dimensional array, or a table with rows and columns.

# Big data sets are often stored, or extracted as JSON.

# JSON is plain text, but has the format of an object, and is well known in the world 
# of programming, including Pandas.

#  head() and tail() method used to print first and last 5 elements respectively and 
#  can also take input and print only specified number of rows

# dropna , fillna

# dropduplicates()  and duplicated()

# The corr() method calculates the relationship between each column in your data set.

# Pandas uses the plot() method to create diagrams.

