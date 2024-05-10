from PyQt6.QtCore import Qt
from PyQt6 import QtGui
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QColorDialog
from PyQt6.QtGui import QPixmap

from src.ui_page_setting import Ui_Form

from Custom_Widgets import * # trong này nó có re nè nên khỏi import re
from Custom_Widgets.QAppSettings import QAppSettings

class Setting(QWidget):
    def __init__(self, controller, parent):
        super(Setting, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.controller = controller
        self.parent = parent
        
        self.ui.comboBox.activated.connect(self.cbb_change)                        

        self.ui.color_bg_demo_lb.mousePressEvent = self.up_color_bg
        self.ui.bg_delete_btn.clicked.connect(lambda event : self.delete_img_click())                              

        self.ui.pushButton_3.clicked.connect(self.save_setting)       
                             
        self.ui.push_logo_btn.clicked.connect(self.up_logo_btn_click)
        self.ui.push_main_img_btn.clicked.connect(self.up_main_img_btn_click)                   
        self.ui.push_accent_btn.clicked.connect(self.up_accent_btn_click)
        self.ui.icon_color_cbb.currentIndexChanged.connect(self.change_icon_color)
        self.ui.push_widget_btn.clicked.connect(self.up_widget_btn_click)

        self.ui.push_logo_back_btn.clicked.connect(lambda event : self.reset())        
        self.ui.push_main_img_back_btn.clicked.connect(lambda event : self.reset())
        self.ui.push_accent_back_btn.clicked.connect(lambda event : self.reset())
        self.ui.push_icon_color_back_btn.clicked.connect(lambda event : self.reset())
        self.ui.push_widget_back_btn.clicked.connect(lambda event : self.reset())
        self.ui.upload_img_back_btn.clicked.connect(lambda event : self.reset())

        self.ui.reset_all_btn.clicked.connect(lambda event : self.reset())
        self.ui.upload_img_btn.clicked.connect(self.upload_img)

        self.load_state()
        self.load_theme()
        self.load_demo_img()
        self.load_cbb()

    def delete_img_click(self):
        if self.img_bg and self.id_image_demo == self.bg_img_path_theme:
            QMessageBox.warning(self, "Notification", "Không thể xóa ảnh đang sử dụng")
        elif self.img_bg:
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
                self.controller.delete_image(self.id_image_demo)
                self.ui.widget_5.setStyleSheet('#widget_5{background-color: #ffffff;}')
                self.img_bg = False
                self.color_bg = False
                
    def reset(self):
        btn = self.sender()
        btn_name = btn.objectName()

        if btn_name == "push_logo_back_btn":
            self.logo_img = False
            self.ui.pushButton_4.setIcon(QtGui.QIcon(self.logo_img_path_theme))
        if btn_name == "push_main_img_back_btn":
            self.db_img = False
            self.ui.push_main_img_btn.text = "UpLoad"
        if btn_name == "push_accent_back_btn":
            self.accent_color = False
            self.ui.accent_color_btn.setStyleSheet('#accent_color_btn{background-color: ' + self.accent_color_theme + '}')
        if btn_name == "push_widget_back_btn":
            self.widget_color = False
            self.ui.widget_color_btn.setStyleSheet('#widget_color_btn{background-color: ' + self.widget_color_theme + '}')
        if btn_name == "push_icon_color_back_btn":
            self.ui.icon_color_btn.setStyleSheet('#icon_color_btn{background-color: ' + self.icon_color_theme[1] + '}')
            self.ui.icon_color_cbb.setCurrentIndex(self.icon_color_theme[0])
        if btn_name == "upload_img_back_btn":
            self.img_bg = False
            self.color_bg = False
            color_pattern = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
            if color_pattern.match(self.bg_img_path_theme):
                self.parent.ui.stackedWidget.setStyleSheet('#stackedWidget{background-color:' + self.bg_img_path_theme + ';}')
            else :
                self.parent.ui.stackedWidget.setStyleSheet('#stackedWidget{background-image: url(' + self.bg_img_path_theme + '); background-position: center; background-repeat: no-repeat;padding: 0;border-top: 3px solid #ff79c6}')
                # self.parent._document_widget.ui.tableWidget_2.setStyleSheet('#tableWidget_2{background-color: rgba(255, 255, 255, 0.626);}')
        if btn_name == "reset_all_btn":
            self.load_state()
            self.controller.reset_setting()
            self.load_theme()
            QAppSettings.updateAppSettings(self.parent)

    def load_state(self):
        self.img_bg = False
        self.color_bg = False
        self.logo_img = False
        self.db_img = False
        self.accent_color = False
        self.widget_color = False

    def save_setting(self):
        bg = None
        accent = None
        widget = None

        if self.logo_img:
            self.controller.read_and_save_image(self.logo_path, "img/resource/logo3.png")

        if self.db_img:
            self.controller.read_and_save_image(self.db_img_path, "img/resource/main3.png")
            self.parent.ui.frame_2.setStyleSheet('#frame_2{background-image: url(' + self.db_img_path + '); background-position: center; background-repeat: no-repeat}')

        if self.accent_color:
            accent = self.accent_path
        else:
            accent = self.accent_color_theme

        if self.widget_color:
            widget = self.widget_path
        else:
            widget = self.widget_color_theme

        if self.img_bg:
            self.change_bg()
            bg = self.get_id_from_path(self.bg_image), self.ui.comboBox.currentIndex() # 0, 1, 2 là stretch, cover, contain
        elif self.color_bg:
            bg = self.bg_color_path, None
        else:
            bg = self.bg_img_path_theme, self.bg_img_active_theme

        self.controller.update_setting(bg, accent, widget, self.ui.icon_color_cbb.currentIndex())
        QAppSettings.updateAppSettings(self.parent)
        self.load_theme()
        self.load_state()

    ### THAY ĐỔI GIAO DIỆN ###
    def up_widget_btn_click(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.widget_color = True
            self.widget_path = color.name()
            self.ui.widget_color_btn.setStyleSheet('#widget_color_btn{background-color: ' + color.name() + '}')

    def change_icon_color(self):
        id = self.ui.icon_color_cbb.currentIndex()
        self.ui.icon_color_btn.setStyleSheet('#icon_color_btn{background-color: ' + self.controller.get_icon_from_id_color(id)[1] + '}')

    def up_accent_btn_click(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.accent_color = True
            self.accent_path = color.name()
            self.ui.accent_color_btn.setStyleSheet('#accent_color_btn{background-color: ' + color.name() + '}')

    def up_main_img_btn_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.db_img = True
            self.db_img_path = file_path
            self.ui.push_main_img_btn.text = file_path.split("/")[-1]  
        
    def up_logo_btn_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.logo_img = True
            self.logo_path = file_path
            self.ui.pushButton_4.setIcon(QtGui.QIcon(file_path))
    ###########################

    ### THÊM ẢNH VÀO CHỖ CHỌN ẢNH DEMO ###
    def insert_image_demo(self, image_id):
        label = QLabel()
        image_path = "img/" + image_id + ".png"
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setMaximumWidth(70)
        label.setMinimumWidth(70)
        label.setMaximumHeight(80)
        label.setMinimumHeight(80)
        label.setScaledContents(True)
        label.mousePressEvent = lambda event, id=image_id: self.handle_image_click(id)
        self.ui.horizontalLayout_18.insertWidget(0, label)
    
    ### LOAD RA ĐỐNG ẢNH ĐÃ TẢI LÊN ###
    def load_demo_img (self):
        for row in self.controller.get_images().values():
            self.insert_image_demo(str(row[0]))
        
    ### LOAD GIAO DIỆN HIỆN TẠI ###
    def load_theme(self):
        theme = self.controller.get_theme()
        
        self.bg_img_path_theme = self.get_id_from_path(theme[1]) # này là lấy id ảnh thôi
        color_pattern = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
        if color_pattern.match(self.bg_img_path_theme):
            self.bg_img_active_theme = None
            self.parent.ui.stackedWidget.setStyleSheet('#stackedWidget{background-color:' + theme[1] + ';}')
            self.ui.widget_5.setStyleSheet('#widget_5{background-color: ' + theme[1] + '}')
        else :
            self.bg_img_active_theme = self.controller.get_active_image()
            self.ui.comboBox.setCurrentIndex(self.bg_img_active_theme)
            self.parent.ui.stackedWidget.setStyleSheet('#stackedWidget{background-image: url(' + theme[1] + '); background-position: center; background-repeat: no-repeat;padding: 0;border-top: 3px solid #ff79c6}')
            self.parent._document_widget.ui.tableWidget_2.setStyleSheet('#tableWidget_2{background-color: rgba(255, 255, 255, 0.626);}')
            self.handle_image_click(self.bg_img_path_theme)

        self.logo_img_path_theme = theme[2]
        self.db_img_path_theme = theme[3]
        self.accent_color_theme = theme[4]
        self.widget_color_theme = theme[5]
        self.icon_color_theme = self.controller.get_icon_from_id_color(theme[6])

        self.parent.ui.top_logo.setIcon(QtGui.QIcon(self.logo_img_path_theme))
        self.parent.ui.frame_2.setStyleSheet('#frame_2{background-image: url(' + self.db_img_path_theme + '); background-position: center; background-repeat: no-repeat}')
        self.controller.change_accent(self.accent_color_theme)
        self.controller.make_noti_icon(self.icon_color_theme[1])
        self.parent.load_icon_color(self.icon_color_theme[1])
        self.load_icon_color(self.icon_color_theme[1])
        # dưới này là đổi màu widgets
        self.parent.ui.header.setStyleSheet('#header{background-color: ' + self.widget_color_theme + ';}')
        self.parent.ui.left_menu_1.setStyleSheet('#left_menu_1{background-color: ' + self.widget_color_theme + ';border-top: 3px solid #ff79c6;}')
        self.parent._document_widget.ui.noti_fr_btn.setStyleSheet('#noti_fr_btn{background-color: ' + self.widget_color_theme + ';border-radius: 10px;}')
        # self.parent._document_widget.ui.tableWidget_2.setStyleSheet('#tableWidget_2 .QPushButton{border: 2px solid ' + self.widget_color_theme + ';border-radius: 5px;color: #000000;}')
        
        self.ui.pushButton_4.setIcon(QtGui.QIcon(self.logo_img_path_theme))
        self.ui.accent_color_btn.setStyleSheet('#accent_color_btn{background-color: ' + self.accent_color_theme + '}')
        self.ui.widget_color_btn.setStyleSheet('#widget_color_btn{background-color: ' + self.widget_color_theme + '}')
        self.ui.icon_color_cbb.setCurrentIndex(self.icon_color_theme[0])
        self.ui.icon_color_btn.setStyleSheet('#icon_color_btn{background-color: ' + self.icon_color_theme[1] + '}')

    ### LOAD ICON_COLOR CÓ SẴN CHO CBB ###
    def load_cbb(self):
        for value in self.controller.get_icons().values():
            self.ui.icon_color_cbb.addItem(value[2])
            
    def get_id_from_path(self, path):
        file_name = path.split("/")[-1]  
        file_id = file_name.split("_")[0]     
        return file_id

    ### UPLOAD IMG ###  chưa có làm cái trường hợp mà up 2 ảnh giống nhau á
    def upload_img(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            name = (file_path.split("/")[-1]).split(".")[0]
            id = self.controller.add_image_to_database(name)
            if id: 
                self.controller.read_and_save_image(file_path, "img/" + str(id) + ".png")
                self.insert_image_demo(str(id))
                self.handle_image_click(str(id))
            else:
                QMessageBox.warning(self, "Notification", "Chứa tối đa 10 ảnh")

    ### SCALE ẢNH THEO CBB ###
    def cbb_change(self):
        try:
            self.handle_image_click(self.id_image_demo)
        except:
            pass

    ### HIỂN THỊ ẢNH DEMO ###
    def handle_image_click(self, image_id):
        self.img_bg = True
        self.color_bg = False
        result, self.id_image_demo = self.controller.scale_image(image_id, self.ui.widget_5.width(), self.ui.widget_5.height(), self.ui.comboBox.currentIndex(), 1)
        self.ui.widget_5.setStyleSheet('#widget_5{background-image: url(' + result + '); background-position: center; background-repeat: no-repeat;}')

    ### ĐÓNG MENU ĐỂ THAY BG ###
    def change_bg(self):
        try:
            print("Change BG")
            if self.parent.ui.left_menu_1.isExpanded():
                self.parent.ui.left_menu_1.collapseMenu()
            if self.parent.ui.left_menu_2.isExpanded():
                self.parent.ui.left_menu_2.collapseMenu()
            self.change_background()
        except Exception as e:
            print(e)

    ### THAY BG ###
    def change_background(self):
        self.bg_image, self.id_image_demo = self.controller.scale_image(self.id_image_demo, self.parent.ui.stackedWidget.width(), self.parent.ui.stackedWidget.height(), self.ui.comboBox.currentIndex())
        self.parent.ui.stackedWidget.setStyleSheet('#stackedWidget{background-image: url(' + self.bg_image + '); background-position: center; background-repeat: no-repeat;padding: 0;border-top: 3px solid #ff79c6}')
        self.parent._document_widget.ui.tableWidget_2.setStyleSheet('#tableWidget_2{background-color: rgba(255, 255, 255, 0.626);}')
        # self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        # self.ui.widget_5.setStyleSheet('#widget_5{background-image: url(' + result + '); background-position: center; background-repeat: no-repeat;}')


   ### CHỌN MÀU BG NẾU KHÔNG DÙNG ẢNH ###
    def up_color_bg(self, event):
        color = QColorDialog.getColor()
        self.ui.widget_5.setStyleSheet('#widget_5{background-color: ' + color.name() + '}')
        self.color_bg = True
        self.img_bg = False
        self.bg_color_path = color.name()

    ### SET ICON COLOR ### này ghi hàm main kh có được tại nó chưa khởi tạo xong bên parent mà nó nhảy vô r
    def load_icon_color(self, color):
        color = color.replace("#", "")
        self.ui.push_main_img_back_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/material_design/refresh.png"))
        self.ui.push_logo_back_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/material_design/refresh.png"))
        self.ui.push_accent_back_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/material_design/refresh.png"))
        self.ui.push_icon_color_back_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/material_design/refresh.png"))
        self.ui.push_widget_back_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/material_design/refresh.png"))
        self.ui.pushButton_4.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/image.png"))
        self.ui.reset_all_btn.setIcon(QtGui.QIcon("Qss/icons/" + color + "/feather/refresh-cw.png"))
        self.parent.ui.frame_5.setStyleSheet('#frame_5{ background-color: transparent; background-image: url("img/resource/bell.png"); background-position: center; background-repeat: no-repeat;}')

    
    ### KÉO THẢ ###
    def check_mouse_over_widget(self):
        if self.ui.widget_5.underMouse():
            return True
        else:
            return False

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage :
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage :
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            if self.check_mouse_over_widget():
                event.setDropAction(Qt.DropAction.CopyAction)
                file_path = event.mimeData().urls()[0].toLocalFile()

                name = (file_path.split("/")[-1]).split(".")[0]
                id = self.controller.add_image_to_database(name)
                if id:
                    self.controller.read_and_save_image(file_path, "img/" + str(id) + ".png")
                    self.insert_image_demo(str(id))
                    self.handle_image_click(str(id))
                    event.accept()
                else:
                    QMessageBox.warning(self, "Notification", "Chứa tối đa 10 ảnh")
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
