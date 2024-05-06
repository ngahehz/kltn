import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit, QSizePolicy
from summa import summarizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tóm tắt văn bản")
        self.setGeometry(100, 100, 400, 400)

        self.text_edit = QPlainTextEdit()
        self.summary_label = QLabel("Tóm tắt văn bản sẽ được hiển thị ở đây")

        self.open_button = QPushButton("Mở file")
        self.open_button.clicked.connect(self.open_file)

        self.summary_button = QPushButton("Tóm tắt")
        self.summary_button.clicked.connect(self.generate_summary)

        self.summary_text_edit = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.summary_button)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.summary_text_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn file", "", "Text Files (*.txt)")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
                self.text_edit.setPlainText(contents)

    def generate_summary(self):
        contents = self.text_edit.toPlainText()
        summary = summarizer.summarize(contents)
        self.summary_text_edit.setPlainText(summary)
        # self.summary_label.setText(summary)


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())