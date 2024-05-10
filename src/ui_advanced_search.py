
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QDateTimeEdit, QComboBox, QPushButton


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 334)

        self.keyword_input = QLineEdit()

        self.from_date_input = QDateTimeEdit()
        self.from_date_input.setDisplayFormat("yyyy-MM-dd")
        self.from_date_input.setCalendarPopup(True)

        self.to_date_input = QDateTimeEdit()
        self.to_date_input.setDisplayFormat("yyyy-MM-dd")
        self.to_date_input.setCalendarPopup(True)

        self.file_type_input = QComboBox()
        self.file_type_input.addItem("All")
        self.file_type_input.addItem(".docx")
        self.file_type_input.addItem(".pdf")

        self.tag_input_txt = QLineEdit()
        self.tag_input_txt.setReadOnly(True)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Qss/icons/000000/material_design/undo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.back_btn = QPushButton("")
        self.back_btn.setIcon(icon1)
        self.back_btn.setIconSize(QtCore.QSize(25, 25))

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Qss/icons/000000/material_design/refresh.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.reset_btn = QPushButton("")
        self.reset_btn.setIcon(icon2)
        self.reset_btn.setIconSize(QtCore.QSize(25, 25))

        self.tag_input_cbb = QComboBox()
        self.tag_input_cbb.addItem("Choose tag")

        self.frame = QtWidgets.QWidget()
        self.frame.setMinimumSize(QtCore.QSize(0, 30))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 30))

        self.verticalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.reset_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        layout = QFormLayout()
        layout.addRow(QLabel("Keyword:"), self.keyword_input)
        layout.addRow(QLabel("From Date:"), self.from_date_input)
        layout.addRow(QLabel("To Date:"), self.to_date_input)
        layout.addRow(QLabel("File Type:"), self.file_type_input)
        layout.addRow(QLabel("Tags:"), self.tag_input_txt)
        layout.addRow(QLabel(""), self.frame)
        layout.addRow(QLabel(""), self.tag_input_cbb)

        self.confirm_button = QPushButton("Confirm")
        self.reset_button = QPushButton("Reset")

        layout.addWidget(self.confirm_button)
        layout.addWidget(self.reset_button)

        Dialog.setLayout(layout)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    


        

    
