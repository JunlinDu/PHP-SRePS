import mysql.connector
'''
This module contains functions that connects to the local database

'''

def conn():
    '''
    Establishing a connection to the database

    :return: a database connection
    '''
    config = {
        "user": "root",
        "passwd": "password",
        "host": "localhost",
        "database": "PHP_SRePS"
    }

    try:
        connect = mysql.connector.connect(**config)
        print("connected successfully")
        return connect
    except:
        print("connection error")


def get_results(query):
    '''
    This function returns a query result for a given query
    Should be used mainly for one-off reading from the database
    Note: Insertion and Update will not work as the changes will
    not be committed to the database table.

    :param query: a String that is a valid SQL query
    :return: the result of the query
    '''
    connect = conn()
    mycursor = connect.cursor(buffered=True)
    mycursor.execute(query)
    results = mycursor.fetchall()
    connect.close()
    return results


if __name__ == "__main__":
    connection = conn()
    mycursor = connection.cursor(buffered=True)
    mycursor.execute("SELECT * FROM product")
    results = mycursor.fetchall()
    print(results)
