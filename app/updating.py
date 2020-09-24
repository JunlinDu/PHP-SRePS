import connection
import reading

def update_quantity():
    return


def update_manufacturer(manufacturer_name,manufacturer_id,cursor):
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
