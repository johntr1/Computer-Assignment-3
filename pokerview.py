from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


# QApplication
# QMainWindow
# QInputDialog
# QMessageBox
# QErrorMessage

class PlayerView(QGroupBox):
    def __init__(self, num, player):
        super().__init__()


app = QApplication([])
app.setStyle('Fusion')


def show_popup():
    msg = QMessageBox()
    msg.setWindowTitle("Set")
    msg.exec()


button = QPushButton('Check')
layout = QHBoxLayout()
layout.addWidget(button)
layout.addWidget(QPushButton('Bet'))
layout.addWidget(QPushButton('Fold'))

button.clicked.connect(show_popup())

window = QWidget()
window.setLayout(layout)
window.show()
app.exec()
