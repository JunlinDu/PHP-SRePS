import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog, QDialogButtonBox
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui

import read
import tables
import connect


class CreateSaleDialog(QDialog):

    producttuple = ()

    def __init__(self, Dialoglocation, ProductTable):
        super(CreateSaleDialog, self).__init__()
        loadUi(Dialoglocation, self)
        self.ProductTable = ProductTable
        self.show()
        self.CheckName.clicked.connect(lambda : self.getName())
        self.buttonBox.accepted.connect(self.accept)
        #TODO ADD REJECTED
        self.accepted.connect(lambda : self.passData())

    def getName(self):
        content = self.ProductID.text()
        if self.verifyIntegrity(content):
            self.ProductNameText.setText(self.ProductTable.get(int(content)))

    def passData(self):
        pId = self.ProductID.text()
        pQuan = self.Quantity.text()
        if self.verifyIntegrity(pId, pQuan):
            self.producttuple = (int(pId), int(pQuan))


    def verifyIntegrity(self, *args):
        for num in args:
            if not num.isnumeric():
                self.showErrorMsg()
                return False
            if int(num) < 1:
                self.showErrorMsg()
                return False
            if int(num) > len(self.ProductTable):
                self.showErrorMsg()
                return False
        return True

    def showErrorMsg(self):
        self.ProductNameText.setText("Please enter a valid number")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    connector = connect.conn()
    c = connector.cursor()
    productList = read.table(tables.TableEnum.product, c)
    productTable = {}
    for x in productList:
        productTable[x[0]] = x[1]
    print(productTable)
    window = CreateSaleDialog('Pages/AddSaleDialog.ui', productTable)
    sys.exit(app.exec_())