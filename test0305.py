import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class AutoResizeTableWidget(QTableWidget):
    def __init__(self, *args):
        super(AutoResizeTableWidget, self).__init__(*args)
        self.setWordWrap(True)
        self.cellChanged.connect(self.adjustRowHeight)

    def adjustRowHeight(self):
        for row in range(self.rowCount()):
            max_height = 0
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item:
                    # Calculate the height needed for the content
                    item_height = self.getItemHeight(item)
                    if item_height > max_height:
                        max_height = item_height
            # Set the row height
            self.setRowHeight(row, max_height)

    def getItemHeight(self, item):
        # Create a widget with the same text and font as the item
        text = item.text()
        font = item.font()
        option = self.viewOptions()
        option.font = font

        # Calculate the required height based on the text and the widget's width
        rect = self.visualItemRect(item)
        doc = self.createDocument(text, font, rect.width())
        doc_height = doc.size().height()
        
        # Add some padding
        padding = 10
        return doc_height + padding

    def createDocument(self, text, font, width):
        from PyQt5.QtGui import QTextDocument
        doc = QTextDocument()
        doc.setDefaultFont(font)
        doc.setTextWidth(width)
        doc.setPlainText(text)
        return doc

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.table = AutoResizeTableWidget(5, 3)  # 5 rows and 3 columns

        # Example content
        content = [
            ["Short text", "Another short text", "Yet another short text"],
            ["A longer piece of text that should wrap to the next line if the column is not wide enough.", 
             "Short text", "Another short text"],
            ["Short text", "Another short text", 
             "A very long piece of text that should cause the cell height to increase significantly when it wraps to multiple lines."],
            ["Short text", "Another short text", "Yet another short text"],
            ["Short text", "Another short text", "Yet another short text"]
        ]

        for row in range(5):
            for column in range(3):
                item = QTableWidgetItem(content[row][column])
                self.table.setItem(row, column, item)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.setWindowTitle('Auto-Resizing QTableWidget')
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
