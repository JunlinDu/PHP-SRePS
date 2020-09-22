import mysql.connector

def conn():
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


def get_results (query):
    '''
    This method returns a query result for a given query

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