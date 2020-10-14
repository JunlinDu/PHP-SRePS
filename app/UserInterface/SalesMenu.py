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
productList = read.table(tables.TableEnum.product, c)

class NewSalesMenu(QMainWindow):

    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()

        self.productTable = {}
        for x in productList:
            self.productTable[x[0]] = x[1]

        self.CurrentView = "Sale"
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
