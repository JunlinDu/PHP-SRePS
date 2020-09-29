#Import libraries
import connect


#export a whole table
def export_table(table_name):
    '''
        function to export a table as a csv

        :param table_name: string name of a table
    '''
    #load headers
    headerquery = 'describe ' + table_name
    header = [row[0] for row in connect.get_results(headerquery)]

    #load rows
    rowsquery = 'select * from ' + table_name
    rows = connect.get_results(rowsquery)


    #write to file
    f = open('CSVs/' + table_name + '.csv', 'w')
    f.write('\"'+ '\",\"'.join(header) + '\"\n')
    for row in rows:
        f.write('\"' + '\",\"'.join(str(r) for r in row) + '\"\n')

    #close file
    f.close()
    print(print(str(len(rows)) + ' rows written successfully to ' + f.name))


export_table('batch')
export_table('customer')
export_table('inventory')
export_table('manufacturer')
export_table('product')
export_table('sale_items')
export_table('sales')