# Importing Packages
import pandas as pd
import pyodbc

# Initializing connection with SQL Server Management Studio
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=INFINITYGEAR\\SQLEXPRESS;'
                      'Database=TRAINING;'
                      'Trusted_Connection=yes;')

# Creating a dataframe from the connected database and desired table
df = pd.read_sql_query('SELECT * from dbo.Consumer_Complaints', conn)

# Exploring data
print(df.head())
print(df.shape)

# printing values of a dataframe --> shows all of them, gives results as list per row.
print(df.values)
print(df.columns)
print(df.index)

# sorting values based on column
df.sort_values("date_received")
# sorting values based on columns and different ascending orders
df.sort_values(["date_received", "product_name"], ascending=[True, False])

# subsetting columms
df_new = df.loc[:, ["product_name", "consumer_disputed", "complaint_id"]]

# resetting indexes
df_new.set_index(["complaint_id", "product_name"], inplace=True)

# grabbing first 3 rows, keeps the first 3 rows as the index is reset.
df_new.head()


