
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QDateTimeEdit, QComboBox, QPushButton


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 334)

        self.keyword_input = QLineEdit()
        self.from_date_input = QDateTimeEdit()
        self.to_date_input = QDateTimeEdit()
        self.from_date_input.setDisplayFormat("yyyy-MM-dd")
        self.to_date_input.setDisplayFormat("yyyy-MM-dd")
        self.file_type_input = QComboBox()
        self.file_type_input.addItem("")
        self.file_type_input.addItem(".docx")
        self.file_type_input.addItem(".pdf")
        self.file_type_input.addItem(".excel")
        self.file_type_input.addItem(".jpg")

        layout = QFormLayout()
        layout.addRow(QLabel("Keyword:"), self.keyword_input)
        layout.addRow(QLabel("From Date:"), self.from_date_input)
        layout.addRow(QLabel("To Date:"), self.to_date_input)
        layout.addRow(QLabel("File Type:"), self.file_type_input)

        self.confirm_button = QPushButton("Confirm")
        self.reset_button = QPushButton("Reset")

        layout.addWidget(self.confirm_button)
        layout.addWidget(self.reset_button)

        Dialog.setLayout(layout)

        QtCore.QMetaObject.connectSlotsByName(Dialog)


    
