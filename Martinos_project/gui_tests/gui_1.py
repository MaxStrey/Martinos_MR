import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QCheckBox, QListWidget
from random import choice

window_titles = [
    'My app',
    'My app',
    'Still my app',
    'Still my app',
    'This is surprising',
    'This is surprising!',
    'Something went wrong',
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        widget = QListWidget()
        widget.addItems(["One", "Two", "Three"])
        # In QListWidget there are two separate signals for the item, and the str
        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)
        self.setCentralWidget(widget)    
        
    def index_changed(self, current, previous):
        print(f"Current index: {current.row()}")

    def text_changed(self, text):
        print(f"Current text: {text}")

app = QApplication(sys.argv)

# Creating the window
window = MainWindow()
# window = QPushButton("Push me!")
window.show()

# Running the app
app.exec_()

