from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from datetime import datetime
from src.ui_advanced_search import *

class AdvancedDialogView(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.confirm_button.clicked.connect(self.search_file)
        self.ui.reset_button.clicked.connect(self.reset_data)

    def show(self):
        QDialog.show(self)

    def reset_data(self):
        self.ui.keyword_input.clear()
        self.ui.file_type_input.setCurrentIndex(0)
        self.ui.from_date_input.setDate(QtCore.QDate.currentDate())
        self.ui.to_date_input.setDate(QtCore.QDate.currentDate())

    def search_file(self):
        self.parent.ui.tableWidget_2.setRowCount(0)
        # self.load_search_table()

        keyword = self.ui.keyword_input.text().strip() or None
        from_date = self.ui.from_date_input.dateTime().toPyDateTime().date()
        to_date = self.ui.to_date_input.dateTime().toPyDateTime().date()
        file_type = self.ui.file_type_input.currentText() or None

        # Tạo một danh sách để lưu trữ các hàng khớp với tìm kiếm
        matched_rows = []

        # Lặp qua từng hàng trong bảng gốc để tìm kiếm
        for row in range(self.parent.ui.tableWidget_2.rowCount()):
            keyword_matched = False
            date_matched = False
            type_matched = False

            # Kiểm tra từ khóa
            keyword_column = self.get_column_index("Tên")
            if keyword_column:
                item = self.parent.ui.tableWidget_2.item(row, keyword_column)
                if item is not None and (keyword is None or keyword.lower() in item.text().lower()):
                    keyword_matched = True
                else:
                    for column in range(self.parent.ui.tableWidget_2.columnCount()):
                        item = self.parent.ui.tableWidget_2.item(row, column)
                        if item is not None and (keyword is None or keyword.lower() in item.text().lower()):
                            keyword_matched = True
                            break

            # Kiểm tra ngày:
            date_column = self.get_column_index("Ngày sửa đổi")
            if date_column is not None:
                date_item = self.parent.ui.tableWidget_2.item(row, date_column)
                if date_item is not None:
                    date_text = date_item.text()
                    if date_text:
                        date = datetime.strptime(date_text, "%Y-%m-%d").date()
                        if from_date <= date <= to_date:
                            date_matched = True
                    else:
                        date_matched = True

            # Kiểm tra loại tệp tin
            type_column = self.get_column_index("Loại")
            if type_column:
                type_item = self.parent.ui.tableWidget_2.item(row, type_column)
                if type_item is not None and (type_item.text() == file_type or file_type == "All"):
                    type_matched = True

            # Kiểm tra nếu tất cả các điều kiện đều khớp
            if keyword_matched or date_matched or type_matched:
                matched_rows.append(row)

        selected_data = []
        for row in matched_rows:
            row_data = []
            for column in range(self.parent.ui.tableWidget_2.columnCount()):
                item = self.parent.ui.tableWidget_2.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")

            selected_data.append(row_data)

        self.update_search_table(selected_data)  
        QDialog.close(self)

    def get_column_index(self, header_label):
        for column in range(self.parent.ui.tableWidget_2.columnCount()):
            if self.parent.ui.tableWidget_2.horizontalHeaderItem(column).text() == header_label:
                return column
        return None
        

    def update_search_table(self, selected_data):
        self.parent.ui.tableWidget_2.clearContents()
        self.parent.ui.tableWidget_2.setRowCount(len(selected_data))
        self.parent.ui.tableWidget_2.setColumnCount(self.parent.ui.tableWidget_2.columnCount())
        self.parent.ui.tableWidget_2.setHorizontalHeaderLabels(["Tên", "Ngày sửa đổi", "Loại", "Kích thước"])  # Thay thế bằng tiêu đề cột thích hợp
        for i, row in enumerate(selected_data):  
            for column, item in enumerate(row):
                item = QtWidgets.QTableWidgetItem(item)
                self.parent.ui.tableWidget_2.setItem(i, column, item)