from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class PlayerView(QGroupBox):
    def __init__(self, num, player):
        super().__init__()




app = QApplication([])
app.setStyle('Fusion')

layout = QHBoxLayout()
layout.addWidget(QPushButton('Check'))
layout.addWidget(QPushButton('Bet'))
layout.addWidget(QPushButton('Fold'))

window = QWidget()
window.setLayout(layout)
window.show()
app.exec()