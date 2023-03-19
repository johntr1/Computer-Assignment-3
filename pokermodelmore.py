from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *


# vad händer om en person raisear mer än vad du har
# rasieing problemet med


class Player:
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
        if self.money < 0:
            print('No money')  # ha ett stop här eller någon annanstans

    def poker_hand_value(self, community_cards):
        return self.hand.best_poker_hand(community_cards.cards)


class TexasHoldEm:
    def __init__(self):
        self.players = []
        self.active_players = []
        self.player_turn = 0
        self.big_blind_player = 0
        self.raiser = 0
        self.pot = 0
        self.deck =[]
        self.community_cards = Hand()
        self.round_counter = 0

        # start the gui and for players and names
        # put the 2 players in the self.players list

        self.hand_out_cards()




        self.players.append(Player('John'))
        self.players.append(Player('Martin'))
        self.hand_out_cards()

        while True:  # While 2 people have money
            for player in self.players:
                player.reset_player_pot()

            for i in range(len(self.players)):  # Resets the active players
                self.active_players.append(1)

            for i, j in enumerate(self.players):  # If the player has no money she/he is not an active player
                if j.check_money() == 0:
                    self.active_players[i] = 0

            self.hand_out_cards()

            self.big_and_little_blind()

            if False == self.pre_flop():
                self.game_winner()
                continue

            community_cards = self.flop()
            if community_cards == False:
                self.game_winner()
                continue

            community_cards = self.turn(community_cards)

            if community_cards == False:
                self.game_winner()
                continue

            self.river(community_cards)
            if community_cards == False:
                self.game_winner()
                continue

            self.showdown(community_cards)

            self.pot_winner()

            self.big_blind_player = (1 + self.big_blind_player) % len(self.players)

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

    def pre_flop(self):
        self.player_turn = (self.big_blind_player + 1) % len(self.active_players)
        self.raiser = self.player_turn
        while True:

            if self.raiser == self.player_turn:
                break

        if not self.betting_round():
            return False
        return True

    def check_round(self):
        if self.round_counter == 1:
            self.community_cards.add_card(self.deck.draw())
            self.community_cards.add_card(self.deck.draw())
            self.community_cards.add_card(self.deck.draw())
        elif self.round_counter == 2:
            self.community_cards.add_card(self.deck.draw())
        elif self.round_counter == 3:
            self.community_cards.add_card(self.deck.draw())
        elif self.round_counter == 4:
            self.showdown()
        else:
            print('error')

    def flop(self):
        community_cards = Hand()
        for i in range(3):
            community_cards.add_card(self.deck.draw())
        # Show 3 community_cards
        print(community_cards.cards)
        if not self.betting_round():
            return False
        return community_cards

    def turn(self, community_cards):

        # show 1 community_card
        community_cards.add_card(self.deck.draw())
        print(community_cards.cards)
        if not self.betting_round():
            return False
        return community_cards


    def river(self, community_cards):
        # show 1 community_card
        community_cards.add_card(self.deck.draw())
        print(community_cards.cards)
        self.betting_round()
        if not self.betting_round():
            return False
        return community_cards

    def showdown(self, community_cards):
        best_poker_hands_list = []

        for index in self.active_players:
            if index == 1:
                best_poker_hands_list.append(self.players[index].poker_hand_value(community_cards))
            else:
                best_poker_hands_list.append(0)

        best_hand_index = best_poker_hands_list.index(max(best_poker_hands_list))
        # besthand = [i for i, x in enumerate(best_poker_hands_list) if x == max(a)]

        for i in range(len(self.active_players)):
            self.active_players[i] = 0
        self.active_players[best_hand_index] = 1

    def betting_round(self):
        player_turn = (self.big_blind_player + 1) % len(self.active_players)
        raiser = player_turn

        while True:

            for i in range(len(self.active_players)):  # checks if the turn_player is an active player
                if self.active_players[(player_turn + 1) % len(self.active_players)] == 1:
                    player_turn = (player_turn + i) % len(self.active_players)
                    break

            chosen = self.choose(self.players[player_turn])
            player_turn = player_turn + 1

            if chosen == 'fold':
                if not self.check_play():
                    return False

            if chosen == "raise":
                raiser = player_turn

            if raiser == player_turn:
                break
        return True

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

    def choose(self, player):
        print(f'What do you want to do? {player.name} You have ${player.money}')
        while True:
            inp = input('What do you want ')
            if inp == 'call':
                self.call(player)
                return None
            elif inp == 'raise':
                self.poker_raise(player)
                return "raise"
            elif inp == 'fold':
                self.fold(player)
                return 'fold'

    def call(self):
        index = (self.player_turn - 1) % len(self.active_players)
        if self.players[index].get_player_pot() > self.player_turn.get_player_pot():  # if the player before has more in the pot
            diff = self.players[index].get_player_pot() - self.player_turn.get_player_pot()
            self.pot = self.pot + diff
            self.player_turn.change_player_pot(diff)
            self.player_turn.change_money(-diff)

            checc
        print(f'{self.players[self.player_turn].get_name()} has called.')

    def poker_raise(self, amount):
        # ask with the GUI how much should raise
        while True:
            amount = int(input('How much do you want to raise with?'))
            if type(amount) == int and amount <= player.money:
                break
            # GUI with an error saying to type in a whole number
            print('not enough money or not an int')  # with an GUI

        self.pot = self.pot + amount
        player.change_player_pot(amount)
        player.change_money(-amount)
        self.raiser = self.player_turn

        print(f'{self.players[self.player_turn].get_name()} has called.')

    def fold(self, player):

        self.remove_active_player(player)
        return 'fold'

    def remove_active_player(self, player):
        self.active_players[self.players.index(player)] = 0

    def pot_winner(self):

        winner_index = self.active_players.index(1)
        print(f'the winner of the pot is {self.players[winner_index].name}')
        return winner_index

    def game_winner(self):

        for i, player in enumerate(self.players):  # checks who has the money
            if not player.check_money() == 0:
                print(f'The winner of the game is {player.get_name()}')
                return i

    def reset_pot(self):


TexasHoldEm()
