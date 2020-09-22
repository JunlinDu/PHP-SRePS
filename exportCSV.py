#Import libraries
import pymysql
import pandas as pd


#initialise connection variables
#https://pythontic.com/database/mysql/query%20a%20table
dbServerName = "127.0.0.1"
dbUser = "root"
dbPassword = ""
dbName = "php_sreps"
charSet = "utf8mb4"
cursorType = pymysql.cursors.DictCursor


#initialise connection
connection = pymysql.connect(host=dbServerName, 
    user=dbUser, 
    password=dbPassword,
    db=dbName, 
    charset=charSet,
    cursorclass=cursorType)


try:
    #read as dataframe
    batch = pd.read_sql("select * from batch", connection)
    customer = pd.read_sql("select * from customer", connection)
    inventory = pd.read_sql("select * from inventory", connection)
    manufacturer = pd.read_sql("select * from manufacturer", connection)
    product = pd.read_sql("select * from product", connection)
    sale_items = pd.read_sql("select * from sale_items", connection)
    sales = pd.read_sql("select * from sales", connection)
except Exception as e:
    print("Exception occured:{}".format(e))
finally:
    connection.close()


#export to csv    #https://towardsdatascience.com/how-to-export-pandas-dataframe-to-csv-2038e43d9c03
batch.to_csv('CSVs/batch.csv', sep='\t')
customer.to_csv('CSVs/customer.csv', sep='\t')
inventory.to_csv('CSVs/inventory.csv', sep='\t')
manufacturer.to_csv('CSVs/manufacturer.csv', sep='\t')
product.to_csv('CSVs/product.csv', sep='\t')
sale_items.to_csv('CSVs/sale_items.csv', sep='\t')
sales.to_csv('CSVs/sales.csv', sep='\t')
