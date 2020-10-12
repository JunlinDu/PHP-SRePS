
import connect
import re
import tables

tablelist = ["customer", "manufacturer", "product", "inventory", "batch", "sales", "sale_items"]


def product_sales(productName, startDate, endDate, cursor):
    '''
    This function checks the number of sales of a
    product in a given time period

    @type productName: str
    :param productName: the name of a specific product
    @type startDate: str
    :param startDate: date from.
    @type endDate: str
    :param endDate: date to. Note: Date must be in yyyy-mm-dd format.
    @type: cursor: Subclass of CMySQLCursor
    :param cursor: a cursor.
    :return: a list.

    Example:
    >>> product_sales('Guck - 1 handful', '2020-09-01', '2020-09-09', cursor)
    [('Guck - 1 handful', Decimal('10'))]

    +------------------+------------+
    | ProductName      | TotalSales |
    +------------------+------------+
    | Guck - 1 handful |         10 |
    +------------------+------------+
    '''

    assert type(productName) == str
    assert re.search("^\d{4}-\d{2}-\d{2}$", startDate) and re.search("^\d{4}-\d{2}-\d{2}$", endDate)

    query = (
            "SELECT P.product_name AS ProductName, SUM(I.Quantity) AS TotalSales "
            "FROM product P "
            "INNER JOIN sale_items I "
            "ON I.product_id = P.product_id "
            "INNER JOIN Sales S "
            "ON I.sales_id = S.sales_id "
            "WHERE (S.date BETWEEN '" + startDate + "' AND '" + endDate + "') "
            "AND P.product_name LIKE '" + productName + "' "
            "GROUP BY P.product_name"
    )
    cursor.execute(query)
    return cursor.fetchall()


def product_exp_date(productName, cursor):
    '''
    This function returns the batch_id, productname, and expiry date
    for a product (there could be multiple batch_ids and expirt dates
    for the same product).

    @type productName: str
    :param productName: the name of a specific product
    :return: a list.

    Example:
    >>> product_exp_date('Panadol - 25 pill box', cursor)
    [(1, 'Panadol - 25 pill box', datetime.date(2022, 9, 19))]

    +---------+-----------------------+------------+
    | BatchId | ProductName           | ExpDate    |
    +---------+-----------------------+------------+
    |       1 | Panadol - 25 pill box | 2022-09-19 |
    +---------+-----------------------+------------+
    '''

    assert type(productName) == str

    query = (
        "SELECT I.batch_id AS BatchId, P.product_name AS ProductName, B.exp_date AS ExpDate "
        "FROM product P "
        "INNER JOIN inventory I "
        "On I.product_id = P.product_id "
        "INNER JOIN batch B "
        "On I.batch_id = B.batch_id "
        "WHERE P.product_name LIKE '" + productName + "' "
        "GROUP BY I.Batch_Id ,P.product_name"
    )

    cursor.execute(query)
    return cursor.fetchall()


def customer_purchase_item(custid, cursor):
    '''
    This function retrieves a customer's entire shipping history
    given his/her ID

    :param custid: ID of the customer
    :param cursor: cursor of the database connection
    :return: a list that contians the customer's shopping history

    Example:
    >>> customer_purchase_item(1, c)
    @:returns:
    [('Grim', 'Dibbler', 'Panadol - 25 pill box', 1),
    ('Grim', 'Dibbler', 'Meat - unknown origin, 200g', 5),
    ('Grim', 'Dibbler', 'Meat - unknown origin, 200g', 3)]
    '''
    assert type(custid) == int
    query = (
        "SELECT C.Surname, C.Given_name, P.Product_name, I.Quantity "
        "FROM customer C "
        "INNER JOIN sales S "
        "ON C.Customer_id = S.Customer_id "
        "INNER JOIN sale_items I "
        "ON I.sales_id = S.sales_id "
        "INNER JOIN product P "
        "ON P.product_id = I.product_id "
        "WHERE C.Customer_id = " + str(custid) + " "
        "GROUP BY C.Surname, C.Given_name, P.Product_name, I.Quantity;"
    )
    cursor.execute(query)
    return cursor.fetchall()


def check_value(table_name, col_name, col_to_match, condition, cursor):
    '''
    Note: This function is less likly to be called from the UI.
    This function checks a column value in a table based on a given condition,
    is mainly used for checking the existance of certian record when performing
    updates.

    :param table_name: name of the table
    :param col_name: the name of the column of which the value is retrieved
    :param col_to_match: the name of the column against which the contion is verified
    :param condition:
    :param cursor: cursor of the database connection
    :return: a list

    Example:
    Suppose this function queries the table below:
    +------------+-----------------------------+-----------------+---------+
    | product_id | product_name                | manufacturer_id | price   |
    +------------+-----------------------------+-----------------+---------+
    |          1 | Panadol - 25 pill box       |               1 |    5.60 |
    |          2 | Meat - unknown origin, 200g |               2 |   15.20 |
    +------------+-----------------------------+-----------------+---------+

    >>> check_value("product", "product_id", "product_name", 'Panadol - 25 pill box', cursor)
    @return: [(1,)]
    '''
    assert type(col_name) == str
    assert type(table_name) == str
    assert type(col_to_match) == str
    assert type(condition) == str

    query = (
            "SELECT " + col_name + " FROM " + table_name + " "
            "WHERE " + col_to_match + " LIKE '" + condition + "'; "
    )
    cursor.execute(query)
    return cursor.fetchall()


