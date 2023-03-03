from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *




# Community_Card Changes
# Player Turn
# Player Winner
# Game Winner

#en call vid river avslutar ronden

class Player():
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.money = 10000
        self.player_pot = 0

    def create_new_hand(self):  # Kanske att handen ska skapas i init
        self.hand = Hand()
        return self.hand

    def get_name(self):
        return self.name

    def get_player_pot(self):
        return self.player_pot

    def change_player_pot(self, amount):
        self.player_pot = self.player_pot + amount

    def reset_player_pot(self):
        self.player_pot = 0

    def check_money(self):
        return self.money

    def change_money(self, amount):
        self.money = self.money + amount

    def poker_hand_value(self, community_cards):
        return self.hand.best_poker_hand(community_cards.cards)


class TexasHoldEm(QObject):
    warning = pyqtSignal(str,)
    update_turn = pyqtSignal()
    update_value = pyqtSignal()
    p_winner = pyqtSignal()
    g_winner = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.players = []
        self.active_players = []
        self.player_turn = 0
        self.big_blind_player = 0
        self.raiser = 0
        self.pot = 0
        self.deck = []
        self.community_cards = Hand()
        self.round_counter = 0
        self.call_counter = 0

        # start the gui and for players and names
        # put the 2 players in the self.players list

        self.players.append(Player('John'))
        self.players.append(Player('Martin'))
        for i in range(len(self.players)):
            self.active_players.append(1)
        self.hand_out_cards()
        self.big_and_little_blind()
        self.update_turn.emit()

    def reset_pot(self):
        print(f'{self.players[0].check_money()} has money John')
        print(f'{self.players[1].check_money()} has money martin')
        if not self.check_game():
            print('game winner')
            self.game_winner()

        for player in self.players:
            player.reset_player_pot()

        self.big_blind_player = (self.big_blind_player + 1) % len(self.players)
        self.pot = 0
        self.round_counter = 0

        self.hand_out_cards()
        self.big_and_little_blind()

    def hand_out_cards(self):
        self.deck = StandardDeck()
        self.deck.shuffle()
        # reset in_pot to 0 for all players
        for i, player in enumerate(self.players):
            if self.active_players[i] == 0:  # Only gives cards to active players
                continue
            hand = player.create_new_hand()
            for j in range(2):
                hand.add_card(self.deck.draw())

    def big_and_little_blind(self):
        for i in range(len(self.active_players)):  # checks if the big blind player is active
            if self.active_players[(self.big_blind_player + i) % len(self.active_players)] == 1:
                self.big_blind_player = (self.big_blind_player + i) % len(self.active_players)
                break

        # big blind
        amount = 100
        self.pot = self.pot + amount
        self.players[self.big_blind_player].change_player_pot(amount)
        self.players[self.big_blind_player].change_money(-amount)

        # small blind
        amount = 50
        self.pot = self.pot + amount
        self.players[(self.big_blind_player - 1) % len(self.active_players)].change_player_pot(amount)
        self.players[(self.big_blind_player - 1) % len(self.active_players)].change_money(-amount)

    def check_round(self):
        if self.call_counter > len(self.players):
            self.round_counter += 1
            self.round()

    def round(self):
        if self.round_counter == 1:
            self.community_cards.add_card(self.deck.draw())
            self.community_cards.add_card(self.deck.draw())
            self.community_cards.add_card(self.deck.draw())
        elif self.round_counter == 2:
            self.community_cards.add_card(self.deck.draw())
        elif self.round_counter == 3:
            self.community_cards.add_card(self.deck.draw())
            print(self.community_cards.cards)
        elif self.round_counter == 4:
            self.showdown()
        else:
            print('too high round number')

    def showdown(self):
        best_poker_hands_list = []

        for player in self.players:
            best_poker_hands_list.append(player.poker_hand_value(self.community_cards))
        for i in range(2):
            print(self.players[i].hand.cards[0])
            print(self.players[i].hand.cards[1])

        best_hand_index = best_poker_hands_list.index(max(best_poker_hands_list))
        print(best_hand_index)

        for i in range(len(self.active_players)):
            self.active_players[i] = 0
        self.active_players[best_hand_index] = 1
        self.pot_winner()

    def check_play(self):
        if sum(self.active_players) <= 1:
            return False
        else:
            return True

    def check_game(self):
        list = []

        for player in self.players:  # checks if more than one person has money
            if not player.check_money() == 0:
                list.append(1)
        if sum(list) <= 1:
            return False
        else:
            return True

    def call(self):
        index = (self.player_turn - 1) % len(self.active_players)
        if self.players[index].get_player_pot() > self.players[self.player_turn].get_player_pot():  # if the player before has more in the pot
            diff = self.players[index].get_player_pot() - self.players[self.player_turn].get_player_pot()
            self.pot = self.pot + diff
            self.players[self.player_turn].change_player_pot(diff)
            self.players[self.player_turn].change_money(-diff)

        print(f'{self.players[self.player_turn].get_name()} has called.')
        self.call_counter += 1
        self.next_turn()
        self.check_round()

    def poker_raise(self, amount):
        if self.players[self.player_turn].check_money() == 0:
            self.call()
            return
        print(f'{self.players[self.player_turn].check_money()} has money {self.players[self.player_turn].get_name()}')


        if amount > self.players[self.player_turn].check_money() or amount <= 0:
            self.warning.emit('Not a valid raise')
        else:
            self.pot = self.pot + amount
            self.players[self.player_turn].change_player_pot(amount)
            self.players[self.player_turn].change_money(-amount)
            self.raiser = self.player_turn

            print(f'{self.players[self.player_turn].get_name()} has raised with ${amount}.')
            self.call_counter = 0
            self.next_turn()

    def fold(self):
        if self.players[self.player_turn].check_money() == 0:
            self.call()
            return
        self.remove_active_player()
        print(f'{self.players[self.player_turn].name} has folded.')
        self.pot_winner()

    def next_turn(self):
        self.player_turn = (self.player_turn + 1) % len(self.active_players)
        print(f'It is {self.players[self.player_turn].get_name()} turn, you have ${self.players[self.player_turn].check_money()}')
        self.update_turn.emit()

    def all_in(self):
        if self.round_counter == 0:
            print('the')

    def remove_active_player(self):
        self.active_players[self.player_turn] = 0

    def pot_winner(self):

        winner_index = self.active_players.index(1)
        player_winner = self.players[winner_index]
        if player_winner.get_player_pot() * 2 < self.pot:
            player_winner.change_money(player_winner.get_player_pot() * 2)
        else:
            player_winner.change_money(self.pot)

        print(f'the winner of the pot is {self.players[winner_index].name}')
        self.reset_pot()

    def game_winner(self):

        for i, player in enumerate(self.players):  # checks who has the money
            if not player.check_money() == 0:
                print(f'The winner of the game is {player.get_name()}')
                self.g_winner
                return i



t = TexasHoldEm()

#for i in range(2):
t.poker_raise(9950)
t.poker_raise(9900)

for i in range(6):
    t.call()
