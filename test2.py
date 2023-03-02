from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cardsview import CardsView
from cardlib import *
from cardsmodel import HandModel
import sys

qt_app = QApplication(sys.argv)

data = ["one", "two", "three", "four", "five"]

model = QStringListModel(data)
# We can hook in anything
# model.dataChanged.connect(lambda idx: print("The data was modified!", idx.row()))
"""
combobox = QComboBox()
combobox.setModel(model)
combobox.show()
"""
listView = QListView()
listView.setModel(model)
listView.show()

qt_app.exec_()

print(model)
