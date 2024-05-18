from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from controller.elastic_client import *
from src.ui_page_search_note import Ui_Form

class Search(QWidget):
    def __init__(self, controller):
        super(Search, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller = controller
        self.client = ElasticClient()
        
        self.ui.tableWidget.hideColumn(0)
        self.ui.tableWidget.setColumnWidth(1, 200)  
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ui.sematic_search_btn.clicked.connect(lambda : self.sematic_search_btn_clicked())
        self.ui.sematic_search_txt.returnPressed.connect(lambda : self.sematic_search_btn_clicked())
        
    def sematic_search_btn_clicked(self):
        query = self.ui.sematic_search_txt.text()
        if self.ui.sematic_search_checkbox.isChecked():
            type_ranker = 'SimCSE'
        else:
            type_ranker = 'BM25'

        result = self.client.search(query, type_ranker)
        print(result)

        self.ui.tableWidget.setRowCount(0)
        for i, item in enumerate(result):
            id = int(item[1])
            self.ui.tableWidget.insertRow(i)
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(id))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(self.controller.get_files()[id][1]))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(self.controller.get_files()[id][7]))
        # self.ui.tableWidget.resizeColumnsToContents()
        # self.ui.tableWidget.resizeRowsToContents()


        