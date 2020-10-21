import UserInterface.StockMenu as StockMenu
import UserInterface.SalesMenu as SalesMenu
import UserInterface.ReportMenu as ReportMenu
import UserInterface.ForecastMenu as ForecastMenu
import UserInterface.UiHandler as UiHandler

'''
How to use
ADD DEPENDANCY
    from UserInterface import SideMenuModule
PUT
    SideMenuModule.InitButtons(self)
IN THE INIT FOR THE UI CLASS
'''

# This handles the code/functions of the purple side menu of all the screens
def InitButtons(UI, SelectedButton):
    UI.StockMenuButton.clicked.connect(lambda i: openNewMenu(UI, StockMenu.NewStockMenu()))
    UI.SalesMenuButton.clicked.connect(lambda i: openNewMenu(UI, SalesMenu.NewSalesMenu()))
    UI.ReportMenuButton.clicked.connect(lambda i: openNewMenu(UI, ReportMenu.NewReportMenu()))
    UI.ForecastMenuButton.clicked.connect(lambda i: openNewMenu(UI, ForecastMenu.NewForecastMenu()))
    UI.BackToMenuButton.clicked.connect(lambda i: openNewMenu(UI, UiHandler.MyApp() ))
    SelectedButton.setStyleSheet("background-color: rgb(145, 131, 167); color: rgb(255, 255, 255);")

def openNewMenu(UI, Item):
    UI.close()
    UI.Open = Item
    UI.Open.show()