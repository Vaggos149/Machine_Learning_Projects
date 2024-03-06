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
