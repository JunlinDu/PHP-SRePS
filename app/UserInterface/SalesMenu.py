import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog, QTableView, QTableWidget
from PyQt5.uic import loadUi
from UserInterface import SaleDialog, StockMenu, ReportMenu, ForecastMenu
from datetime import datetime
import read
import tables
import connect
import insert

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

    # This hash table holds key-value pairs of products
    # Id and corresponding name. Used for searching for
    # product name
    productTable = {}

    # Customer table, used to verify that the given
    # customer Id correspond to a registered customer
    customerTable = {}

    # aggregated total price
    total = 0.0

    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()
        self.CurrentView = "Sale"

        self.initiateTables()
        self.setDate(datetime.today())

        header = self.SaleList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.SaleList.setSelectionBehavior(QTableView.SelectRows)

        self.Submit.clicked.connect(lambda: self.submit())
        self.Cancel.clicked.connect(lambda: self.initialize())

        self.NewSaleButton.clicked.connect(lambda: self.showAddSaleDialog(None, None))
        self.EditSalesItem.clicked.connect(lambda: self.editEntry())
        self.DeleteSalesItem.clicked.connect(lambda: self.deleteEntry())
        self.StockMenuButton.clicked.connect(self.openStockMenu)
        self.ReportMenuButton.clicked.connect(self.openReportMenu)
        self.ForecastMenuButton.clicked.connect(self.openForecastMenu)

    def editEntry(self):
        selectedrow = self.SaleList.selectionModel().selectedRows()
        if len(selectedrow) == 1:
            for index in sorted(selectedrow):
                PId = self.SaleList.item(index.row(), 0)
                PQuan = self.SaleList.item(index.row(), 2)
                self.showAddSaleDialog(PId.text(), PQuan.text())

    def deleteEntry(self):
        selectedrow = self.SaleList.selectionModel().selectedRows()
        if len(selectedrow) == 1:
            for index in sorted(selectedrow):
                PId = self.SaleList.item(index.row(), 0)
                self.SaleList.removeRow(index.row())

    def initiateTables(self):
        # initiates the productTable table.
        for x in productList:
            self.productTable[x[0]] = [x[1], x[3]]
        # initiates the customerTable table.
        for c in customerList:
            self.customerTable[c[0]] = (c[1] + " " + c[2])
        # print(self.productTable)
        # print(self.customerTable)

    def setSaleItems(self, dialog):
        if dialog.producttuple != (0, 0):
            if dialog.producttuple[0] not in self.saleItems:
                self.saleItems[dialog.producttuple[0]] = dialog.producttuple[1]
            else:
                self.saleItems[dialog.producttuple[0]] = self. \
                                                             saleItems[dialog.producttuple[0]] + dialog.producttuple[1]
            self.setColumns()

    def setDate(self, date):
        d = QDate(date.year, date.month, date.day)
        self.dateEdit.setDate(d)
        # print(type(self.dateEdit.date().day()))

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
        self.setDate(datetime.today())
        self.GrandTotalText.setText("0")
        self.NetProfitText.setText("0")
        self.SaleList.clear()
        self.SaleList.setRowCount(0)
        self.SaleList.setHorizontalHeaderLabels(['Quantity', 'Product Name', 'Quantity', 'Sub Total'])

    def submit(self):
        date = self.dateEdit.date()
        customerId = self.lineEditId.text()
        total = self.GrandTotalText.text()

        if not self.verifyCustomerId(customerId):
            return
        if len(self.saleItems) == 0:
            self.showMessageDialog("Sales List is Empty, Please Enter Items Before Proceed")
        self.showSummaryDialog(date, customerId,
                               self.customerTable[int(customerId)],
                               total, self.saleItems, self.productTable)


    def verifyCustomerId(self, id):
        content = self.lineEditId.text()
        if content == "" or not content.isnumeric():
            self.showMessageDialog("Please Enter a Valid Numeric Customer ID")
            return False
        elif self.customerTable[int(content)] is None:
            self.showMessageDialog("The ID Entered Has no Corresponding Entry in the Database")
            return False
        return True

    def saleConfirm(self, dialog):
        if dialog.productSoldOut is None:
            self.initialize()
        else:
            self.showMessageDialog(dialog.productSoldOut + " does not have enough left")

    def showAddSaleDialog(self, prodId, prodQuantity):
        dialog = SaleDialog.CreateSaleDialog('Pages/AddSaleDialog.ui', self.productTable, prodId, prodQuantity)
        dialog.buttonBox.accepted.connect(lambda: self.setSaleItems(dialog))
        dialog.exec_()

    def showMessageDialog(self, message):
        dialog = MessageDialog(message)
        dialog.exec_()

    def showSummaryDialog(self, date, customerId, name, total, saleItemsTable, productsTable):
        dialog = Summary(date, customerId, name, total, saleItemsTable, productsTable)
        dialog.buttonBox.accepted.connect(lambda: self.saleConfirm(dialog))
        dialog.exec_()

    def openStockMenu(self):
        self.close()
        self.Open = StockMenu.NewStockMenu()
        self.Open.show()

    def openReportMenu(self):
        self.close()
        self.Open = ReportMenu.NewReportMenu()
        self.Open.show()

    def openForecastMenu(self):
        self.close()
        self.Open = ForecastMenu.NewForecastMenu()
        self.Open.show()

class Summary(QDialog):

    productSoldOut = None

    def __init__(self, date, customerId, name, total, saleItemsTable, productsTable):
        super(Summary, self).__init__()
        loadUi('Pages/SummaryDialog.ui', self)

        self.date = datetime.strptime(str(date.year()) + "-" + str(date.month()) + "-" + str(date.day()), '%Y-%m-%d').strftime('%Y-%m-%d')
        self.customerId = customerId
        self.name = name
        self.total = total
        self.saleItems = saleItemsTable
        self.productsTable = productsTable

        self.setSaleList()

        self.Id.setText(str(self.customerId))
        self.Name.setText(self.name)
        self.Date.setText(datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%Y'))
        self.Total.setText(str(total))

        # self.buttonBox.accepted.connect(self.accept)
        self.accepted.connect(lambda: self.execute())

    def execute(self):
        arr = []
        for PId in self.saleItems:
            arr.append((PId, self.saleItems[PId]))
        print(arr)
        id = insert.new_sale(self.date, connector, c, int(self.customerId), arr)
        if type(id) is not int:
            self.productSoldOut = id.split(' ', 1)[0]
        self.close()

    def setSaleList(self):
        self.SaleList.setRowCount(len(self.saleItems))
        r = 0

        for PId in self.saleItems:
            self.SaleList.setItem(r, 0, QTableWidgetItem(self.productsTable[PId][0]))
            self.SaleList.setItem(r, 1, QTableWidgetItem(str(self.saleItems[PId])))
            r += 1


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
