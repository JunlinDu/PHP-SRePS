import sys

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi

#Imports all the Database scripts
import read
import connect
import tables
import insert





class ManageProductDialog(QDialog):
    def __init__(self):
        super(ManageProductDialog, self).__init__()
        loadUi('Pages/ManageProductDialog.ui', self)
        self.show()

        #
        # header = self.ProductList.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # self.GenerateProducts()
        self.EditProductButton.clicked.connect(self.ShowProductDialog)


    def ShowProductDialog(self):
        mydialog = CreateInputDialog1('Pages/EditProductDialog.ui')
        mydialog.EditProductButton.accepted.connect(lambda: self.EditProduct(mydialog))
        mydialog.exec()

class CreateInputDialog1(QDialog):
    def __init__(self, Dialoglocation):
            super(CreateInputDialog1, self).__init__()
            loadUi(Dialoglocation, self)
            self.show()




# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManageProductDialog()
    sys.exit(app.exec_())