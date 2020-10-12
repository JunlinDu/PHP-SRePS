import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi



class NewSalesMenu(QMainWindow):
    def __init__(self):
        super(NewSalesMenu, self).__init__()
        loadUi('Pages/SalesWindow.ui', self)
        self.show()

    def addSale(self):
        self.AddButton.clicked.connect(self.showAddSaleDialog())

    def showAddSaleDialog(self):
        mydialog = CreateAddSaleDialog('Pages/AddSaleDialog.ui')
        mydialog.exec()




class CreateAddSaleDialog(QMainWindow):
    def __init__(self, Dialoglocation):
        super(CreateAddSaleDialog, self).__init__()
        loadUi(Dialoglocation, self)
        self.show()




# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewSalesMenu()
    sys.exit(app.exec_())
