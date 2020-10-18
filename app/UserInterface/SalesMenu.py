import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
from UserInterface import SaleDialog
from datetime import datetime
import read
import tables
import connect
from UserInterface.SaleDateDialog import EditDateDialog

connector = connect.conn()
c = connector.cursor()

# This variable holds an array of product arrays
productList = read.table(tables.TableEnum.product, c)

# This variable holds an array of customers
customerList = read.table(tables.TableEnum.customer, c)


class NewSalesMenu(QMainWindow):
    # This is a hash table that holds individual
    # added sales (Key: Product Id, Value: Quantity).
    # It will be added, modified or emptied
    saleItems = {}

    # This hash table holds key-value pairs of product
    # Id and corresponding name. Used for searching for
    # product name
    productTable = {}

    # Customer table, used to verify that the given
    # customer Id correspond to a registered customer
    customerTable = {}

    # aggregated total price
    total = 0.0

    # Formatted date to be passed to the database
    dateFormated = datetime.today().strftime('%Y-%m-%d')

    # customer Id of current sale, -1 means unset
    customerId = -1

    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()
        self.CurrentView = "Sale"

        self.initiateTables()
        self.setDate(datetime.today().strftime('%d/%m/%Y'))

        header = self.SaleList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.Submit.clicked.connect(lambda: self.submit())
        self.Cancel.clicked.connect(lambda: self.initialize())
        self.EditDate.clicked.connect(lambda: self.showEditDateDialog())

        # Opens a Dialog
        self.NewSaleButton.clicked.connect(lambda: self.showAddSaleDialog())

    def initiateTables(self):
        # initiates the productTable table.
        for x in productList:
            self.productTable[x[0]] = [x[1], x[3]]
        # initiates the customerTable table.
        for c in customerList:
            self.customerTable[c[0]] = (c[1] + " " + c[2])
        # print(self.productTable)
        print(self.customerTable)

    def setSaleItems(self, dialog):
        if dialog.producttuple != (0, 0):
            if dialog.producttuple[0] not in self.saleItems:
                self.saleItems[dialog.producttuple[0]] = dialog.producttuple[1]
            else:
                self.saleItems[dialog.producttuple[0]] = self. \
                                                             saleItems[dialog.producttuple[0]] + dialog.producttuple[1]
            self.setColumns()

    def setDate(self, date):
        if date is not None:
            self.DateText.setText(date)
            self.dateFormated = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
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
        self.GrandTotalText.setText(str("{:.2f}".format(self.total)))
        self.NetProfitText.setText(str("{:.2f}".format(self.total - self.total * 0.8)))

    def initialize(self):
        self.saleItems = {}
        self.total = 0
        self.setDate(datetime.today().strftime('%d/%m/%Y'))
        self.GrandTotalText.setText("0")
        self.NetProfitText.setText("0")
        self.customerId = -1
        self.SaleList.clear()
        self.SaleList.setRowCount(0)
        self.SaleList.setHorizontalHeaderLabels(['Quantity', 'Product Name', 'Quantity', 'Sub Total'])

    def submit(self):
        self.showMessageDialog("Test Message")
        return

    def verifyData(self):
        return

    def showAddSaleDialog(self):
        dialog = SaleDialog.CreateSaleDialog('Pages/AddSaleDialog.ui', self.productTable)
        dialog.buttonBox.accepted.connect(lambda: self.setSaleItems(dialog))
        dialog.exec_()

    def showEditDateDialog(self):
        dialog = EditDateDialog('Pages/EditDate.ui')
        dialog.buttonBox.accepted.connect(lambda: self.setDate(dialog.date))
        dialog.exec_()

    def showMessageDialog(self, message):
        dialog = MessageDialog(message)
        dialog.exec_()

    def showSummaryDialog(self):
        return


class Summary(QDialog):

    def __init__(self, Dialoglocation):
        super(Summary, self).__init__()
        loadUi(Dialoglocation, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.accepted.connect(lambda: self.execute())

    def execute(self):
        return


class MessageDialog(QDialog):

    def __init__(self, message):
        assert type(message) == str
        super(MessageDialog, self).__init__()
        loadUi('Pages/MessageDialog.ui', self)
        self.message.setText(message)


# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewSalesMenu()
    sys.exit(app.exec_())
