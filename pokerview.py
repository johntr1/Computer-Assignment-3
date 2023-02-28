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
    def __init__(self, player):
        super().__init__()
        self.player = player  # player is player name
        layout = QVBoxLayout()
        player_turn = QLabel()
        player_turn.setText(self.player)
        layout.addWidget(player_turn)
        self.setLayout(layout)


class PokerButtons(QGroupBox):
    def __init__(self):
        super().__init__()

        button = QPushButton('Check')
        layout = QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(QPushButton('Bet'))
        layout.addWidget(QPushButton('Fold'))
        self.setLayout(layout)


class PokerBoardView(QWidget):
    def __init__(self, poker):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)


class PokerView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        layout.addWidget(PlayerView(player), 2, 3, 1, 2)
        layout.addWidget(PokerButtons(),0,1)

        phbox = QHBoxLayout()
        phbox.addWidget(PokerButtons())

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("CA3 Group 19")
        status = QStatusBar()
        status.addWidget(PlayerView(player))
        self.setStatusBar(status)

        # Menu Bars
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        # Tool bars
        toolbar = QToolBar("Poker Actions")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)


player = "John"

"""
app = QApplication(sys.argv)
import sys

window = MainWindow(app)
window.show()
app.exec_()
"""

app = QApplication(sys.argv)
window = PokerView()
window.show()
app.exec_()