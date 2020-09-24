import connection
import reading

def update_quantity(product_id, red_quan, db, cursor):
    '''
    This function updates quantity (mainly reduces) of a product in the inventory

    Note: this function mainly serves as a utility function for inserting.py
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
    >>> update_quantity(3, 20, connect, c)
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
    alist = reading.batch_retrieval_of_oldest(product_id, red_quan, cursor)
    if len(alist) == 0:
        return -1
    else:
        query = (
            "UPDATE Inventory "
            "SET quantity = quantity - " + str(red_quan) + " "
            "WHERE batch_id = " + str(alist[0][0]) + "; "
        )
        cursor.execute(query)
        db.commit()
        return 0


def update_manufacturer(manufacturer_name, manufacturer_id, db, cursor):
    '''
        Note: This function is able to update the manufacturer of the medicine. This function can be used when changing medicine manufacturers.
    '''
    assert type(manufacturer_name) == str
    assert type(manufacturer_id) == int
    update = (
            "update manufacturer set ('Manufacturer_name') where name= ('Manufacturer_id') "
            "select * from manufacturer where (+ Manufacturer_id +)"
    )
    cursor.execute(update)
    return cursor.fetchone()


if __name__ == "__main__":
    connect = connection.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    c = connect.cursor(buffered=True)
    result = update_quantity(3, 20, connect, c)
    print(result)

