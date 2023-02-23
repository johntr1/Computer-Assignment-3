from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import sys

qt_app = QApplication(sys.argv)


class TheTable(QWidget):  # A group box might be nice here, lets of but a border and title around the widgets!
    def __init__(self):
        super().__init__()  # Call the QWidget initialization as well!

        call_button = QPushButton("Call")
        fold_button = QPushButton("Fold")
        raise_button = QPushButton("Raise")


        gbox = QHBoxLayout()
        gbox.addWidget(call_button)
        gbox.addWidget(fold_button)
        gbox.addWidget(raise_button)
        gbox.addLayout(gbox)


        self.setLayout(gbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('The Table')


win = TheTable()
win.show()
qt_app.exec_()








