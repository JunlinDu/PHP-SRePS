#Import libraries
import pymysql #pip install PyMySQL
import pandas as pd #pip install pandas
from matplotlib import pyplot as plt #pip install matplotlib

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

#body
try:
    #with connection.cursor() as cursor:
    query = "select * from items"

    #read as dataframe
    dataframe = pd.read_sql(query, connection)

except Exception as e:
    print("Exception occured:{}".format(e))
finally:
    connection.close()


#export to csv
    #https://towardsdatascience.com/how-to-export-pandas-dataframe-to-csv-2038e43d9c03
    #dataframe.to_csv('dataframe.csv', sep='\t')