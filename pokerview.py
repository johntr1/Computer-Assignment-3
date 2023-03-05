from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cardsview import CardsView
from cardlib import *
from cardsmodel import HandModel
from pokermodel import *
import sys


# QApplication
# QMainWindow
# QInputDialog
# QMessageBox
# QErrorMessage


class PlayerView(QGroupBox):
    def __init__(self, game):
        super().__init__()
        self.game = game
        #      self.player = player  # player is player name
        layout = QVBoxLayout()
        #       player_turn = QLabel()
        #      player_turn.setText(f"{self.player}s tur")
        #    layout.addWidget(player_turn)
        layout.addWidget(CardsView(self.game.player_cards, card_spacing=50))
        self.setLayout(layout)


class PokerButtons(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        layout = QVBoxLayout()
        player_cards = self.game.player_cards
        print(player_cards)
        raise_button = QPushButton("Raise")
        raise_button.clicked.connect(self.get_input)
        layout.addWidget(raise_button)

        call_button = QPushButton("Call")
        call_button.clicked.connect(self.game.call)
        layout.addWidget(call_button)

        fold_button = QPushButton("Fold")
        fold_button.clicked.connect(self.game.fold)
        layout.addWidget(fold_button)

        flip_button = QPushButton('Flip')
        layout.addWidget(flip_button)
        flip_button.clicked.connect(player_cards.flip)
        self.setLayout(layout)

    def get_input(self):
        number, ok = QInputDialog.getInt(self, "Raise", "Enter a number")
        if ok:
            self.game.poker_raise(number)


class PokerBoardView(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.layout = QHBoxLayout(self)
        self.card_view = CardsView(HandModel(self.game.community_cards.cards), card_spacing=250)
        self.layout.addWidget(self.card_view)
        self.setLayout(self.layout)
        self.game.update_round.connect(self.update_cards)

    def update_value(self):
        self.card_view.update_view()

    def update_cards(self):
        self.layout.removeWidget(self.card_view)
        self.card_view.deleteLater()
        self.card_view = CardsView(self.game.community_cards_model, card_spacing=250)
        self.layout.addWidget(self.card_view)



class InformationBox(QWidget):
    def __init__(self, game):
        super().__init__()
        layout = QVBoxLayout()
        # Lägg till layouts:
        # Motståndarens pengar
        # Hur mycket är i potten
        # Vad motståndaren har ökat med


class PokerView(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game

        layout = QGridLayout()

        layout.addWidget(PlayerView(game), 3, 1)
        layout.addWidget(PokerButtons(game), 3, 0)
        layout.addWidget(PokerBoardView(game), 0, 0, 2, 4)
        self.setLayout(layout)

        self.game.warning.connect(self.alert_warning)

    def alert_warning(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()


class MainWindow(QMainWindow):
    def __init__(self, app, game):
        super().__init__()
        self.game = game
        self.app = app
        self.setWindowTitle("CA3 Group 19")
        self.setFixedHeight(700)
        self.setFixedWidth(850)
        self.setCentralWidget(PokerView(game))

        player_money = QLabel("")
        status = QStatusBar()

        # Menu Bars
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        # Tool bars
        toolbar = QToolBar("Poker Actions")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Connect signals
        self.game.update_turn.connect(self.update_player_turn_label)
        # self.game.update_value.connect(self.update_values)
        # self.game.p_winner.connect(self.pot_winner)
        # self.game.g_winner.connect(self.game_winner)

        self.player_turn = QLabel(f'{self.game.players[self.game.player_turn].get_name()}s tur')
        status.addWidget(self.player_turn)
        status.addWidget(player_money)
        self.setStatusBar(status)

    def update_player_turn_label(self):
        self.player_turn.setText(f'{self.game.players[self.game.player_turn].get_name()}s tur')


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
hand.add_card(NumberedCard(2, Suit.Hearts))
hand.add_card(KingCard(Suit.Spades))
hand.add_card(NumberedCard(2, Suit.Clubs))
hand.add_card(KingCard(Suit.Diamonds))
hand.add_card(KingCard(Suit.Spades))
# hand.add_card(NumberedCard(2, Suit.Spades))

cards = HandModel(hand.cards)

hand2 = Hand()

hand2.add_card(NumberedCard(2, Suit.Spades))
hand2.add_card(KingCard(Suit.Spades))
cards2 = HandModel(hand2.cards)

app = QApplication(sys.argv)

game = TexasHoldEm()

window = MainWindow(app, game)
window.show()
app.exec_()
