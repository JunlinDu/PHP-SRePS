#Import libraries
import connect
import read


#export a whole table
def table(table_name):
    '''
        function to export a specific table as a csv

        :param table_name: string name of a table
    '''
    #load headers
    headerquery = 'describe ' + table_name
    header = [row[0] for row in connect.execute(headerquery)]

    #load rows
    rowsquery = 'select * from ' + table_name
    rows = connect.execute(rowsquery)


    #write to file
    f = open('CSVs/' + table_name + '.csv', 'w')
    f.write('\"'+ '\",\"'.join(header) + '\"\n')
    for row in rows:
        f.write('\"' + '\",\"'.join(str(r) for r in row) + '\"\n')

    #close file
    f.close()
    print(print(str(len(rows)) + ' rows written successfully to ' + f.name))

def result(result):
    '''
        function to export a table as a csv
        
        :param result: results
    '''
    # write to file
    f = open('CSVs/result.csv', 'w')
    for row in result:
        f.write('\"' + '\",\"'.join(str(r) for r in row) + '\"\n')

    # close file
    f.close()
    print(print(str(len(result)) + ' rows written successfully to ' + f.name))

table('batch')
table('customer')
table('inventory')
table('manufacturer')
table('product')
table('sale_items')
table('sales')

connection = connect.conn()
cursor = connection.cursor()

result(read.sales_breakdown("2020-01-01", "2020-12-31", cursor))