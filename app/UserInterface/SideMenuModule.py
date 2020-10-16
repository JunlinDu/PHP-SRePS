import UserInterface.StockMenu as StockMenu
import UserInterface.SalesMenu as SalesMenu
import UserInterface.ReportMenu as ReportMenu
#from UserInterface import ForecastMenu //WIP WAITING FOR SCRIPT TO BE FINISHED


'''
How to use
ADD DEPENDANCY
    from UserInterface import SideMenuModule
PUT
    SideMenuModule.InitButtons(self)
IN THE INIT FOR THE UI CLASS
'''

# This handles the code/functions of the purple side menu of all the screens
def InitButtons(UI):
    UI.StockMenuButton.clicked.connect(lambda i: openNewMenu(UI, StockMenu.NewStockMenu()))
    UI.SalesMenuButton.clicked.connect(lambda i: openNewMenu(UI, SalesMenu.NewSalesMenu()))
    UI.ReportMenuButton.clicked.connect(lambda i: openNewMenu(UI, ReportMenu.NewReportMenu()))
    #UI.ForecastMenuButton.clicked.connect(lambda i: openNewMenu(UI, ForecastMenu.NewForecastMenu()))

def openNewMenu(UI, Item):
    UI.close()
    UI.Open = Item
    UI.Open.show()
