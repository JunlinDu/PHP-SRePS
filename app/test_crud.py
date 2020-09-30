import unittest
import datetime

import read
import tables
import connect

con = connect.conn()
cursor = con.cursor(buffered=True)

class TestRead(unittest.TestCase):

    def test_product_sales(self):
        result = read.product_sales('Guck - 1 handful', '2020-09-01', '2020-09-09', cursor)
        self.assertEqual('Guck - 1 handful', result[0][0])
        self.assertEqual(10, result[0][1])

    def test_product_exp_date(self):
        result = read.product_exp_date('Panadol - 25 pill box', cursor)
        self.assertEqual(datetime.date(2022, 9, 19), result[0][2])

    def test_customer_purchase_item(self):
        result = read.customer_purchase_item(3, cursor)
        self.assertEqual(1, len(result))
        for item in result:
            self.assertEqual('Fut', item[0])

    def test_prodname_by_id(self):
        result = read.prodname_by_id(1, cursor)
        self.assertEqual('Panadol - 25 pill box', result)

    def test_table(self):
        result = read.table(tables.TableEnum.product, cursor)
        self.assertEqual(5, len(result))
        result = read.table(tables.TableEnum.sale_items, cursor)
        self.assertEqual(7 ,len(result))

if __name__ == '__main__':
    unittest.main()



'''
Note: all test cases here are based on the dummy data in the database.sql
file. Tests may be failed given a different set of data, especially for
functions that queries multiple tables.
Suppose the table in the database is as the following:

product:
+-------------+------------+-------------+----------------------------------+------------+
| customer_id | surname    | given_name  | address                          | dob        |
+-------------+------------+-------------+----------------------------------+------------+
|           1 | unknown    | unknown     | NULL                             | NULL       |
|           2 | Spin       | Shooter     | 62 buddy drive, sunshine west    | 2002-02-02 |
|           3 | Fut        | Jigglehouse | 72 thirteen lane, fertree gully  | 0600-12-25 |
|           4 | Perman     | Danger      | 2000 excelcior glade, wilderness | NULL       |
|           5 | Thradburry | Leina       | NULL                             | 2050-09-12 |
+-------------+------------+-------------+----------------------------------+------------+

batch:
+----------+------------+------------+-------------+----------+
| batch_id | product_id | exp_date   | import_date | quantity |
+----------+------------+------------+-------------+----------+
|        1 |          1 | 2022-09-19 | 2020-09-12  |      200 |
|        2 |          2 | 2020-09-19 | 2020-09-10  |       10 |
|        3 |          3 | NULL       | 2020-01-01  |    10000 |
|        4 |          4 | NULL       | NULL        |     NULL |
|        5 |          5 | 0000-01-01 | NULL        |       50 |
+----------+------------+------------+-------------+----------+

customer:
+-------------+------------+-------------+----------------------------------+------------+
| customer_id | surname    | given_name  | address                          | dob        |
+-------------+------------+-------------+----------------------------------+------------+
|           1 | unknown    | unknown     | NULL                             | NULL       |
|           2 | Spin       | Shooter     | 62 buddy drive, sunshine west    | 2002-02-02 |
|           3 | Fut        | Jigglehouse | 72 thirteen lane, fertree gully  | 0600-12-25 |
|           4 | Perman     | Danger      | 2000 excelcior glade, wilderness | NULL       |
|           5 | Thradburry | Leina       | NULL                             | 2050-09-12 |
+-------------+------------+-------------+----------------------------------+------------+

inventory:
+----------+----------+------------+----------+
| inven_id | batch_id | product_id | quantity |
+----------+----------+------------+----------+
|        1 |        1 |          1 |      200 |
|        2 |        2 |          2 |       10 |
|        3 |        3 |          3 |    10000 |
|        4 |        4 |          4 |        4 |
|        5 |        5 |          5 |       50 |
+----------+----------+------------+----------+

manufacturer:
+-----------------+-------------------+
| manufacturer_id | manufacturer_name |
+-----------------+-------------------+
|               1 | Chemical Company  |
|               2 | Chem Shop         |
|               3 | Manu-chem         |
|               4 | My Dad            |
|               5 | Found It          |
+-----------------+-------------------+

sale_items:
+--------------+----------+------------+----------+
| sale_item_id | sales_id | product_id | quantity |
+--------------+----------+------------+----------+
|            1 |        1 |          1 |        1 |
|            2 |        1 |          2 |        5 |
|            3 |        2 |          2 |        2 |
|            4 |        3 |          3 |        6 |
|            5 |        4 |          3 |        2 |
|            6 |        4 |          4 |        2 |
|            7 |        5 |          5 |       10 |
+--------------+----------+------------+----------+

sales:
+----------+-------------+------------+
| sales_id | customer_id | date       |
+----------+-------------+------------+
|        1 |           1 | 2020-09-01 |
|        2 |           2 | NULL       |
|        3 |           3 | 2020-09-03 |
|        4 |           4 | 2020-09-05 |
|        5 |           5 | 2020-09-09 |
+----------+-------------+------------+

'''