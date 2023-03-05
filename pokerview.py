from cardsview import CardsView
from pokermodel import *


class PlayerView(QWidget):
    # Create a view for the player cards
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Define layout
        self.layout = QVBoxLayout()

        # Add widgets
        
        self.card_view = CardsView(self.game.player_cards_list[self.game.player_turn], card_spacing=50)
        self.layout.addWidget(self.card_view)

        self.setLayout(self.layout)

        self.game.update_turn.connect(self.update_cards)

    def update_cards(self):
        self.layout.removeWidget(self.card_view)
        self.card_view.deleteLater()
        self.card_view = CardsView(self.game.player_cards_list[self.game.player_turn], card_spacing=50)
        self.layout.addWidget(self.card_view)


class PokerButtons(QWidget):
    # Creates a view for the buttons in the GUI
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Define layout
        self.layout = QVBoxLayout()

        # Add all buttons
        self.raise_button = QPushButton("Raise")
        self.raise_button.clicked.connect(self.get_input)
        self.layout.addWidget(self.raise_button)

        self.call_button = QPushButton("Call")
        self.call_button.clicked.connect(self.game.call)
        self.layout.addWidget(self.call_button)

        self.fold_button = QPushButton("Fold")
        self.fold_button.clicked.connect(self.game.fold)
        self.layout.addWidget(self.fold_button)

        # Add the flip button so that the players can hide their cards
        self.flip_button = QPushButton('Flip')
        self.layout.addWidget(self.flip_button)
        self.flip_button.clicked.connect(self.game.player_cards_list[self.game.player_turn].flip)

        self.setLayout(self.layout)

        # Signals for the flip
        self.game.update_turn.connect(self.update_flip)

    def update_flip(self):
        # Updates the widget depending player
        idx = self.layout.indexOf(self.flip_button)
        self.layout.removeWidget(self.flip_button)
        self.flip_button.deleteLater()
        self.flip_button = QPushButton('Flip')
        self.layout.insertWidget(idx, self.flip_button)
        self.flip_button.clicked.connect(self.game.player_cards_list[self.game.player_turn].flip)

    def get_input(self):
        # Calls on the poker_raise function if the player presses ok
        number, ok = QInputDialog.getInt(self, "Raise", "Enter a number")
        if ok:
            self.game.poker_raise(number)


class PokerBoardView(QWidget):
    # View for the table cards
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Define the layout
        self.layout = QHBoxLayout(self)
        # Add the widget by calling on CardsView
        self.card_view = CardsView(self.game.community_cards_model, card_spacing=240)
        self.layout.addWidget(self.card_view)
        self.setLayout(self.layout)

        # Signals
        self.game.update_round.connect(self.update_cards)

    def update_cards(self):
        # Updates the widget by quickly removing it and replacing it.
        self.layout.removeWidget(self.card_view)
        self.card_view.deleteLater()
        self.card_view = CardsView(self.game.community_cards_model, card_spacing=240)
        self.layout.addWidget(self.card_view)


class InformationBox(QWidget):
    # View with all necessary information to play poker
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Define layout
        self.layout = QVBoxLayout()

        # Adds all labels
        self.player_pot = QLabel(f"My money in the pot: {self.game.players[self.game.player_turn].player_pot}")
        self.total_pot = QLabel(f"Total pot: {self.game.pot}")
        self.opponent_money = QLabel(f"Opponent's total money: {self.game.players[self.game.player_turn - 1].money}")
        self.opponent_pot = QLabel(
            f"Opponent's money in the pot: {self.game.players[self.game.player_turn - 1].player_pot}")

        # Add the widgets to the layout
        self.layout.addWidget(self.total_pot)
        self.layout.addWidget(self.player_pot)
        self.layout.addWidget(self.opponent_pot)
        self.layout.addWidget(self.opponent_money)

        # Signals
        self.game.update_turn.connect(self.update_information)
        self.setLayout(self.layout)

    def update_information(self):
        # Updates the information if turn changes
        self.total_pot.setText(f"Total pot: {self.game.pot}")

        self.player_pot.setText(f"My money in the pot: {self.game.players[self.game.player_turn].player_pot}")
        self.opponent_pot.setText(
            f"Opponent's money in the pot: {self.game.players[self.game.player_turn - 1].player_pot}")
        self.opponent_money.setText(f"Opponent's total money: {self.game.players[self.game.player_turn - 1].money}")


class PokerView(QWidget):
    # This is the structure for the view. Uses grid layout to implement all the other views
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Define layout
        layout = QGridLayout()

        # Add all the widgets from other classes and position them accordingly
        layout.addWidget(PlayerView(game), 3, 1)
        layout.addWidget(PokerButtons(game), 3, 0)
        layout.addWidget(PokerBoardView(game), 0, 0, 2, 3)
        layout.addWidget(InformationBox(game), 3, 2)
        self.setLayout(layout)

        # Signals
        self.game.pop_up.connect(self.pop_up_window)

    @staticmethod
    def pop_up_window(self, text: str):
        # Creates a popup box if getting called by a signal
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()


class MainWindow(QMainWindow):
    # The main window for the GUI
    def __init__(self, app, game):
        super().__init__()
        self.game = game
        self.app = app

        # Sets the title and fixed height and width of the window
        self.setWindowTitle("CA3 Group 19")
        self.setFixedHeight(700)
        self.setFixedWidth(1000)

        # Implements the widgets from PokerView
        self.setCentralWidget(PokerView(game))

        # Status Bar
        status = QStatusBar()

        # Connect signals
        self.game.update_turn.connect(self.update_player_turn_label)

        # Add labels for the status bar
        self.player_turn = QLabel(f"{self.game.players[self.game.player_turn].get_name()}'s turn,")
        status.addWidget(self.player_turn)

        self.player_money = QLabel(f'Current money: ${self.game.players[self.game.player_turn].money}')
        status.addWidget(self.player_money)

        self.setStatusBar(status)

        # Signals
        self.game.quit.connect(self.quit_window)

    def update_player_turn_label(self):
        # Updates information depending on player turn
        self.player_turn.setText(f"{self.game.players[self.game.player_turn].get_name()}'s turn, ")
        self.player_money.setText(f'current money: ${self.game.players[self.game.player_turn].money}')

    def quit_window(self):
        # Quits the game if called by a signal
        self.app.quit()
