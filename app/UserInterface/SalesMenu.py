import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
from UserInterface import SaleDialog
import read
import tables
import connect


connector = connect.conn()
c = connector.cursor()

# This holds an array of product arrays
productList = read.table(tables.TableEnum.product, c)

class NewSalesMenu(QMainWindow):

    # This is a hash table that holds individual
    # added sales (Key: Product Id, Value: Quantity).
    # It will be added, modified or emptied
    saleItems  = {}

    # This hash table holds key-value pairs of product Id
    # and corresponding name. Used for searching for product
    # name
    productTable = {}

    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()

        # initiates the productTable table.
        for x in productList:
            self.productTable[x[0]] = x[1]

        self.CurrentView = "Sale"

        # Opens a Dialog
        self.NewSaleButton.clicked.connect(lambda: self.showAddSaleDialog())

    def showAddSaleDialog(self):
        dialog = SaleDialog.CreateSaleDialog('Pages/AddSaleDialog.ui', self.productTable)
        dialog.exec_()
        print(dialog.producttuple)



# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewSalesMenu()
    sys.exit(app.exec_())
