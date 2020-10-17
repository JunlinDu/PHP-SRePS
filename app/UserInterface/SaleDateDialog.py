import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidgetItem, QDialog, QDialogButtonBox
from PyQt5.uic import loadUi
import re

class EditDateDialog(QDialog):

    date = None

    def __init__(self, Dialoglocation):
        super(EditDateDialog, self).__init__()
        loadUi(Dialoglocation, self)

        self.Validate.clicked.connect(lambda : self.validateData())
        self.show()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.accepted.connect(lambda: self.passData())

    def passData(self):
        if self.validateData():
            self.date = self.Date.text()

    def validateData(self):
        entry = self.Date.text()
        print(entry)
        x = re.search("(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}", entry)
        if x:
            self.message.setText("OK")
            return True
        self.message.setText("Incorrect Format")
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditDateDialog('Pages/EditDate.ui')
    sys.exit(app.exec_())