import tables
import connect
import read

'''
This module contains functions that performs Update

'''

def quantity(product_id, red_quan, db, cursor):
    '''
    This function updates quantity (mainly reduces) of a product in the inventory

    Note: this function mainly serves as a utility function for insert.py
    Customers will purchase items and the correspoing product's quantity in the
    inventory will be reduced. This function performs the reduction of quantity.

    :param product_id: ID of product
    :param red_quan: quantity to be reduced
    :param db: the database connection
    :param cursor: cursor of the database connection
    :return: -1 if the product runs out of stocks in the inventory. 0 if success.

    Example:
    Before:
    +----------+----------+------------+----------+
    | inven_id | batch_id | product_id | quantity |
    +----------+----------+------------+----------+
    |        1 |        1 |          1 |      200 |
    |        2 |        2 |          2 |       10 |
    |        3 |        3 |          3 |    10000 | <-----
    |        4 |        4 |          4 |        4 |
    |        6 |        5 |          2 |       50 |
    +----------+----------+------------+----------+
    >>> quantity(3, 20, connect, c)
    @:returns: 0
    After:
        Before:
    +----------+----------+------------+----------+
    | inven_id | batch_id | product_id | quantity |
    +----------+----------+------------+----------+
    |        1 |        1 |          1 |      200 |
    |        2 |        2 |          2 |       10 |
    |        3 |        3 |          3 |     9980 | <-----
    |        4 |        4 |          4 |        4 |
    |        6 |        5 |          2 |       50 |
    +----------+----------+------------+----------+
    '''
    assert type(product_id) == int
    assert type(red_quan) == int

    alist = read.batch_retrieval_of_oldest(product_id, red_quan, cursor)
    if len(alist) == 0:
        return -1
    else:
        query = (
                "UPDATE Inventory "
                "SET quantity = quantity - " + str(red_quan) + " "
                                                               "WHERE batch_id = " + str(alist[0][0]) + "; "
        )
        cursor.execute(query)
        return 0


def manufacturer(manufacturer_name, manufacturer_id, db, cursor):
    '''
    This function updates a manufacturer name given an id

    :param manufacturer_name: new name of the manufacturer
    :param manufacturer_id: the ID of the manufacturer whose name is inteded to be modified
    :param db: the database connection
    :param cursor: cursor of the database connection
    :return: -1 if there's no corresponding manufacturer of provided ID. 0 if updated successfully

    Example:
    Before:
    +-----------------+-----------------------+
    | manufacturer_id | manufacturer_name     |
    +-----------------+-----------------------+
    |               1 | Chemical Company      |
    |               5 | Found It              |
    |              16 | Aavis Pharmaceuticals |
    +-----------------+-----------------------+
    >>> manufacturer("updated", 5, connect, c)
    @:returns: 0
    After:
    +-----------------+-----------------------+
    | manufacturer_id | manufacturer_name     |
    +-----------------+-----------------------+
    |               1 | Chemical Company      |
    |               5 | updated               |
    |              16 | Aavis Pharmaceuticals |
    +-----------------+-----------------------+
    '''
    assert type(manufacturer_name) == str
    assert type(manufacturer_id) == int

    conditionStr = "WHERE manufacturer_id = " + str(manufacturer_id) + "; "
    cursor.execute(
        "SELECT * FROM MANUFACTURER " + conditionStr)
    alist = cursor.fetchall()
    if len(alist) == 0:
        return -1
    else:
        query = (
            "UPDATE manufacturer "
            "SET manufacturer_name = '" + manufacturer_name + "' " +
            conditionStr
        )
        cursor.execute(query)
        db.commit()
        return 0


# functions below are newly added update functions
def customer(cus_id, surname, given_name, address, dob, db, cursor):
    if validate("customer_id", cus_id, tables.TableEnum.customer, cursor):
        query = ("UPDATE customer"
                 + " SET customer_id = " + str(cus_id)
                 + " SET surname = '" + surname
                 + "' SET given_name = '" + given_name
                 + "' SET address = '" + address
                 + "' SET dob = '" + dob
                 + "' WHERE customer_id = " + str(cus_id) + "; "
                 )
        cursor.execute()
        db.commit()
        return 0
    else:
        return -1


def product(product_id, product_name, manufacturer_id, price, db, cursor):
    if validate("product_id", product_id, tables.TableEnum.product, cursor):
        query = ("UPDATE product"
                 + " SET product_name = '" + str(product_name)
                 + "' SET manufacturer_id = " + str(manufacturer_id)
                 + " SET price = " + str(price)
                 + " WHERE product_id = " + str(product_id)
                 )
        cursor.execute(query)
        db.commit()
        return 0
    else:
        return -1


def inventory(inven_id, batch_id, product_id, quantity, db, cursor):
    if validate("inven_id", inven_id, tables.TableEnum.inventory, cursor):
        query = ("UPDATE product"
                 + " SET batch_id = " + str(batch_id)
                 + " SET product_id = " + str(product_id)
                 + " SET quantity = " + str(quantity)
                 + " WHERE inven_id = " + str(inven_id)
                 )

        cursor.execute(query)
        db.commit()
        return 0
    else:
        return -1


def validate(id_name, id, table_enum, curosr):
    curosr.execute("SELECT * FROM "
                   + str(read.tablelist[table_enum.value])
                   + " WHERE " + str(id_name)
                   + " = " + str(id) + "; "
                   )
    alist = curosr.fetchall()
    if len(alist) == 0:
        return False
    else:
        return True


if __name__ == "__main__":
    connect = connect.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    c = connect.cursor(buffered=True)
    # result = quantity(3, 20, connect, c)
    # print(result)
    result = manufacturer("updated", 5, connect, c)
    print(result)
