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
        layout.addWidget(player_turn)

        card_layout = QHBoxLayout()
        hand = HandModel(cards.cards)
        layout.addWidget(CardsView(hand, card_spacing=50))
        self.setLayout(layout)


class PokerButtons(QGroupBox):
    def __init__(self, cards):
        super().__init__()

        button = QPushButton('Check')
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(QPushButton('Bet'))
        layout.addWidget(QPushButton('Fold'))
        fold_button = QPushButton('Flip')
        layout.addWidget(fold_button)
        hand = HandModel(cards.cards)
        fold_button.clicked.connect(hand.flip)
        self.setLayout(layout)


class PokerBoardView(QWidget):
    def __init__(self, table_cards):
        super().__init__()
        layout = QHBoxLayout()
        hand = HandModel(table_cards.cards)
        layout.addWidget(CardsView(hand, card_spacing=250))
        self.setLayout(layout)


class PokerView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        layout.addWidget(PlayerView(player, hand), 3, 1)
        layout.addWidget(PokerButtons(cards), 3, 0)
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
        status = QStatusBar()
        status.addWidget(player_turn)
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
cards = hand

hand2 = Hand()

hand2.add_card(NumberedCard(2, Suit.Spades))
hand2.add_card(KingCard(Suit.Spades))
hand = hand2

app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
app.exec_()
