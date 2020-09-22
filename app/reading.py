import connection
import re

def retrieve_product_sales(productName, startDate, endDate, cursor):
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
    :return: an associative array.

    Example:
    >>> retrieve_product_sales('Guck - 1 handful', '2020-09-01', '2020-09-09')
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


def retrieve_product_exp_date(productName, cursor):
    '''
    This function returns the batch_id, productname, and expiry date
    for a product (there could be multiple batch_ids and expirt dates
    for the same product).

    @type productName: str
    :param productName: the name of a specific product
    :return: an associative array.

    Example:
    >>> retrieve_product_exp_date('Panadol - 25 pill box')
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

# check a customer's
def retrieve_customer_purchase_item():
    return

# check manufacturer of a product

# check products by manufacturer


def check_value(table_name, col_name, col_to_match, condition, cursor):
    '''

    :param table_name:
    :param col_name:
    :param col_to_match:
    :param condition:
    :param cursor:
    :return:
    '''
    query = (
            "SELECT " + col_name + " FROM " + table_name + " "
            "WHERE " + col_to_match + " LIKE '" + condition + "'; "
    )
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    connect = connection.conn()
    # Note: cursor must be set up this way (although the parameter 'buffered=True')
    # can be omitted. Otherwise 'weakly-referenced object no longer exists' error will occur
    c = connect.cursor(buffered=True)
    result = retrieve_product_sales('Guck - 1 handful', '2020-09-01', '2020-09-09', c)
    print(result)
    result = retrieve_product_exp_date('Panadol - 25 pill box', c)
    print(result)
    connect.close()
