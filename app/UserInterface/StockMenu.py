import decimal
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime

# Imports all the Database scripts
import read
import connect
import tables
import insert
from UserInterface import SalesMenu, ReportMenu, ForecastMenu
from UserInterface.ProductDialog import ManageProductDialog

'''
This Method manages the code for the Stock UI and its related dialog popup boxes.
'''
# Probably bad practice but at dont have to create this object 1000 times
connector = connect.conn()
c = connector.cursor()
result = read.table(tables.TableEnum.manufacturer, c)


class NewStockMenu(QMainWindow):

    def __init__(self):
        super(NewStockMenu, self).__init__()
        loadUi('Pages/StockWindow.ui', self)
        self.show()

        # Variables
        self.CurrentView = "Product"

        # self.BatchView.setHidden(True)

        # Makes column size all even
        header = self.ProductList.horizontalHeader()

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        #header = self.dialog.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        # Set table labels

        self.GenerateProducts()

        # self.SwitchListButton.clicked.connect(self.SwitchList)
        # self.BatchBackButton.clicked.connect(self.SwitchList)
        self.CreateProductButton.clicked.connect(self.ShowCreateProductDialog)
        #self.CreateProductButton_2.clicked.connect(self.ShowManageProductDialog)
        self.CreateProductButton_2.clicked.connect(self.ShowManageProductDialog)
        self.SwitchListButton.clicked.connect(self.ShowRestoredialog)
        #self.CreateProductButton_2.clicked.connect()
        self.SalesMenuButton.clicked.connect(self.openSalesMenu)
        self.ReportMenuButton.clicked.connect(self.openReportMenu)
        self.ForecastMenuButton.clicked.connect(self.openForecastMenu)


    def SwitchList(self):
        row = self.ProductList.currentRow()
        if row == 0 or row == -1:
            return
        if self.CurrentView == "Product":
            self.CurrentView = "Batch"
            self.BatchView.setHidden(False)
            self.ProductView.setHidden(True)
            self.GenerateBatchs(self.ProductList.item(row, 0).text())
        else:
            self.CurrentView = "Product"
            self.BatchView.setHidden(True)
            self.ProductView.setHidden(False)
            self.GenerateProducts()

    # Function Requires database
    def GenerateProducts(self):
        ProductList = self.ProductList
        ProductList.clear()
        self.ProductList.setHorizontalHeaderLabels(['Code', 'Product', 'Quantity', 'Price'])

        result = read.table(tables.TableEnum.product, c)
        rowCount = 0
        self.ProductList.setRowCount(len(result))

        for item in result:
            self.ProductList.setItem(rowCount, 0, QTableWidgetItem(str(item[0])))
            self.ProductList.setItem(rowCount, 1, QTableWidgetItem(item[1]))
            self.ProductList.setItem(rowCount, 2, QTableWidgetItem( str(item[2])))
            self.ProductList.setItem(rowCount, 3, QTableWidgetItem("$" + str(item[3])))


            rowCount = rowCount + 1

    # Function Requires database, product ID included
    def GenerateBatchs(self, ProductID):
        result = read.prodname_by_id(int(ProductID), c)

        BatchList = self.BatchList
        BatchList.clear()
        BatchList.setHorizontalHeaderLabels(['Batch id', 'Import Date', 'Export Date', 'Quantity'])

        # Show product info
        self.ProductIDText.setText("Product ID: " + ProductID)
        self.ProductNameText.setText(result)
        self.ManufacturerText.setText("Manufacturer: Some Company")
        self.StockCountText.setText("420 in stock")
        self.SalesPriceText.setText("Sales Price: $50")
        self.RetailPriceText.setText("Retail Price: $50")

        # Put Batch stuff here
        self.BatchList.setRowCount(50)
        self.dialog.populateTable()
        for x in range(1, 50):
            self.BatchList.setItem(x, 0, QTableWidgetItem("ID"))
            self.BatchList.setItem(x, 1, QTableWidgetItem("Some Product"))
            self.BatchList.setItem(x, 2, QTableWidgetItem("$100"))
            self.BatchList.setItem(x, 3, QTableWidgetItem("100"))

        # Edit Product Dialog
        try:
            self.EditProductButton.clicked.disconnect()
        except:
            pass
        self.EditProductButton.clicked.connect(self.showEditProductDialog)

        # Edit Batch Dialog
        try:
            self.EditBatchButton.clicked.disconnect()
        except:
            pass
        self.EditBatchButton.clicked.connect(self.ShowEditBatchDialog)

        # Create Batch Dialog
        try:
            self.CreateBatchButton.clicked.disconnect()
        except:
            pass
        self.CreateBatchButton.clicked.connect(self.ShowCreateBatchDialog)

    # Manages input from create product dialog (STILL WIP)
    def CreateProduct(self, Dialog):
        productName = Dialog.ProductName.text()
        manufacturer = Dialog.ManufacturerBox.currentText()
        Price = round(float(Dialog.RetailPrice.text()), 2)

        insert.product(productName, manufacturer, Price, connector, c)

        # Reloads the list
        self.GenerateProducts()

    def EditProduct(self, Dialog):
        print(Dialog.ProductID.text())

    def CreateBatch(self, Dialog):
        print(Dialog.ProductID.text())

    def EditBatch(self, Dialog):
        print(Dialog.ProductID.text())

    # def ShowManageProductDialog(self):
    #     mydialog = ManageProductDialog()
    #     ####
    #     mydialog.exec()

    '''
    Editing
    def batch(product_id, exp_date, import_date, quantity, db, cursor):
    '''
    def ShowManageProductDialog(self):
        '''
        [(1, 'Panadol - 25 pill box', 1, Decimal('5.60')),
        (2, 'Meat - unknown origin, 200g', 2, Decimal('15.20')),
        (3, 'Liquid - heavy, 100ml cups', 3, Decimal('2020.05')),
        (4, 'Pain - heavy, 1 serving', 4, Decimal('0.01')),
        '''
        mydialog = CreateInputDialog('Pages/ManageProductDialog.ui')
        productList = read.table(tables.TableEnum.product, c)

        for product in productList:
            mydialog.comboBox.addItem(str(product[0]) + " " + product[1])
            #mydialog.OK.clicked.connect(lambda: self.commitToDatabase1(mydialog))
            #self.populateTable2(dialog)

        mydialog.exec()

    def commitToDatabase1(self, dialog):
        self.populateTable1(dialog)


    def populateTable2(self, dialog):
        header2 = dialog.BatchList.horizontalHeader()
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        tableWidget = dialog.BatchList
        tableWidget.clear()
        dialog.BatchList.setHorizontalHeaderLabels(['Batch_ID', 'Product_ID', 'EXP_date', 'Import_Date', 'Quantity'])

        ptl = read.table(tables.TableEnum.product, c)
        rowCount = 0
        dialog.BatchList.setRowCount(len(ptl))

        for item1 in ptl:
            dialog.BatchList.setItem(rowCount, 0, QTableWidgetItem(str(item1[0])))
            dialog.BatchList.setItem(rowCount, 1, QTableWidgetItem(str(item1[1])))
            dialog.BatchList.setItem(rowCount, 2, QTableWidgetItem(str(item1[2])))
            dialog.BatchList.setItem(rowCount, 3, QTableWidgetItem(str(item1[3])))

            rowCount = rowCount +1


    def ShowRestoredialog(self):
        mydialog = CreateInputDialog('Pages/StockDialog.ui')
        productList = read.table(tables.TableEnum.product, c)

        for product in productList:
            mydialog.ProductIDCombo.addItem(str(product[0]) + " " + product[1])

        mydialog.Confirm.clicked.connect(lambda: self.commitToDatabase(mydialog))
        mydialog.exec()

    def commitToDatabase(self, dialog):
        res = self.validateData(dialog)
        if res:
            date = dialog.dateEdit.date()

            formatedImportDate = datetime.strptime(str(date.year()) + "-" + str(date.month()) + "-" + str(date.day()), '%Y-%m-%d').strftime('%Y-%m-%d')
            date = dialog.dateEdit_2.date()
            formatedExpireDate = datetime.strptime(str(date.year()) + "-" + str(date.month()) + "-" + str(date.day()), '%Y-%m-%d').strftime('%Y-%m-%d')
            print(formatedImportDate + "   " + formatedExpireDate)

            # this is a string, need to be converted to integer later
            quantity = dialog.Quantity.text()

            product = dialog.ProductIDCombo.currentText()
            # this is a string, need to be converted to integer later
            pId = product.split()[0]

            batchId = insert.batch(int(pId), formatedExpireDate, formatedImportDate, int(quantity), connector, c)
            # print(batchId)
            self.populateTable(dialog)


    def populateTable(self, dialog):
        header1 = dialog.tableWidget.horizontalHeader()
        header1.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        tableWidget = dialog.tableWidget
        tableWidget.clear()
        dialog.tableWidget.setHorizontalHeaderLabels(['Batch_ID', 'Product_ID', 'EXP_date', 'Import_Date', 'Quantity'])

        batchList = read.table(tables.TableEnum.batch, c)
        rowCount = 0
        dialog.tableWidget.setRowCount(len(batchList))

        for item1 in batchList:
            dialog.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(item1[0])))
            dialog.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(item1[1])))
            dialog.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(item1[2])))
            dialog.tableWidget.setItem(rowCount, 3, QTableWidgetItem(str(item1[3])))
            dialog.tableWidget.setItem(rowCount, 4, QTableWidgetItem(str(item1[4])))
            rowCount = rowCount +1


    def validateData(self, dialog):
        quanInput = dialog.Quantity.text()
        if not quanInput.isnumeric():
            dialog.label.setText("Invalid Input, Quantity must be numeric")
            return False

        if int(quanInput) <=0:
            dialog.label.setText("Invalid Input, Quantity must be greater than 0")
            return False

        dialog.label.setText(" ")
        return True


    def showEditProductDialog(self):
        mydialog = CreateInputDialog('Pages/EditProductDialog.ui')
        # mydialog.buttonBox.accepted.connect(lambda: self.EditProduct(mydialog))
        mydialog.exec()

    def ShowCreateProductDialog(self):
        mydialog = CreateInputDialog('Pages/ProductDialog.ui')
        # Creates the combobox input

        for manufacturer in result:
            mydialog.ManufacturerBox.addItem(manufacturer[1])

        def priceChanged(text):
            if text != "":
                mydialog.SalesPrice.setText("$" + str(round(float(text) * 1.2, 2)))
            else:
                mydialog.SalesPrice.setText("$0")

        mydialog.onlyInt = QRegExpValidator(QRegExp("^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$"))
        mydialog.RetailPrice.setValidator(mydialog.onlyInt)

        mydialog.RetailPrice.textChanged.connect(priceChanged)
        mydialog.buttonBox.accepted.connect(lambda: self.CreateProduct(mydialog))

        mydialog.exec()

    def ShowEditBatchDialog(self):
        row = self.BatchList.currentRow()
        if row == 0 or row == -1:
            return
        mydialog = CreateInputDialog('Pages/EditBatchDialog.ui')
        mydialog.buttonBox.accepted.connect(lambda: self.EditBatch(mydialog))
        mydialog.exec()

    def ShowCreateBatchDialog(self):
        mydialog = CreateInputDialog('Pages/BatchDialog.ui')
        mydialog.buttonBox.accepted.connect(lambda: self.CreateBatch(mydialog))
        mydialog.exec()

    def openSalesMenu(self):
        self.close()
        self.Open = SalesMenu.NewSalesMenu()
        self.Open.show()

    def openReportMenu(self):
        self.close()
        self.Open = ReportMenu.NewReportMenu()
        self.Open.show()

    def openForecastMenu(self):
        self.close()
        self.Open = ForecastMenu.NewForecastMenu()
        self.Open.show()


class CreateInputDialog(QDialog):
    def __init__(self, Dialoglocation):
        super(CreateInputDialog, self).__init__()
        loadUi(Dialoglocation, self)
        self.show()


# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewStockMenu()
    sys.exit(app.exec_())
