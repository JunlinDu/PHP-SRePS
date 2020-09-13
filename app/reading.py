import connection
import re

connect = connection.conn()


def retrieve_product_sales(productName, startDate, endDate):
    '''
    Returns an associative array
    @type productName: str
    @param productName: the name of a specific product

    @type startDate: str
    @param startDate: date from.

    @type endDate: str
    @param endDate: date to.

    Date must be in yyyy-mm-dd format.

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
    mycursor = connect.cursor(buffered=True)
    mycursor.execute(query)
    results = mycursor.fetchall()
    connect.close()
    return results







if __name__ == "__main__":
    result = retrieve_product_sales('Guck - 1 handful', '2020--01', '2020-09-09')
    print(result)
