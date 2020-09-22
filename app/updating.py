import connection
import reading


def insert_product(product_name, manufacturer_name, price, connection, cursor):
    '''

    :param product_name: name of the product
    :param manufacturer_name: name of manufacturer
    :param price: price (@type: float)
    :param connection: connection to the database
    :param cursor: the cursor of the database connection
    :return: product id

    Example:
    Existing product table in the database
    +------------+-----------------------------+-----------------+---------+
    | product_id | product_name                | manufacturer_id | price   |
    +------------+-----------------------------+-----------------+---------+
    |          1 | Panadol - 25 pill box       |               1 |    5.60 |
    |          2 | Meat - unknown origin, 200g |               2 |   15.20 |
    |          6 | Panadol - 26 pill box       |               1 |    5.60 |
    +------------+-----------------------------+-----------------+---------+

    >>> insert_product("Panadol - 26 pill box", "Chemical Company", 5.60, connect, mycursor)
    The function above will return 6 because the product already existed in the table
    '''
    assert type(product_name) == str
    assert type(manufacturer_name) == str
    assert type(price) == float
    alist = reading.check_value("product", "product_id",
                                "product_name", product_name, cursor)
    if len(alist) == 0:
        manufacturer_id = insert_manufacturer(manufacturer_name, connection, cursor)
        query = (
            "INSERT INTO product (`product_name`, `manufacturer_id`, `price`) "
            "VALUES  ('" + product_name + "', '" + str(manufacturer_id) + "', '" + str(price) + "'); "
        )
        cursor.execute(query)
        connection.commit()
        print("New product " + product_name + " added! ")
        return cursor.lastrowid
    else:
        return alist[0][0]


def insert_manufacturer(manufacturer_name, connection, cursor):
    '''
    This function inserts to the database a new manufacturer record
    and returns the corresponding manufacturer_id

    :param manufacturer_name: the name of the manufacturer
    :param connection: connection to the database
    :param cursor: a cursor
    :return: manufacturer id
    '''
    assert type(manufacturer_name) == str
    alist = reading.check_value("manufacturer", "manufacturer_id",
                                "manufacturer_name", manufacturer_name, cursor)
    if len(alist) == 0:
        query = (
                "INSERT INTO manufacturer (`manufacturer_name`) "
                "VALUES ('" + manufacturer_name + "'); "
        )
        cursor.execute(query)
        connection.commit()
        print("New manufacturer " + manufacturer_name + " added! ")
        return cursor.lastrowid
    else:
        return alist[0][0]


def insert_customer():
    return


def insert_batch():
    return


def insert_new_sale():
    return


if __name__ == "__main__":
    # tests
    connect = connection.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    mycursor = connect.cursor(buffered=True)
    print(insert_product("Panadol - 26 pill box", "Chemical Company", 5.60, connect, mycursor))
    connect.close()
