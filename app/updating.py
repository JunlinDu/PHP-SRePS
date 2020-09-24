import connection
import reading

def update_quantity(product_id, red_quan, db, cursor):
    '''


    :param product_id:
    :param red_quan:
    :param db:
    :param cursor:
    :return:
    '''
    assert type(product_id) == int
    assert type(red_quan) == int

    query = (
        "SELECT I.batch_id FROM inventory I "
        "INNER JOIN batch B "
        "ON I.batch_id = B.batch_id "
        "WHERE (I.product_id = " + str(product_id) + ") "
        "AND (I.quantity <> 0) "
        "AND (I.quantity - " + type(red_quan) + " >= 0 ) "
        "ORDER BY B.exp_date ASC LIMIT 1; "
    )

    return


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

