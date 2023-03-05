from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cardsview import CardsView
from cardlib import *
from cardsmodel import HandModel
from pokermodel import *
import sys

class PlayerView(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        #      self.player = player  # player is player name
        self.layout = QVBoxLayout()
        self.card_view = CardsView(self.game.player_cards_list[self.game.player_turn], card_spacing=50)
        #       player_turn = QLabel()
        #      player_turn.setText(f"{self.player}s tur")
        #    layout.addWidget(player_turn)
        self.layout.addWidget(self.card_view)

        self.setLayout(self.layout)

        self.game.update_turn.connect(self.update_cards)

    def update_cards(self):
        self.layout.removeWidget(self.card_view)
        self.card_view.deleteLater()
        self.card_view = CardsView(self.game.player_cards_list[self.game.player_turn], card_spacing=50)
        self.layout.addWidget(self.card_view)


class PokerButtons(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.layout = QVBoxLayout()

        self.raise_button = QPushButton("Raise")
        self.raise_button.clicked.connect(self.get_input)
        self.layout.addWidget(self.raise_button)

        self.call_button = QPushButton("Call")
        self.call_button.clicked.connect(self.game.call)
        self.layout.addWidget(self.call_button)

        self.fold_button = QPushButton("Fold")
        self.fold_button.clicked.connect(self.game.fold)
        self.layout.addWidget(self.fold_button)

        self.flip_button = QPushButton('Flip')
        self.layout.addWidget(self.flip_button)
        self.flip_button.clicked.connect(self.game.player_cards_list[self.game.player_turn].flip)

        self.setLayout(self.layout)

        self.game.update_turn.connect(self.update_flip)

    def update_flip(self):
        idx = self.layout.indexOf(self.flip_button)
        self.layout.removeWidget(self.flip_button)
        self.flip_button.deleteLater()
        self.flip_button = QPushButton('Flip')
        self.layout.insertWidget(idx, self.flip_button)
        self.flip_button.clicked.connect(self.game.player_cards_list[self.game.player_turn].flip)

    def get_input(self):
        number, ok = QInputDialog.getInt(self, "Raise", "Enter a number")
        if ok:
            self.game.poker_raise(number)


class PokerBoardView(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.layout = QHBoxLayout(self)
        self.card_view = CardsView(self.game.community_cards_model, card_spacing=240)
        self.layout.addWidget(self.card_view)
        self.setLayout(self.layout)
        self.game.update_round.connect(self.update_cards)

    def update_cards(self):
        # Inspired by internet
        self.layout.removeWidget(self.card_view)
        self.card_view.deleteLater()
        self.card_view = CardsView(self.game.community_cards_model, card_spacing=240)
        self.layout.addWidget(self.card_view)


class InformationBox(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.layout = QVBoxLayout()
        self.player_pot = QLabel(f"My money in the pot: {self.game.players[self.game.player_turn].player_pot}")

        self.total_pot = QLabel(f"Total pot: {self.game.pot}")
        self.opponent_money = QLabel(f"Opponent's total money: {self.game.players[self.game.player_turn - 1].money}")
        self.opponent_pot = QLabel(
            f"Opponent's money in the pot: {self.game.players[self.game.player_turn - 1].player_pot}")

        self.layout.addWidget(self.total_pot)
        self.layout.addWidget(self.player_pot)
        self.layout.addWidget(self.opponent_pot)
        self.layout.addWidget(self.opponent_money)

        self.game.update_turn.connect(self.update_information)
        self.setLayout(self.layout)

    def update_information(self):
        self.total_pot.setText(f"Total pot: {self.game.pot}")

        self.player_pot.setText(f"My money in the pot: {self.game.players[self.game.player_turn].player_pot}")
        self.opponent_pot.setText(
            f"Opponent's money in the pot: {self.game.players[self.game.player_turn - 1].player_pot}")
        self.opponent_money.setText(f"Opponent's total money: {self.game.players[self.game.player_turn - 1].money}")

class PokerView(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game

        layout = QGridLayout()

        layout.addWidget(PlayerView(game), 3, 1)
        layout.addWidget(PokerButtons(game), 3, 0)
        layout.addWidget(PokerBoardView(game), 0, 0, 2, 3)
        layout.addWidget(InformationBox(game), 3, 2)
        self.setLayout(layout)

        self.game.pop_up.connect(self.pop_up_window)

    def pop_up_window(self, text: str):
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
        self.setFixedWidth(1000)
        self.setCentralWidget(PokerView(game))

        status = QStatusBar()

        # Tool bars
        toolbar = QToolBar("Poker Actions")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Connect signals
        self.game.update_turn.connect(self.update_player_turn_label)
        # self.game.update_value.connect(self.update_values)
        # self.game.p_winner.connect(self.pot_winner)
        # self.game.g_winner.connect(self.game_winner)

        self.player_turn = QLabel(f"{self.game.players[self.game.player_turn].get_name()}'s turn,")
        status.addWidget(self.player_turn)

        self.player_money = QLabel(f'Current money: ${self.game.players[self.game.player_turn].money}')
        status.addWidget(self.player_money)

        self.setStatusBar(status)

        self.game.quit.connect(self.quit_window)

    def update_player_turn_label(self):
        self.player_turn.setText(f"{self.game.players[self.game.player_turn].get_name()}'s turn, ")
        self.player_money.setText(f'current money: ${self.game.players[self.game.player_turn].money}')

    def quit_window(self):
        app.quit()
