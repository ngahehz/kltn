# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         layout = QVBoxLayout()

#         # Tạo combobox để chọn chữ
#         self.combobox = QComboBox(self)
#         self.combobox.addItems(["Chữ 1", "Chữ 2", "Chữ 3"])  # Thay đổi danh sách chữ tùy ý
#         layout.addWidget(self.combobox)

#         # Tạo button để thêm chữ vào vùng trống
#         self.add_button = QPushButton("Thêm", self)
#         self.add_button.clicked.connect(self.add_text)
#         layout.addWidget(self.add_button)

#         # Tạo vùng trống để hiển thị các chữ đã được chọn
#         self.text_box = QVBoxLayout()
#         layout.addLayout(self.text_box)

#         self.setLayout(layout)

#     def add_text(self):
#         selected_text = self.combobox.currentText()
#         if selected_text:
#             hbox = QHBoxLayout()
#             label = QLabel(f" [x{selected_text}] ")
#             delete_button = QPushButton("Xóa")
#             delete_button.clicked.connect(lambda: self.remove_text(hbox))
#             hbox.addWidget(label)
#             hbox.addWidget(delete_button)
#             self.text_box.addLayout(hbox)

#     def remove_text(self, hbox_layout):
#         # Xóa hbox_layout khỏi text_box
#         item = self.text_box.itemAt(self.text_box.indexOf(hbox_layout))
#         if item is not None:
#             item.widget().deleteLater()
#             self.text_box.removeItem(item)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Tạo một danh sách chứa các frame
        self.frames = []

        # Tạo một nút để thêm frame mới
        self.addButton = QPushButton("Add Frame")
        self.addButton.clicked.connect(self.add_new_frame)
        self.layout.addWidget(self.addButton, 0, 0)

    def add_new_frame(self):
        # Tạo một frame mới
        new_frame = self.create_frame(f"Frame {len(self.frames) + 1}")
        row = len(self.frames) // 2 + 1
        col = len(self.frames) % 2
        self.layout.addWidget(new_frame, row, col)
        self.frames.append(new_frame)
        row_count = self.layout.rowCount()
        print("Số dòng của QGridLayout là:", row_count)

    def create_frame(self, text):
        frame = QWidget()
        frame.setStyleSheet(
            """ 
                    border-radius: 10px;
                    border: 2px solid #6272a4;
                
            """
            )
        layout = QGridLayout()
        label = QLabel(text)
        label.setStyleSheet(
            """ 
                background-color: transparent;
            """
            )
        button = QPushButton("Delete")
        button.clicked.connect(lambda: self.remove_frame(frame))
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 0)
        frame.setLayout(layout)
        return frame

    def remove_frame(self, frame):
        self.layout.removeWidget(frame)
        frame.deleteLater()
        self.frames.remove(frame)

        # if len(self.frames) % 2 == 0:
        #     self.layout.removeRow(row)

        # Cập nhật lại chỉ mục hàng và cột của các frame còn lại
        for index, f in enumerate(self.frames):
            row = index // 2 + 1
            col = index % 2
            self.layout.addWidget(f, row, col)

        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
