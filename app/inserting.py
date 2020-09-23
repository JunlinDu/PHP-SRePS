import connection
import reading
import re

def insert_product(product_name, manufacturer_name, price, db, cursor):
    '''
    This function inserts a new product into the product table.
    If the product does not already exists in the table, the function
    will insert a new record and return the corresponding id.
    If the product already exisits in the table, the function will return
    the corresponding id only.

    :param product_name: name of the product
    :param manufacturer_name: name of manufacturer
    :param price: price (@type: float)
    :param db: connection to the database
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
        manufacturer_id = insert_manufacturer(manufacturer_name, db, cursor)
        query = (
            "INSERT INTO product (`product_name`, `manufacturer_id`, `price`) "
            "VALUES  ('" + product_name + "', '" + str(manufacturer_id) + "', '" + str(price) + "'); "
        )
        cursor.execute(query)
        db.commit()
        print("New product " + product_name + " added! ")
        return cursor.lastrowid
    else:
        return alist[0][0]


def insert_manufacturer(manufacturer_name, db, cursor):
    '''
    This function inserts to the database a new manufacturer record
    and returns the corresponding manufacturer_id

    :param manufacturer_name: the name of the manufacturer
    :param db: connection to the database
    :param cursor: the cursor of the database connection
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
        db.commit()
        print("New manufacturer " + manufacturer_name + " added! ")
        return cursor.lastrowid
    else:
        return alist[0][0]


def insert_batch(product_id, exp_date, import_date, quantity, db, cursor):
    '''
    This function .....

    :param product_id:
    :param exp_date:
    :param import_date:
    :param quantity:
    :param db:
    :param cursor:
    :return:
    '''
    query = (
            "INSERT INTO batch (`product_id`, `exp_date`, `import_date`, `quantity`) "
            "VALUES ('" + product_id + "', '" + exp_date + "', '" + import_date + "', '" + quantity + "');"
    )
    cursor.execute(query)
    db.commit()
    batch_id = cursor.lastrowid
    insert_inventory(batch_id, product_id, quantity, db, cursor)
    return batch_id


def insert_inventory(batch_id, product_id, quantity, db, cursor):

    return


def insert_customer(surname, given_name, address, dob, db, cursor):
    '''
    This function insert a new record of customer and returns the corresponding ID.

    :param surname: customer surname
    :param given_name: customer given name
    :param address: customer address
    :param dob: date of birth, in yyyy-mm-dd format
    :param db: connection to the database
    :param cursor: the cursor of the database connection
    :return: customer id that is inserted

    Example:
    >>> insert_customer('Matthew', 'Peterson', 'vic 3033', '1998-08-08', connect, mycursor)
    Suppose that the last customer ID before inserting is 5
    @return: 6
    '''
    assert type(surname) == str
    assert type(given_name) == str
    assert type(address) == str
    assert type(dob) == str and re.search("^\d{4}-\d{2}-\d{2}$", dob)
    query = (
            "INSERT INTO customer (`surname`, `given_name`, `address`, `dob`) "
            "VALUES  ('" + surname + "', '" + given_name + "', '" + address + "', '" + dob + "'); "
    )
    cursor.execute(query)
    db.commit()
    print("New customer added! ")
    return cursor.lastrowid


def insert_new_sale():
    return


if __name__ == "__main__":
    # tests
    connect = connection.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    mycursor = connect.cursor(buffered=True)
    print(insert_customer('Matthew', 'Peterson', 'vic 3033', '1998-08-08', connect, mycursor))
    connect.close()
