import os

from PyQt6.QtCore import pyqtSignal, QDateTime
from PyQt6.QtWidgets import QDialog

from src.ui_dialog_reminder import *

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from datetime import datetime



class DialogView(QDialog):
    parameter = pyqtSignal(str,str)

    def __init__(self, value):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.dateTimeEdit.setDateTime(QDateTime(datetime.now()))
        self.ui.dateTimeEdit.setDisplayFormat("yyyy-MM-dd")
        self.ui.textEdit.setText("")
        self.ui.ok_btn.clicked.connect(self.clickOK)
        self.ui.cancel_btn.clicked.connect(self.close)
        
        if value[8] != None:
            if value[9] != None:
                self.ui.textEdit.setText(str(value[9]))
            self.ui.dateTimeEdit.setDateTime(QDateTime(datetime.strptime(value[8], "%Y-%m-%d")))
            # self.ui.textEdit.d()

            # cursor = self.ui.textEdit.textCursor()
            # cursor.clearSelection()
            # self.ui.textEdit.setTextCursor(cursor)

    # def get_info(self, row_focus):
    #     self.row_focus = row_focus

    def clickOK(self):
        self.parameter.emit(self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd"), self.ui.textEdit.toPlainText())
        self.close()

    def show(self):
        QDialog.show(self)
        self.ui.textEdit.setFocus()
        self.ui.textEdit.selectAll()

    



        