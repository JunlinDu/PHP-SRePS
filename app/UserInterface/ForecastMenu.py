import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi

#Imports all the Database scripts
import read
import connect

'''
This Method manages the code for the Stock UI and its related dialog popup boxes.
'''
#Probably bad practice but at dont have to create this object 1000 times


class NewForecastMenu(QMainWindow):

    def __init__(self):
        self.connector = connect.conn()
        self.cursor = self.connector.cursor()
        self.period = "1 MONTH"
        super(NewForecastMenu, self).__init__()
        loadUi('Pages/ForecastWindow.ui', self)
        self.show()
        self.CurrentView = "Forecast"
        self.resizeBreakdownTable()
        self.updatePage()

        self.periodComboBox.currentIndexChanged.connect(self.updatePage)

    def resizeBreakdownTable(self):
        header = self.BreakdownList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def generateBreakdownTable(self):
        breakdownList = self.BreakdownList
        breakdownList.clear()
        self.BreakdownList.setHorizontalHeaderLabels(['Product ID', 'Description', 'Quantity', 'Total Sales', 'Net Profit'])

        result = read.forecast_breakdown(self.period, self.cursor)
        self.BreakdownList.setRowCount(len(result))
        rowCount = 0
        for item in result:
            self.BreakdownList.setItem(rowCount, 0, QTableWidgetItem(str(item[0])))
            self.BreakdownList.setItem(rowCount, 1, QTableWidgetItem(str(item[1])))
            self.BreakdownList.setItem(rowCount, 2, QTableWidgetItem(str(item[2])))
            if str(item[3]) == "None":
                self.BreakdownList.setItem(rowCount, 3, QTableWidgetItem(""))
                self.BreakdownList.setItem(rowCount, 4, QTableWidgetItem(""))
            else:
                self.BreakdownList.setItem(rowCount, 3, QTableWidgetItem("$" + str(item[3])))
                self.BreakdownList.setItem(rowCount, 4, QTableWidgetItem("$" + str(item[4])))
            rowCount = rowCount + 1

    def generateForecastElements(self):
        result = read.forecast_elements(self.period, self.cursor)
        result = result[0]

        self.ExpectedSales.setText("$" + str(result[0]))
        self.NetProfit.setText("$" + str(result[1]))
        self.NumberOfProducts.setText(str(result[2]))

    def updatePage(self):
        self.readForecastPeriod()
        self.generateBreakdownTable()
        self.generateForecastElements()

    def readForecastPeriod(self):
        period = self.periodComboBox.currentText()
        self.period = period
# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewForecastMenu()
    sys.exit(app.exec_())