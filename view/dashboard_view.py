from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMenu, QMainWindow, QInputDialog, QMessageBox

from src.ui_dashboard import Ui_MainWindow
from src.ui_noti_dropdown import DropdownNoti

from view.document_view import Document
from view.setting_view import Setting

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings

class MyWindow(QMainWindow):
    def __init__(self, controller, controller1, controller2):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.controller = controller
        self.document_widget = Document(controller1, self)
        self.setting_widget = Setting(controller2, self)

        self.ui.horizontalLayout_14.addWidget(self.document_widget)
        self.ui.verticalLayout_4.addWidget(self.setting_widget)

        loadJsonStyle(
            self, self.ui, jsonFiles={"json-styles/dashboard_style.json"}  
        )

        QAppSettings.updateAppSettings(self)
        
        loadJsonStyle(self.document_widget, self.document_widget.ui, jsonFiles={"json-styles/document_style.json"})

        # settings = QSettings()
        # print("Current theme", settings.value("THEME"))
        # print("Current Icons color", settings.value("ICONS-COLOR"))
    
        # for theme in self.ui.themes:
        #     print(theme.name)

        # settings.setValue("THEME", "TINA1")
            
        # QAppSettings.updateAppSettings(self)

        

        self.ui.menu_btn.clicked.connect(lambda: self.button_click())            ## Click menu button
        self.ui.all_btn.clicked.connect(lambda: self.button_click())             ## Click all button
        self.ui.tags_btn.clicked.connect(lambda: self.button_click())            ## Click tags button
        self.ui.settings_btn.clicked.connect(lambda: self.button_click())        ## Hiển thị trang cài đặt

        self.ui.top_logo.clicked.connect(lambda: self.button_click())
        self.ui.maxi_btn.clicked.connect(self.temp)                             ## Ẩn menu phải
        self.ui.add_tag_btn.clicked.connect(self.click_add_labels_btn)            ## Click add tag button
        self.ui.frame_5.mousePressEvent = self.DropDownNoti                     ## Hiển thị noti thông báo
        
        self.load()

        ################ HIỂN THỊ NOTI ################    
    def DropDownNoti(self, event):
        popup_menu = DropdownNoti(self, self.controller.get_notifications())
        app_pos = self.ui.centralwidget.mapToGlobal(QtCore.QPoint(0, 0))
        frame_pos = self.ui.frame_5.mapToGlobal(self.ui.frame_5.rect().bottomRight())
        popup_pos = QtCore.QPoint(frame_pos.x() - popup_menu.sizeHint().width(), app_pos.y() + self.ui.header.height())
        popup_menu.move(popup_pos)
        popup_menu.show()

    def button_click(self):
        btn = self.sender()
        btnName = btn.objectName()
        self.ui.left_menu_2.collapseMenu()

        if btnName == "top_logo":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)

        elif btnName == "menu_btn":
            pass

        elif btnName == "all_btn":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
            self.document_widget.load_table()

        elif btnName == "tags_btn":
            if self.document_widget.ui.info_right.expanded:
                self.document_widget.ui.info_right.collapseMenu()
            if self.ui.left_menu_2.expanded:
                self.ui.left_menu_2.collapseMenu()
            else:
                self.ui.left_menu_2.expandMenu()

        elif btnName == "settings_btn":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)


    ### LOAD ###
    def load(self):
        self.load_menu_labels()

        self.noti_count = self.controller.check_read_status()
        self.ui.label_2.setText(str(self.noti_count)) # hiển thị số thông báo chưa đọc

        height_menu = self.ui.menu_btn.sizeHint().height()
        self.ui.widget_3.setMinimumHeight(height_menu)

    # ẩn menu phải
    def temp(self):
        self.document_widget.ui.info_right.collapseMenu()

    ### TAG ĐỒ Ơ ###    
    def load_menu_labels(self):
        for row in self.controller.get_labels().values():
            self.add_label_btn(row)

    def add_label_btn(self, row):
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)

        button = QPushButton(row[1])
        button.setFixedHeight(self.ui.tags_btn.sizeHint().height())
        button.setFixedWidth(self.ui.tags_btn.maximumWidth())
        button.setFont(font)
        button.setContextMenuPolicy(Qt.CustomContextMenu) 
        button.customContextMenuRequested.connect(self.showContextMenu)
        button.clicked.connect(lambda event, id = row[0] : self.click_sub_labels_btn(id))
        button.setProperty("id", row[0])    
        self.ui.verticalLayout_9.addWidget(button)
    
    def click_sub_labels_btn (self, id):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        self.ui.left_menu_2.collapseMenu()
        self.document_widget.load_table(id)

    def showContextMenu(self, pos):
        button = self.sender()
        menu = QMenu(self)
        deleteAction = menu.addAction("Delete Label")
        action = menu.exec(button.mapToGlobal(pos))
        if action == deleteAction:
            self.warning(button)

    def warning(self, btn):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('Warning')
        messageBox.setText('Are you sure you want to delete?')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.setDefaultButton(QMessageBox.No)

        no_btn = messageBox.button(QMessageBox.No)
        no_btn.setText('Cancel')

        yesButton = messageBox.button(QMessageBox.Yes)
        yesButton.setText('Continue')

        reply = messageBox.exec_()
        if reply == QMessageBox.Yes:
            self.controller.delete_label(btn.property("id"))
            self.document_widget.delete_item_cbb(btn.text())
            btn.deleteLater()
        else:
            return

    def click_add_labels_btn(self):
        text, ok = QInputDialog.getText(self, "Enter Label Name", "Enter the new label name:")
        if ok:
            result = self.controller.add_label_to_database(text)
            if result[0]:
                self.add_label_btn(self.controller.get_labels()[result[1]])
                self.document_widget.add_item_cbb(text)
            else:
                QMessageBox.warning(self, "Notification", "Tên label này đã tồn tại")
            
    def load_icon_color(self, color):
        color = color.replace("#", "")
        self.ui.menu_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/menu.png"))
        self.ui.all_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/file.png"))
        self.ui.tags_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/tag.png"))
        self.ui.settings_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/settings.png"))
        self.ui.mini_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/window_minimize.png"))
        self.ui.maxi_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/maximize.png"))
        self.ui.close_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/x.png"))
        self.ui.add_tag_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/plus.png"))
        
        self.document_widget.ui.advanced_search.setIcon(QtGui.QIcon("Qss/icons/" + color + "/font_awesome/solid/sliders.png"))
        self.document_widget.ui.noti_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/font_awesome/regular/bell.png"))
