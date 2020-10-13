
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi


class CreateSaleDialog(QDialog):
    def __init__(self, Dialoglocation):
        super(CreateSaleDialog, self).__init__()
        loadUi(Dialoglocation, self)
        self.show()