from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

qt_app = QApplication(sys.argv)


class TheTable(QWidget):  # A group box might be nice here, lets of but a border and title around the widgets!
    def __init__(self):
        super().__init__()  # Call the QWidget initialization as well!

        call_button = QPushButton("Call")
        fold_button = QPushButton("Fold")
        raise_button = QPushButton("Raise")


        gbox = QGridLayout()
        gbox.addWidget(call_button, 3,1)
        gbox.addWidget(fold_button,3 ,2)
        gbox.addWidget(raise_button, 3, 3)
        gbox.addLayout(gbox)


        self.setLayout(gbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('The Table')


win = TheTable()
win.show()
qt_app.exec_()








