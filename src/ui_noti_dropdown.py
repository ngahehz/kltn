import os

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget,QVBoxLayout, QLabel, QMessageBox, QPushButton
from PyQt6.QtCore import Qt

class DropdownNoti(QWidget):
    def __init__(self, parent=None, notification=None):
        super().__init__(parent)
        self.notification = notification
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        layout = QVBoxLayout(self)
        layout.setObjectName("DropdownLayout")

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for i, row in enumerate(self.notification.values(),start=0):
            # self.menu.addMenu(row[2])
            label = QLabel(row[3], self)  
            label.setWordWrap(True) 
            label.setMaximumHeight(63) # 2 dong 47, 3 dòng 63
            label.setMaximumWidth(200)
            label.setObjectName("dropdownItem" + str(i))
            # label.setAlignment(Qt.AlignBottom) 
            # label.mousePressEvent = self.onAction1Clicked(label.objectName())
            label.mousePressEvent = lambda event, row=row: self.onAction1Clicked(row)
            if row[4] == 0:
                label.setStyleSheet("background-color: #ffff8d;")
            layout.insertWidget(0, label)
            # layout.addWidget(label)
            
    def onAction1Clicked(self, row):
        
        custom_button = QPushButton("See")
        custom_button.setMaximumWidth(100) 

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Thông báo")
        msg_box.setMaximumWidth(50)
        msg_box.setText(row[3])
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.addButton(custom_button, QMessageBox.AcceptRole)
        msg_box.setStandardButtons(QMessageBox.Open | QMessageBox.Close)
        
        open_button = msg_box.button(QMessageBox.Open)
        open_button.clicked.connect(lambda: self.okButtonClicked(row))
        custom_button.clicked.connect(lambda: self.customButtonClicked(row))
        # nếu mà chưa đọc thì mới cập nhật trạng thái 
        if row[4] == 0:
            self.parent._controller.update_read_status_of_notification(row[0])
            self.parent.noti_count -= 1
            self.parent.ui.label_2.setText(str(self.parent.noti_count))

        msg_box.exec()

        
    def customButtonClicked(self, row):
        if not os.path.exists(row[2]):
            print("File path not found")
            QMessageBox.warning(self, "Notification", "File not exists")
            return
        
        self.parent.ui.stackedWidget.setCurrentWidget(self.parent.ui.page_3)
        self.parent._document_widget.open_file_inside(row[2], os.path.basename(row[2]))

    def okButtonClicked(self, row):
        if not os.path.exists(row[2]):
            print("File not found")
            QMessageBox.warning(self, "Notification", "File not exists")
            return
        
        os.startfile(row[2])