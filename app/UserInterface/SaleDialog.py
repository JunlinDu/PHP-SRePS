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
        self.accepted.connect(lambda : self.passData())



    def getName(self):
        content = self.ProductID.text()
        if content.isnumeric():
            if int(content) > len(self.ProductTable) or int(content) < 1:
                self.ProductNameText.setText("Please enter a valid number")
            else:
                self.ProductNameText.setText(self.ProductTable.get(int(content)))
        else:
            self.ProductNameText.setText("Please enter a number")

    def passData(self):
        self.producttuple = (int(self.ProductID.text()), int(self.Quantity.text()))
        return


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