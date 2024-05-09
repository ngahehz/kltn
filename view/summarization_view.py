from PyQt6.QtWidgets import QWidget

from src.ui_page_summarization import Ui_Form
from controller.helper import summarizer

class Summarization(QWidget):
    def __init__(self):
        super(Summarization, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.sum_btn.clicked.connect(self.generate_summary)
        self.ui.del_sum_btn.clicked.connect(self.del_sum1)

    def del_sum1(self):
        self.ui.sum1_txt.clear()
        self.ui.sum2_txt.clear()

    def generate_summary(self):
        contents = self.ui.sum1_txt.toPlainText()
        summary = summarizer(contents)
        self.ui.sum2_txt.setPlainText(summary)