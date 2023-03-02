from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cardsview import CardsView
from cardlib import *
from cardsmodel import HandModel
import sys


# QApplication
# QMainWindow
# QInputDialog
# QMessageBox
# QErrorMessage


class PlayerView(QGroupBox):
    def __init__(self, player, cards):
        super().__init__()
        self.player = player  # player is player name
        layout = QVBoxLayout()
        player_turn = QLabel()
        player_turn.setText(f"{self.player}s tur")
        #        layout.addWidget(player_turn)

        card_layout = QHBoxLayout()
        layout.addWidget(CardsView(cards, card_spacing=50))
        self.setLayout(layout)


class PokerButtons(QWidget):
    def __init__(self, cards):
        super().__init__()

        layout = QVBoxLayout()
        raise_button = QPushButton("Raise")
        raise_button.clicked.connect(self.get_input)
        layout.addWidget(raise_button)

        layout.addWidget(QPushButton('Call'))
        layout.addWidget(QPushButton('Fold'))
        fold_button = QPushButton('Flip')
        layout.addWidget(fold_button)
        fold_button.clicked.connect(cards.flip)
        self.setLayout(layout)

    def get_input(self):
        number, ok = QInputDialog.getInt(self, "Raise", "Enter a number")
        if ok:
            game.next_turn()
            return True


class PokerBoardView(QWidget):
    def __init__(self, table_cards):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(CardsView(table_cards, card_spacing=250))
        self.setLayout(layout)


class PokerView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        layout.addWidget(PlayerView(player, cards2), 3, 1)
        layout.addWidget(PokerButtons(cards2), 3, 0)
        layout.addWidget(PokerBoardView(cards), 0, 0, 2, 4)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("CA3 Group 19")
        self.setFixedHeight(700)
        self.setFixedWidth(850)
        self.setCentralWidget(PokerView())
        player_turn = QLabel("Johns tur")
        player_money = QLabel("")
        status = QStatusBar()
        status.addWidget(player_turn)
        status.addWidget(player_money)
        self.setStatusBar(status)
        # Menu Bars
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        # Tool bars
        toolbar = QToolBar("Poker Actions")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)


player = "John"

"""
app = QApplication(sys.argv)
import sys

window = MainWindow(app)
window.show()
app.exec()


# Runs all classes
class PokerView(QWidget):
    '
app.exec_()
"""
# deck = StandardDeck()
hand = Hand()
hand.add_card(NumberedCard(2, Suit.Spades))
hand.add_card(KingCard(Suit.Spades))
hand.add_card(NumberedCard(2, Suit.Spades))
hand.add_card(KingCard(Suit.Spades))
hand.add_card(KingCard(Suit.Spades))
# hand.add_card(NumberedCard(2, Suit.Spades))

cards = HandModel(hand.cards)

hand2 = Hand()

hand2.add_card(NumberedCard(2, Suit.Spades))
hand2.add_card(KingCard(Suit.Spades))
cards2 = HandModel(hand2.cards)

app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
app.exec_()
