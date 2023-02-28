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



#en window som frågar om namn på 2 spelare
#en table som kan visa alla korten, sina pengar och motståndarens pengar. vad motståndaren har ökat med om de har ökat.
#vad potten ligger på. Namnen, raise, fold, call,
#en (pop up) för vad man vill raisea med och om man har skrivit in för mycket eller inte en siffra
#x won x money fönster för varje pot
#x won the game fönster när det bara är en person med pengar kvar

list = [1, 1, 0, 1]
alist = []
for i in range(len(list)):
    alist.append(1)

print(alist)
for i, j in enumerate(list):
    if j == 1:
        alist[i] = 0

print(alist)

