import os

from datetime import datetime 
from PyQt6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QMenu, QFileDialog, QMessageBox, QTableWidgetItem, QInputDialog, QComboBox, QGridLayout
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QColor, QDesktopServices
from PyQt6.QtWebEngineWidgets import QWebEngineView

from src.ui_page_document import Ui_Form
from view.dialog_reminder_view import *
from view.advanced_search_view import *

class Document(QWidget):
    def __init__(self, controller, parent):
        super(Document, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller = controller
        self.parent = parent

        self.ui.add_btn.clicked.connect(lambda: self.add_file())                ## Thêm file
        self.ui.tableWidget_2.itemClicked.connect(self.on_item_clicked)         ## Hiển thị thông tin file khi click vào file ở table
        self.ui.note_txt.textChanged.connect(self.note_text_change)             ## Cập nhật note của file
        self.ui.noti_btn.clicked.connect(self.open_noti_dialog)                 ## Mở dialog cài đặt thông báo
        self.ui.tabWidget_2.tabCloseRequested.connect(self.close_tab)           ## Đóng tab

        self.ui.search_input.textChanged.connect(self.search_files)
        self.ui.advanced_search.clicked.connect(self.show_advanced_search_dialog)

        self.load_table()
        self.load_cbb()
        self.ui.new_tag_btn.clicked.connect(self.add_new_frame)
        self.ui.new_tag_cbb.currentIndexChanged.connect(self.new_tag_cbb_changed)

        self.ui.tableWidget_2.keyPressEvent = self.keyPressEvent                ## Sự kiện di chuyển lên xuống bằng bàn phím trên table
        self.ui.comboBox.currentIndexChanged.connect(self.sort_table)

    def show_advanced_search_dialog(self):
        self.advanced_search_dialog = AdvancedDialogView(self)
        self.advanced_search_dialog.show()
        
    def search_files(self):
        search_text = self.ui.search_input.text().lower()
        row_count = self.ui.tableWidget_2.rowCount()

        for row in range(row_count):
            file_name = self.ui.tableWidget_2.item(row, 1).text().lower()
            if search_text in file_name:
                self.ui.tableWidget_2.setRowHidden(row, False)
            else:
                self.ui.tableWidget_2.setRowHidden(row, True)

    ### THÊM FILE MỚI ###
    def add_file(self):
        # import docx2txt text = docx2txt.process(doc_file)
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Upload file", "", "'PDF and DOCX files (*.pdf *.docx)'")
        if not file_paths:
            return 

        for file_path in file_paths:
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            # check xem đã tồn tại hay chưa
            if self.controller.check_url_is_exist(file_path):
                QMessageBox.warning(self, "Notification", "File "+ file_name +" already exists")
                continue

            file_type = os.path.splitext(file_path)[1]

            if file_type in ['.pdf', '.docx']:
                file_size_kb = os.path.getsize(file_path) / 1024
                upload_date = datetime.now().date()

                row_position = self.ui.tableWidget_2.rowCount()
                new_row = (file_name, file_path, upload_date, file_size_kb, file_type)
                id = self.controller.add_file_to_database(new_row)

                button = QPushButton("Delete")
                button.setFocusPolicy(Qt.NoFocus)
                checkbox = QCheckBox()
                checkbox.setFocusPolicy(Qt.NoFocus)
                combobox = self.create_cbb()
                combobox.setFocusPolicy(Qt.NoFocus)
                self.comboBoxes.append(combobox)

                self.ui.tableWidget_2.insertRow(row_position)
                self.ui.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(str(id)))
                self.ui.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(str(new_row[0])))
                self.ui.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(str(new_row[4])))
                self.ui.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(new_row[2])))
                self.ui.tableWidget_2.setItem(row_position, 4, QTableWidgetItem())
                self.ui.tableWidget_2.setItem(row_position, 5, QTableWidgetItem())
                self.ui.tableWidget_2.setItem(row_position, 6, QTableWidgetItem())

                button.clicked.connect(lambda event, id = id: self.delete_file(id))
                combobox.activated.connect(lambda index, combo_box=combobox: self.combo_box_changed(index, combo_box))
                checkbox.stateChanged.connect(lambda state, id = id: self.set_priority(id))
                combobox.setCurrentText("")

                self.ui.tableWidget_2.setCellWidget(row_position, 4, combobox)
                self.ui.tableWidget_2.setCellWidget(row_position, 5, checkbox)
                self.ui.tableWidget_2.setCellWidget(row_position, 6, button)

            else:
                QMessageBox.warning(self, "Extension not supported", "Cannot open file")
       
    ################ HIỂN THỊ THÔNG TIN FILE KHI CLICK VÀO TABLE ################
    def on_item_clicked(self):
        self.ui.info_right.expandMenu()
        if self.parent.ui.left_menu_2.expanded:
            self.parent.ui.left_menu_2.collapseMenu()
        # self.index = self.ui.tableWidget_2.currentRow() # t laays casi file index nayf chi as ta
        id = self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 0).text()
        self.row_focus = self.controller.get_files()[int(id)]
        self.ui.name_lb.setText("<b>" + str(self.row_focus[1]) + "</b>")
        self.ui.dir_lb.setText("<b>Đường dẫn</b>: " + str(self.row_focus[2]))
        self.ui.dir_lb.setToolTip(" Click to open folder of file ")
        self.ui.dir_lb.mousePressEvent = lambda event: self.open_folder(self.row_focus[2])

        self.ui.size_lb.setText("<b>Size</b>: " + str(round(self.row_focus[4], 2)) + " kB")

        if(self.row_focus[7] == None):
            self.ui.note_txt.setText("")
        else:
            self.ui.note_txt.setText(str(self.row_focus[7]))

        self.ui.new_tag_cbb.setCurrentIndex(1)
        self.tag_widget()

    ################ CẬP NHẬT NOTES CỦA FILE ################ (t thêm s cho nó không có màu)
    def note_text_change(self):
        self.controller.update_note_of_file(self.row_focus[0], self.ui.note_txt.toPlainText())

    ################ MỞ DIALOG CÀI ĐẶT THÔNG BÁO ################
    def open_noti_dialog(self):
        self.noti_dialog = DialogView(self.row_focus)
        self.noti_dialog.parameter.connect(self.update_file)
        self.noti_dialog.show()

    ################ TẠO HOẶC CHỈNH SỬA REMINDER Ở ĐÂY NÈ ################
    def update_file(self, date, note):
        self.controller.update_reminder_of_file(self.row_focus[0], date, note)

    ### MỞ FOLDER ###
    def open_folder(self, file_path=None):
        folder_path = os.path.dirname(file_path)
        if folder_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    ### THÊM DÒNG ###
    def insert_row_table(self, row, i):
        button = QPushButton("Delete")
        button.setFocusPolicy(Qt.NoFocus)
        checkbox = QCheckBox()
        checkbox.setFocusPolicy(Qt.NoFocus)
        if row[10] == 1:                # không để i = 0 vì có thể trùng file đầu
            checkbox.setChecked(True)
        combobox = self.create_cbb()
        combobox.setFocusPolicy(Qt.NoFocus)
        self.comboBoxes.append(combobox)

        self.ui.tableWidget_2.insertRow(i)
        self.ui.tableWidget_2.setItem(i, 0, QTableWidgetItem(str(row[0])))
        self.ui.tableWidget_2.setItem(i, 1, QTableWidgetItem(str(row[1])))
        self.ui.tableWidget_2.setItem(i, 2, QTableWidgetItem(str(row[5])))
        self.ui.tableWidget_2.setItem(i, 3, QTableWidgetItem(str(row[3])))
        self.ui.tableWidget_2.setItem(i, 4, QTableWidgetItem())
        self.ui.tableWidget_2.setItem(i, 5, QTableWidgetItem())
        self.ui.tableWidget_2.setItem(i, 6, QTableWidgetItem())

        self.ui.tableWidget_2.setCellWidget(i, 4, combobox)
        self.ui.tableWidget_2.setCellWidget(i, 5, checkbox)
        self.ui.tableWidget_2.setCellWidget(i, 6, button)

        button.clicked.connect(lambda event, id=row[0]: self.delete_file(id))
        combobox.activated.connect(lambda index, combo_box=combobox: self.combo_box_changed(index, combo_box))
        combobox.setCurrentText(self.controller.get_label_name_by_id_file(row[6]))
        checkbox.stateChanged.connect(lambda state, id=row[0]: self.set_priority(id))

        if not os.path.exists(row[2]):
            print("File",str(row[1]),"not found")
            for column in range(7):
                _item = self.ui.tableWidget_2.item(i, column)
                _item.setBackground(QColor(234, 108, 108, 100))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            current_row = self.ui.tableWidget_2.currentRow()
            if current_row > 0:
                self.ui.tableWidget_2.setCurrentCell(current_row - 1, self.ui.tableWidget_2.currentColumn())
                self.on_item_clicked()
        elif event.key() == Qt.Key_Down:
            current_row = self.ui.tableWidget_2.currentRow()
            if current_row < self.ui.tableWidget_2.rowCount() - 1:
                self.ui.tableWidget_2.setCurrentCell(current_row + 1, self.ui.tableWidget_2.currentColumn())
                self.on_item_clicked()

    ### LOAD TABLE ###
    def load_table (self, labels = None):
        # nếu có ấn button sub_label thì lấy file theo label
        if labels:  
            file_list = self.controller.get_files(labels)
        else:
            file_list = self.controller.get_files()

        # tạo danh sách để lưu trữ cbb tạp ra để sau này có thể thay đổi giá trị của cbb cho dễ
        self.comboBoxes = []    
        
        self.ui.tableWidget_2.clearContents()
        self.ui.tableWidget_2.setRowCount(0)

        for i, row in enumerate(file_list.values(), start=0):
            # kiểm tra xem có reminder nào sắp tới không
            if row[8] == datetime.now().strftime('%Y-%m-%d'):
                self.controller.check_reminder_in_notification(row)

            if row[10] == 1:
                self.insert_row_table(row, 0)
            else:
                self.insert_row_table(row, i)

        self.ui.tableWidget_2.hideColumn(0)
        self.ui.tableWidget_2.setColumnWidth(1, 200)  
        self.ui.tableWidget_2.setColumnWidth(2, 50) 
        self.ui.tableWidget_2.setColumnWidth(5, 60) 
        self.ui.tableWidget_2.setColumnWidth(6, 60) 
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        for row in range(self.ui.tableWidget_2.rowCount()):
            for col in range(4):
                item = self.ui.tableWidget_2.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    ### CBB FOR TABLE ###
    def create_cbb (self):
        combo_box = QComboBox()
        combo_box.setStyleSheet(
        """QComboBox{
            background-color: transparent;
            border-radius: 5px;
            border: 1px solid rgb(33, 37, 43);
        }
        QComboBox:hover{
            border: 1px solid rgb(64, 71, 88);
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px; 
            border-left-width: 3px;
            border-left-color: rgba(39, 44, 54, 150);
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;	
            background-position: center;
            background-repeat: no-reperat;
        }
        QComboBox QAbstractItemView {
            color: rgb(121, 175, 255);	
            background-color: rgb(255, 255, 255);
        }""")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        combo_box.setFont(font)

        combo_box.addItem("(+)")
        combo_box.addItem("")

        for row in self.controller.get_labels().values():
            combo_box.addItem(row[1])
        
        return combo_box
    
    def add_item_cbb(self, text):
        for cbb in self.comboBoxes:
            cbb.addItem(text)

    def combo_box_changed(self, index, combo_box):
        row = self.ui.tableWidget_2.indexAt(combo_box.pos())
        if row.isValid():
            row = row.row()

        # chưa có làm được cái lấy giá trị cbb cũ rồi fill nếu như không điền được tên
        self.ui.tableWidget_2.setCurrentCell(row, 0)  ## CHỖ NÀY KHÔNG CHẮC LẮM NẾU MÀ XÓA BỚT DÒNG THÌ CÁI ROW NÓ SAO
        file_id = int(self.ui.tableWidget_2.item(row, 0).text())
        if index == 0:
            text, ok = QInputDialog.getText(self, "Enter label Name", "Enter the new label name:")
            if ok:
                result = self.controller.add_label_to_database(text)
                if result[0]:
                    self.add_item_cbb(text)                                # thêm label mới vào cbb
                    combo_box.setCurrentIndex(combo_box.count() - 1)       # chuyển index về label mới thêm
                    label_id = result[1]                                     # lấy id của label mới thêm
                    self.controller.update_label_of_file(file_id, label_id)    # cập nhật label cho file
                else:
                    QMessageBox.warning(self, "Notification", "Tên label này đã tồn tại")
                    combo_box.setCurrentIndex(1)
            else:
                combo_box.setCurrentIndex(1)
        elif index == 1:
            self.controller.update_label_of_file(file_id, None)
        else: # lấy id theo index của cbb bằng list
            label_id = list(self.controller.get_labels().keys())[index-2]
            self.controller.update_label_of_file(file_id, label_id)

    def delete_item_cbb(self, name):
        index = self.comboBoxes[0].findText(name)
        for cbb in self.comboBoxes: 
            if not cbb:
                self.comboBoxes.remove(cbb)
                continue
            if cbb.currentIndex() == index :
                cbb.setCurrentIndex(1)
            cbb.removeItem(index)

    ### CONTEXT ###
    def contextMenuEvent(self, event):
        if self.ui.tableWidget_2.underMouse():
        # if self.ui.tableWidget_2.geometry().contains(event.globalPos()):
        # if self.ui.tableWidget_2.rect().contains(event.pos()):
            menu = QMenu(self)
            openInHere = menu.addAction("open in here")
            openByApp = menu.addAction("open by app") 
    
            action = menu.exec(self.mapToGlobal(event.pos()))

            if action == openInHere:
                id = int(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 0).text())
                path = self.controller.get_url_by_id_file(id)
                self.open_file_inside(QUrl.fromLocalFile(path), os.path.basename(path))
                
            elif action == openByApp:
                id = int(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 0).text())
                path = self.controller.get_url_by_id_file(id)
                if not os.path.exists(path):
                    print("File not found")
                    QMessageBox.warning(self, "Notification", "File not exists")
                os.startfile(path)
        
    ### MỞ FILE TRONG TAB MỚI ###
    def open_file_inside(self, qurl=None, label="blank"):
        open_tab_count = self.ui.tabWidget_2.count()

        # kiểm tra nếu tab đã được mở
        for i in range (open_tab_count):
            tab_name = self.ui.tabWidget_2.tabText(i)
            if tab_name == label:
                self.ui.tabWidget_2.setCurrentIndex(i)
                return

        # kiểm tra đường dẫn có trống không
        if qurl is None:
            qurl = QUrl("http://www.google.com")

        # load the url
        web = QWebEngineView()

        # enable plugins
        web.settings().setAttribute(web.settings().WebAttribute.PluginsEnabled, True)
        # enable pdf viewer
        # web.setting().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        web.settings().setAttribute(web.settings().WebAttribute.PdfViewerEnabled, True)

        web.setUrl(qurl)

        # hiển thị tab
        i = self.ui.tabWidget_2.addTab(web, label)
        self.ui.tabWidget_2.setCurrentIndex(i)

    ### ĐÓNG TAB ####
    def close_tab(self, index):
        if index == 0:
            return
        self.ui.tabWidget_2.removeTab(index)

    ### XÓA FILE BẰNG BTN TRONG TABLE ###
    def delete_file(self, id):
        button = self.sender()
        index = self.ui.tableWidget_2.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            self.ui.tableWidget_2.setCurrentCell(row, 0)
        else:
            return
            
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
            self.controller.delete_file(id)
            if self.ui.info_right.expanded:
                self.ui.info_right.collapseMenu()
            selected_row = self.ui.tableWidget_2.currentRow()
            if selected_row >= 0:
                self.ui.tableWidget_2.removeRow(selected_row)
        else:
            return

    ### SET PRIORITY ###
    def set_priority(self, id):
        checkbox = self.sender()
        index = self.ui.tableWidget_2.indexAt(checkbox.pos())
        if index.isValid():
            row = index.row()
            self.ui.tableWidget_2.setCurrentCell(row, 0)

        if checkbox.isChecked():
            self.controller.update_priority_of_file(id, 1)
        else:
            self.controller.update_priority_of_file(id, 0)

        self.load_table()

    def sort_table(self):
        current_index = self.ui.comboBox.currentIndex()
    
        if current_index == 1:  # A - Z
            self.ui.tableWidget_2.sortItems(1, Qt.SortOrder.AscendingOrder)
        elif current_index == 2:  # Z - A
            self.ui.tableWidget_2.sortItems(1, Qt.SortOrder.DescendingOrder)
        elif current_index == 3:  # Date ->
            self.ui.tableWidget_2.sortItems(1, Qt.SortOrder.AscendingOrder)
        elif current_index == 4:  # Date <-
            self.ui.tableWidget_2.sortItems(1, Qt.SortOrder.DescendingOrder)
        elif current_index == 5:  # Size ->
            self.ui.tableWidget_2.sortItems(3, Qt.SortOrder.AscendingOrder)
        elif current_index == 6:  # Size <-
            self.ui.tableWidget_2.sortItems(3, Qt.SortOrder.DescendingOrder)

    def load_cbb(self):
        self.ui.new_tag_cbb.addItem("(+)")
        self.ui.new_tag_cbb.addItem("")
        for value in self.controller.get_tags().values():
            self.ui.new_tag_cbb.addItem(value[1])
        self.ui.new_tag_cbb.setCurrentIndex(1)

    def new_tag_cbb_changed(self):
        if self.ui.new_tag_cbb.currentText() == "(+)":
            text, ok = QInputDialog.getText(self, "Enter tag Name", "Enter the new tag name:")
            if ok:
                result = self.controller.add_tag_to_database(text)
                if result[0]:
                    self.ui.new_tag_cbb.addItem(text)
                    self.ui.new_tag_cbb.setCurrentIndex(self.ui.new_tag_cbb.count() - 1)
                else:
                    QMessageBox.warning(self, "Notification", "Tag name already exists")
                    self.ui.new_tag_cbb.setCurrentIndex(1)
            else:
                self.ui.new_tag_cbb.setCurrentIndex(1)

    def tag_widget(self):
        if self.ui.new_tag_wg.layout() is None:
            self.layout = QGridLayout()
            self.layout.setContentsMargins(0, 0, 0, 0)
            # self.layout.setSpacing(14)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.ui.new_tag_wg.setLayout(self.layout)
        else:
            for i in range(self.layout.count()):
                self.layout.itemAt(i).widget().deleteLater()
        print(self.row_focus[0])
        self.frames = []
        id = self.row_focus[0]
        self.add_new_frame(self.controller.get_files_tags(id))

    def add_new_frame(self, list = None):
        print("list",list)
        if list:
            # print("1")
            for i, tag in enumerate(list.values()):
                new_frame = self.create_frame(self.controller.get_tags()[tag[2]][1])
                row = i // 2 + 1
                col = i % 2
                self.layout.addWidget(new_frame, row, col)
                self.frames.append(new_frame)
                new_frame.setMaximumWidth(88)
                new_frame.setMinimumWidth(88)
                
        elif self.ui.new_tag_cbb.currentText() == "":
            # print("2")
            return
        
        else:
            print("3")
            # print(self.row_focus[0], self.ui.new_tag_cbb.currentText())
            result = self.controller.add_file_tag_to_database(self.row_focus[0], self.ui.new_tag_cbb.currentText())
            if not result[0]:
                QMessageBox.warning(self, "Notification", "Tag name already exists in this file")
                self.ui.new_tag_cbb.setCurrentIndex(1)
                return
            new_frame = self.create_frame(self.ui.new_tag_cbb.currentText())
            row = len(self.frames) // 2 + 1
            col = len(self.frames) % 2
            self.layout.addWidget(new_frame, row, col)
            self.frames.append(new_frame)
            new_frame.setMaximumWidth(88)
            new_frame.setMinimumWidth(88)
        

    def create_frame(self, text):
        frame = QWidget()
        frame.setObjectName("frm_tag")
        frame.setStyleSheet(
            """ #frm_tag {
                    border-radius: 10px;
                    border: 2px solid #6272a4;
                } 
            """
            )
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(text)
        label.setStyleSheet(
            """ 
                background-color: transparent;
            """
            )
        
        button = QPushButton()
        button.setStyleSheet(
            """ 
                background-color: transparent;
                border: none;
            """
            )
        button.setMaximumSize(QtCore.QSize(23, 23))
        button.setMinimumSize(QtCore.QSize(23, 23))
        button.clicked.connect(lambda: self.remove_frame(frame, text))
        button.setIcon(QtGui.QIcon("Qss/icons/000000/feather/window_close.png"))
        button.setIconSize(QtCore.QSize(8, 8))

        spacer_item = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout.addWidget(label, 0, 0)
        layout.addItem(spacer_item, 0, 1)
        layout.addWidget(button, 0, 2)

        frame.setLayout(layout)
        return frame
    

    def remove_frame(self, frame, text):
        self.layout.removeWidget(frame)
        frame.deleteLater()
        self.frames.remove(frame)
        
        self.controller.delete_file_tag(self.row_focus[0], self.controller.get_tag_id_by_name(text))

        for index, f in enumerate(self.frames):
            row = index // 2 + 1
            col = index % 2
            self.layout.addWidget(f, row, col)

        self.ui.new_tag_wg.adjustSize()    