import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
from UserInterface import SaleDialog
from datetime import datetime
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
    saleItems = {}

    # This hash table holds key-value pairs of product Id
    # and corresponding name. Used for searching for product
    # name
    productTable = {}

    total = 0

    dateFormat = datetime.today().strftime('%Y-%m-%d')

    customerId = -1

    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()
        self.CurrentView = "Sale"

        self.initiateTables()
        self.setDate()

        header = self.SaleList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.RefreshDate.clicked.connect(lambda : self.setDate())

        self.Cancel.clicked.connect(lambda : self.cancelSale())


        # Opens a Dialog
        self.NewSaleButton.clicked.connect(lambda: self.showAddSaleDialog())


    def test(self):
        print("Aaaaa")

    def initiateTables(self):
        # initiates the productTable table.
        for x in productList:
            self.productTable[x[0]] = [x[1], x[3]]
        # print(self.productTable)

    def setSaleItems(self, dialog):
        if dialog.producttuple != (0, 0):
            if dialog.producttuple[0] not in self.saleItems:
                self.saleItems[dialog.producttuple[0]] = dialog.producttuple[1]
            else:
                self.saleItems[dialog.producttuple[0]] = self.\
                    saleItems[dialog.producttuple[0]] + dialog.producttuple[1]
            self.setColumns()

    def setDate(self):
        self.DateText.setText(datetime.today().strftime('%d/%m/%Y'))
        # print(datetime.today().strftime('%Y-%m-%d'))

    def setColumns(self):
        self.SaleList.setRowCount(len(self.saleItems))
        rowNumber = 0
        for PId in self.saleItems:
            quantity = self.saleItems[PId]
            subtotal = float(self.productTable[PId][1] * quantity) * 1.2
            self.total += subtotal
            self.SaleList.setItem(rowNumber, 0, QTableWidgetItem(str(PId)))
            self.SaleList.setItem(rowNumber, 1, QTableWidgetItem(self.productTable[PId][0]))
            self.SaleList.setItem(rowNumber, 2, QTableWidgetItem(str(quantity)))
            self.SaleList.setItem(rowNumber, 3, QTableWidgetItem(str(subtotal)))
            rowNumber += 1
        self.GrandTotalText.setText(str(self.total))
        self.NetProfitText.setText(str("{:.2f}".format(self.total - self.total * 0.8)))

    def cancelSale(self):
        self.saleItems = {}
        self.SaleList.clear()
        self.SaleList.setRowCount(0)
        self.SaleList.setHorizontalHeaderLabels(['Quantity', 'Product Name', 'Quantity', 'Sub Total'])

    def showAddSaleDialog(self):
        dialog = SaleDialog.CreateSaleDialog('Pages/AddSaleDialog.ui', self.productTable)
        dialog.buttonBox.accepted.connect(lambda: self.setSaleItems(dialog))
        dialog.exec_()

# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewSalesMenu()
    sys.exit(app.exec_())
