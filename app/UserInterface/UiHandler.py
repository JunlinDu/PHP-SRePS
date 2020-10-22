import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from UserInterface import StockMenu
from UserInterface import SalesMenu
from UserInterface import ReportMenu
from UserInterface import ForecastMenu
from UserInterface.Resources.images import *


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        loadUi('Pages/MainMenu.ui', self)
        self.show()
        self.StockMenu.clicked.connect(self.openStockMenu)
        self.SalesMenu.clicked.connect(self.openSalesMenu)
        self.ReportMenu.clicked.connect(self.openReportMenu)
        self.ForecastMenu.clicked.connect(self.openForecastMenu)

    def openStockMenu(self):
        self.close()
        self.Open = StockMenu.NewStockMenu()
        self.Open.show()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
