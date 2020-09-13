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


if __name__ == "__main__":
    connection = conn()
    mycursor = connection.cursor(buffered=True)
    mycursor.execute("SELECT * FROM product")
    results = mycursor.fetchall()
    print(results)