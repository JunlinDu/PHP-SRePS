# import libraries
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi

import UserInterface.SideMenuModule as SideMenuModule
import connect
import export
import read


class NewReportMenu(QMainWindow):
    def __init__(self):
        # initialise variables
        self.connector = connect.conn()
        self.cursor = self.connector.cursor()
        self.CurrentView = "Report"
        self.startDate = "2020-01-01"
        self.endDate = "2020-12-31"
        # initialise window
        super(NewReportMenu, self).__init__()
        loadUi('Pages/ReportWindow.ui', self)
        self.show()
        # refresh page
        self.UpdatePage()
        # setup signals
        self.monthComboBox.currentIndexChanged.connect(self.UpdatePage)
        self.yearComboBox.currentIndexChanged.connect(self.UpdatePage)
        self.ExportReport.clicked.connect(self.Export)
        SideMenuModule.InitButtons(self)

    def ResizeSalesBreakdown(self):
        # resize breakdown list to better fit.
        header = self.BreakdownList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

    def GenerateSalesBreakdown(self):
        # reset breakdown list
        self.BreakdownList.clear()
        self.BreakdownList.setHorizontalHeaderLabels(['Date', 'Product', 'Quantity Sold', 'Total Sales', 'Net Profit'])
        self.ResizeSalesBreakdown()
        # refresh variables
        self.ReadDateBoxes()
        result = read.sales_breakdown(self.startDate, self.endDate, self.cursor)
        self.BreakdownList.setRowCount(len(result))
        # print sales via loop
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

    def GenerateReportElements(self):
        # refresh variables
        self.ReadDateBoxes()
        # read/select first row of report_elements
        result = read.report_elements(self.startDate, self.endDate, self.cursor)[0]
        # write results to ui elements
        if str(result[0]) == "None":
            self.TotalSales.setText("$0")
            self.NetProfit.setText("$0")
        else:
            self.TotalSales.setText("$" + str(result[0]))
            self.NetProfit.setText("$" + str(result[1]))
        self.NumberOfSales.setText(str(result[2]))
        self.NumberOfProducts.setText(str(result[3]))

    def UpdatePage(self):
        self.GenerateReportElements()
        self.GenerateSalesBreakdown()

    def ReadDateBoxes(self):
        # read month
        month = int(self.monthComboBox.currentIndex())
        if month == 0:
            startMonth = "01"
            endMonth = "12"
        else:
            startMonth, endMonth = str('{:02}'.format(month)), str('{:02}'.format(month))
        # read year
        year = self.yearComboBox.currentText()
        if year == "ALL DATA":
            self.monthComboBox.setCurrentText("Any")
            startYear = "0000"
            endYear = "9999"
        else:
            startYear, endYear = year, year
        # update date fields
        self.startDate = startYear + "-" + startMonth + "-01"
        self.endDate = endYear + "-" + endMonth + "-31"

    def Export(self):
        result = read.sales_breakdown(self.startDate, self.endDate, self.cursor)
        export.result(result)
        # implement popup?


# testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewReportMenu()
    sys.exit(app.exec_())
