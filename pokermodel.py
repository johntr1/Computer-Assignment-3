# Author:
# John Tran
# Martin Diderholm
# Date: 05/03/2023
# Group 19

from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from cardsmodel import HandModel

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.money = 10000
        # How much money the player has in the pot
        self.player_pot = 0

    def drop_cards(self):
        self.hand.drop_all_cards()

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
    pop_up = pyqtSignal(str, ) #Signal for errors and winners
    update_turn = pyqtSignal() #Signal for the player view
    update_value = pyqtSignal() #Signal for the info view
    update_round = pyqtSignal()#Signal for the table view
    quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.players = []
        self.active_players = [] #The players that are active in the pot
        self.player_turn = 1
        self.big_blind_player = 0
        self.pot = 0
        self.deck = []
        self.community_cards = Hand()
        self.round_counter = 0
        self.call_counter = 0
        self.community_cards_model = HandModel([])
        self.folded = False

        self.players.append(Player('John')) # The names of the players
        self.players.append(Player('Martin'))

        for i in range(len(self.players)):
            self.active_players.append(1)
        self.player_cards_list = []
        for i in range(len(self.players)):
            self.player_cards_list.append(0)
        self.hand_out_cards()
        self.big_and_little_blind()

        self.player_cards = self.player_cards_list[self.player_turn]

        self.update_round.emit()
        self.update_value.emit()

    def reset_pot(self):
        if not self.check_game():
            self.game_winner()
            return

        for player in self.players:
            player.reset_player_pot()

        self.big_blind_player = (self.big_blind_player + 1) % len(self.players)
        self.player_turn = (self.big_blind_player + 1) % len(self.players)#So the player starting is after the big blind
        self.pot = 0
        self.round_counter = 0
        self.community_cards = Hand()
        self.community_cards_model = HandModel([])

        for i in range(len(self.players)):
            self.active_players[i] = 1

        self.hand_out_cards()
        self.big_and_little_blind()
        self.player_cards = self.player_cards_list[self.player_turn]
        self.update_turn.emit()
        self.update_round.emit()

    def hand_out_cards(self):# Creates a new deck and hands out cards to all the players
        self.deck = StandardDeck()
        self.deck.shuffle()

        for i, player in enumerate(self.players):
            if self.active_players[i] == 0:  # Only gives cards to active players
                continue
            player.drop_cards()
            print(player.hand.cards)
            for j in range(2):
                player.hand.add_card(self.deck.draw())
                print(player.hand.cards)
        for i in range(len(self.players)):
            print(self.players[i].hand.cards)
            player_cards = HandModel(self.players[i].hand.cards)
            self.player_cards_list[i] = player_cards

    def big_and_little_blind(self):

        # give out the big blind
        amount = 100
        self.pot = self.pot + amount
        self.players[self.big_blind_player].change_player_pot(amount)
        self.players[self.big_blind_player].change_money(-amount)

        #hands out the small blind
        amount = 50
        self.pot = self.pot + amount
        self.players[(self.big_blind_player - 1) % len(self.active_players)].change_player_pot(amount)
        self.players[(self.big_blind_player - 1) % len(self.active_players)].change_money(-amount)

    def check_round(self):
        #Keeps track if there are too many calls in a row and changes the round accordingly
        if self.call_counter >= len(self.players):
            self.call_counter = 0
            self.round_counter += 1
            self.round()

    def round(self): #Checks what round it and adds community cards of starts the showdown
                    #also emits  update_round
        if self.round_counter == 1:

            self.community_cards.add_card(self.deck.draw())
            self.community_cards_model.cards.append(self.community_cards.cards[-1])

            self.community_cards.add_card(self.deck.draw())
            self.community_cards_model.cards.append(self.community_cards.cards[-1])

            self.community_cards.add_card(self.deck.draw())
            self.community_cards_model.cards.append(self.community_cards.cards[-1])

            self.update_round.emit()
            print('Flop')
        elif self.round_counter == 2:
            self.community_cards.add_card(self.deck.draw())
            self.community_cards_model.cards.append(self.community_cards.cards[-1])
            self.update_round.emit()
            print('Turn')
        elif self.round_counter == 3:
            self.community_cards.add_card(self.deck.draw())
            self.community_cards_model.cards.append(self.community_cards.cards[-1])
            self.update_round.emit()
            print('River')
        elif self.round_counter == 4:
            print('Showdown')
            self.showdown()
        else:
            print('Too high round number')

    def showdown(self):#Checks a the poker hand values for all the players and changes the active player list
                        #so only the one with the best hand wins
        best_poker_hands_list = []

        for player in self.players:
            best_poker_hands_list.append(player.poker_hand_value(self.community_cards))

        best_hand_index = best_poker_hands_list.index(max(best_poker_hands_list))

        for i in range(len(self.active_players)):
            self.active_players[i] = 0
        self.active_players[best_hand_index] = 1
        self.pot_winner()
        self.update_turn.emit()

    def check_game(self): #check if there are more than 2 players that have money
        list = []

        for player in self.players:
            if not player.check_money() == 0:
                list.append(1)
        if sum(list) <= 1:
            return False
        else:
            return True

    def call(self): #

        index = (self.player_turn - 1) % len(self.active_players)
        if self.players[index].get_player_pot() > self.players[
            self.player_turn].get_player_pot():  # if the player before has more in the pot
            #Increase the call depending on how much more the other person has in the pot
            diff = self.players[index].get_player_pot() - self.players[self.player_turn].get_player_pot()
            if diff > self.players[self.player_turn].money: #If you dont have enough money you still call
                diff = self.players[self.player_turn].money
            self.pot = self.pot + diff
            self.players[self.player_turn].change_player_pot(diff)
            self.players[self.player_turn].change_money(-diff)

        print(f'{self.players[self.player_turn].get_name()} has called.')
        self.call_counter += 1
        self.check_round()
        self.next_turn()

    def poker_raise(self, amount):
        if self.players[self.player_turn].check_money() == 0:#if you don't have any money you just call instead
            self.call()
            return
        #The difference of the two player pots
        pot_diff = self.players[(self.player_turn - 1) % len(self.players)].player_pot - self.players[self.player_turn].player_pot

        if amount + pot_diff > self.players[self.player_turn].check_money() or amount <= 0:
            self.pop_up.emit('Not a valid raise!')
        else:
            if not pot_diff == 0:
                amount = amount + pot_diff

            self.pot = self.pot + amount
            self.players[self.player_turn].change_player_pot(amount)
            self.players[self.player_turn].change_money(-amount)

            print(f'{self.players[self.player_turn].get_name()} has raised with ${amount-pot_diff}.')
            self.call_counter = 1 #Reseting the call counter
            self.next_turn()

    def fold(self):
        if self.players[self.player_turn].check_money() == 0: #If you dont have any money you call instead
            self.call()
            return
        self.remove_active_player()
        self.folded = True
        print(f'{self.players[self.player_turn].name} has folded.')

        self.pot_winner()#As there are only 2 players pot_winner is run
        self.reset_pot()

    def next_turn(self):
        self.player_turn = (self.player_turn + 1) % len(self.active_players)
        print(f'It is {self.players[self.player_turn].get_name()} turn, '
              f'you have ${self.players[self.player_turn].check_money()}')#So it's easier to play on the console
        if self.players[self.player_turn].check_money() == 0:
            self.all_in() #calls for you if you dont have any money so
        self.update_turn.emit()#updates the player view

    def all_in(self):
        self.call()

    def remove_active_player(self):
        self.active_players[self.player_turn] = 0

    def pot_winner(self):#gets the winner and hands out the money to the winner

        winner_index = self.active_players.index(1)
        player_winner = self.players[winner_index]
        if player_winner.get_player_pot() * 2 < self.pot:#If one person has done an all in but has less money in the pot
            player_winner.change_money(player_winner.get_player_pot() * 2)
        else:
            player_winner.change_money(self.pot)

        if not self.folded:#if you fold you should not see what hand the other person had
            self.pop_up.emit(
                f'The winner of the pot is {self.players[winner_index].name} with the total of ${self.pot} and with the hand '
                f'{str(self.players[winner_index].poker_hand_value(self.community_cards)).replace("_", " ").lower()}')
            print(
                f'The winner of the pot is {self.players[winner_index].name} with the total of ${self.pot} and with the hand '
                f'{str(self.players[winner_index].poker_hand_value(self.community_cards)).replace("_", " ").lower()}')
        else:
            self.pop_up.emit(
                f'The winner of the pot is {self.players[winner_index].name} with the total of ${self.pot}')
            print(
                f'The winner of the pot is {self.players[winner_index].name} with the total of ${self.pot}')
        self.reset_pot()

    def game_winner(self):#Is only run if there only is one player with money

        for i, player in enumerate(self.players):  # checks who has the money
            if not player.check_money() == 0:
                print(f'The winner of the game is {player.get_name()}')
                self.pop_up.emit(f'The winner of the game is {player.get_name()}. Thanks for playing!')
                #Sends two emits one for a pop up and one to en the game
        self.quit.emit()
