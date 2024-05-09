from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog
from datetime import datetime
from src.ui_advanced_search import *
from PyQt6.QtCore import QDateTime, Qt

class AdvancedDialogView(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.to_date_input.setDateTime(QDateTime(datetime.now()))

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
        self.parent.load_table(self.parent.label)

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
            keyword_column = 1
            # keyword_column = self.get_column_index("Tên")
            # if keyword_column:
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
            # date_column = self.get_column_index("Ngày sửa đổi")
            date_column = 3
            # if date_column is not None:
            date_item = self.parent.ui.tableWidget_2.item(row, date_column)
            if date_item is not None:
                date_text = date_item.text()
                if date_text:
                    date = datetime.strptime(date_text, "%Y-%m-%d").date()
                    if from_date <= date <= to_date:
                        date_matched = True
                # else:  # nga: chỗ này sao ra true ấy nhỉ? 
                #     date_matched = True

            # Kiểm tra loại tệp tin
            # type_column = self.get_column_index("Loại")
            type_column = 2
            # if type_column:
            type_item = self.parent.ui.tableWidget_2.item(row, type_column)
            if type_item is not None and (type_item.text() == file_type or file_type == "All"):
                type_matched = True

            # Kiểm tra nếu tất cả các điều kiện đều khớp 
            if keyword_matched and date_matched and type_matched:
            # if keyword_matched or date_matched or type_matched:
                matched_rows.append(self.parent.ui.tableWidget_2.item(row, 0).text())


        self.update_search_table(matched_rows)  
        QDialog.close(self)

    def update_search_table(self, matched_rows):
        selected_data = []
        for id in matched_rows:
            selected_data.append(self.parent.controller.get_files()[int(id)])

        self.parent.comboBoxes = []    
        
        self.parent.ui.tableWidget_2.clearContents()
        self.parent.ui.tableWidget_2.setRowCount(0)

        for i, row in enumerate(selected_data, start=0):
            # kiểm tra xem có reminder nào sắp tới không
            if row[8] == datetime.now().strftime('%Y-%m-%d'):
                self.parent.controller.check_reminder_in_notification(row)

            if row[10] == 1:
                self.parent.insert_row_table(row, 0)
            else:
                self.parent.insert_row_table(row, i)

        for row in range(self.parent.ui.tableWidget_2.rowCount()):
            for col in range(4):
                item = self.parent.ui.tableWidget_2.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)