def prodname_by_id(product_id, cursor):
    '''
    This function returns a product name given an id.

    :param product_id: ID of the product
    :param cursor: cursor of the database connection
    :return: @String | Product name

    Example:
    >>> prodname_by_id(2, cursor)
    @:returns: "Meat - unknown origin, 200g"
    '''

    assert type(product_id) == int

    query = (
        "SELECT product_name FROM product "
        "WHERE product_id = " + str(product_id) + "; "
    )
    cursor.execute(query)
    alist = cursor.fetchall()
    return alist[0][0]


def batch_retrieval_of_oldest(product_id, red_quan, cursor):
    '''
    Note: this function mainly serves as a utility function for operations in updating
    and is less likely to be called from UI.

    This function returns the batch_id from the inventory for a provided product
    where the product's quantity is more than 0, and it is greater than 0 after
    quantity reduction, and is of the earliest expire date.

    :param product_id: ID of product
    :param red_quan: quantity to be reduced
    :param cursor: cursor of the database connection
    :return: a list contains the batch_id of the selected product

    Example:
    >>> batch_retrieval_of_oldest()(1, 10, c)
    @:returns [(1,)]
    '''
    assert type(product_id) == int
    assert type(red_quan) == int

    query = (
            "SELECT I.batch_id FROM inventory I "
            "INNER JOIN batch B "
            "ON I.batch_id = B.batch_id "
            "WHERE (I.product_id = " + str(product_id) + ") "
            "AND (I.quantity <> 0) "
            "AND (I.quantity - " + str(red_quan) + " >= 0 ) "
            "ORDER BY B.exp_date ASC LIMIT 1; "
    )
    cursor.execute(query)
    return cursor.fetchall()


def table(table_enum, cursor):
    '''
    This function returns an entire table given an TableEnum

    :param table_enum: an Enum Object that corresponds to a table (refer to tables.py).
    :param cursor: a cursor of the database connection
    :return: a list contains an entire table

    Example:
    >>> table(tables.TableEnum.product, c)
    @:returns:
    [(1, 'Panadol - 25 pill box', 1, Decimal('5.60')),
    (2, 'Meat - unknown origin, 200g', 2, Decimal('15.20')),
    (3, 'Liquid - heavy, 100ml cups', 3, Decimal('2020.05')),
    (4, 'Pain - heavy, 1 serving', 4, Decimal('0.01')),
    (5, 'Guck - 1 handful', 5, None),
    (6, 'Panadol - 26 pill box', 1, Decimal('5.60'))]

    '''
    assert type(table_enum) == tables.TableEnum

    query = (
        "SELECT * FROM " + tablelist[table_enum.value] + "; "
    )
    cursor.execute(query)
    return cursor.fetchall()


def product_quantity(cursor):
    '''
    :return:
    [(1, 'Panadol - 25 pill box', Decimal('5.60'), Decimal('200')),
    (2, 'Meat - unknown origin, 200g', Decimal('15.20'), Decimal('10')),
    (3, 'Liquid - heavy, 100ml cups', Decimal('2020.05'), Decimal('10000')),
    (4, 'Pain - heavy, 1 serving', Decimal('0.01'), Decimal('4')),
    (5, 'Guck - 1 handful', None, Decimal('50'))]
    '''

    query = (
        "SELECT p.Product_id, p.Product_name, p.Price, SUM(i.Quantity) AS Quantity "
        "FROM Product p "
        "INNER JOIN Inventory i "
        "ON i.Product_id = p.Product_id "
        "GROUP BY p.Product_id; "
    )
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    connect = connect.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    c = connect.cursor()
    result = product_sales('Guck - 1 handful', '2020-09-01', '2020-09-09', c)
    print(result)
    result = product_exp_date('Panadol - 25 pill box', c)
    print(result)
    result = batch_retrieval_of_oldest(3, 10, c)
    print(result)
    print(len(result))
    print(result[0][0])
    result = prodname_by_id(2, c)
    print(result)
    print("\n")
    result = table(tables.TableEnum.product, c)
    print(result)
    for item in result:
        print(item)

    result = customer_purchase_item(1, c)
    print(result)
    for item in result:
        print(item)

    print(product_quantity(c))
    connect.close()
