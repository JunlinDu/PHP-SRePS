#import libraries
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi


#Imports other files
import read
import connect
import UserInterface.SideMenuModule as SideMenuModule

#Probably bad practice but at dont have to create this object 1000 times
connector = connect.conn()
cursor = connector.cursor()

class NewReportMenu(QMainWindow):
    def __init__(self):
        super(NewReportMenu, self).__init__()
        loadUi('Pages/ReportWindow.ui', self)
        self.show()
        self.CurrentView = "Report"
        self.GenerateReportElements()
        self.GenerateSalesBreakdown()
        self.ResizeSalesBreakdown()
        #https://doc.qt.io/qtforpython/PySide2/QtWidgets/QComboBox.html
        #when i return i'll implement the date box.

    def ResizeSalesBreakdown(self):
        header = self.BreakdownList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

    def GenerateSalesBreakdown(self):
        BreakdownList = self.BreakdownList
        BreakdownList.clear()
        self.BreakdownList.setHorizontalHeaderLabels(['Date', 'Product', 'Quantity Sold', 'Total Sales', 'Net Profit'])
        result = read.sales_breakdown("2020-01-01", "2020-12-31", cursor)
        rowCount = 0
        self.BreakdownList.setRowCount(len(result))
        for item in result:
            self.BreakdownList.setItem(rowCount, 0, QTableWidgetItem(str(item[0])))
            self.BreakdownList.setItem(rowCount, 1, QTableWidgetItem(str(item[1])))
            self.BreakdownList.setItem(rowCount, 2, QTableWidgetItem(str(item[2])))
            if (str(item[3]) == "None"):
                self.BreakdownList.setItem(rowCount, 3, QTableWidgetItem(""))
                self.BreakdownList.setItem(rowCount, 4, QTableWidgetItem(""))
            else:
                self.BreakdownList.setItem(rowCount, 3, QTableWidgetItem("$"+str(item[3])))
                self.BreakdownList.setItem(rowCount, 4, QTableWidgetItem("$"+str(item[4])))
            rowCount = rowCount + 1

    def GenerateReportElements(self):
        result = read.report_elements("2020-01-01", "2020-12-31", cursor)
        result = result[0]
        print(result)
        self.TotalSales.setText("$"+str(result[0]))
        self.NetProfit.setText("$"+str(result[1]))
        self.NumberOfSales.setText(str(result[2]))
        self.NumberOfProducts.setText(str(result[3]))

# init
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewReportMenu()
    sys.exit(app.exec_())
    SideMenuModule.InitButtons(self)
