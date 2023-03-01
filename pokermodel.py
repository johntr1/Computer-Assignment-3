from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *



class Player():

    def __init__(self, name):
        self.name = name
        self.hand = None
        self.money = 10000
        self.player_pot = 0

    def create_new_hand(self): #Kanske att handen ska skapas i init
        self.hand = Hand()
        return self.hand

    def get_name(self):
        return self.name
    def player_pot(self):
        return self.player_pot

    def change_player_pot(self, amount):
        self.in_pot = self.in_pot + amount

    def reset_player_pot(self):
        self.player_pot = 0

    def check_money(self):
        return self.money

    def change_money(self, amount):
        self.money = self.money + amount
        if self.money < 0:
            print('No money')#ha ett stop här eller någon annanstans

    def poker_hand_value(self, community_cards):
       return self.hand.best_poker_hand(community_cards)

class TexasHoldEm:
    def __init__(self):
        self.players = []
        self.active_players =[]
        self.pot = 0
        self.deck = None
        self.community_cards = []
        self.big_blind_player = 0


        #start the gui and for players and names

        while True:#While 2 people have money

            for player in self.players:
                player.reset_player_pot()

            for i in range(len(self.players)): #Resets the active players
                self.active_players.append(1)

            for i, j in enumerate(self.players): # If the player has no money she/he is not an active player
                if j.check_money() == 0:
                    self.active_players[i] = 0

            self.hand_out_cards()

            self.big_and_little_blind()

            self.pre_flop()






            self.big_blind_player = 1 + self.big_blind_player



    def hand_out_cards(self):

        self.deck = StandardDeck()
        self.deck = self.deck.shuffle()

        #reset in_pot to 0 for all players
        for i, player in enumerate(self.players()):
            if self.active_players[i] == 0: # Only gives cards to active players
                continue
            hand = player.create_new_hand()
            for j in range(2):
                hand.add_card(self.deck.draw())


    def big_and_little_blind(self):

        for i in len(self.active_players): #checks if the big blind player is active
            if self.active_players[self.big_blind_player + i] == 1:
                self.big_blind_player = self.big_blind_player + i
                break

        #big blind
        amount = 100
        self.pot = self.pot + amount
        self.players[self.big_blind_player].change_in_pot(amount)
        self.players[self.big_blind_player].change_money(-amount)

        #small blind
        amount = 50
        self.pot = self.pot + amount
        self.players[self.big_blind_player-1].change_in_pot(amount)
        self.players[self.big_blind_player-1].change_money(-amount)

    def pre_flop(self):
        self.betting_round()

    def flop(self):
        community_cards = []
        for i in range(3):
            community_cards.append(self.deck.draw)
        #Show 3 community_cards
        self.betting_round()
        return community_cards

    def turn(self,community_cards):

        #show 1 community_card
        community_cards.append(self.deck.draw)
        print(community_cards)
        self.betting_round()
        return community_cards

    def river(self, community_cards):
        #show 1 community_card
        community_cards.append(self.deck.draw)
        print(community_cards)
        self.betting_round()
        return community_cards

    def showdown(self, community_cards):
        best_poker_hands_list = []

        for index in self.active_players:
            if index == 1:
                best_poker_hands_list.append(self.players[index].poker_hand_value(community_cards))
            else:
                best_poker_hands_list.append(0)

        best_hand_index = best_poker_hands_list.index(max(best_poker_hands_list))
        #besthand = [i for i, x in enumerate(best_poker_hands_list) if x == max(a)]

        for i in len(self.active_players):
            self.active_players[i] = 0
        self.active_players[best_hand_index] = 1







    def betting_round(self):
        player_turn = self.big_blind_player + 1
        raiser = player_turn

        while True:

            for i in len(self.active_players):  # checks if the turn_player is an active player
                if self.active_players[player_turn + i] == 1:
                    player_turn = player_turn + i
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

    def check_play(self):
        if sum(self.active_players) <= 1:
            return False
        else:
            return True

    def check_game(self):

        list = []
        for player in self.players:  #checks if more than one person has money
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
            elif inp == 'rasie':
                self.poker_raise(player)
                return  "raise"
            elif inp == 'fold':
                self.fold(player)
                return 'fold'



    def call(self, player):

        index = self.players.index(player)-1
        if self.players[index].player_pot() > player.player_pot: #if the player before has more in the pot
            diff = self.players[index].player_pot() - player.player_pot
            self.pot = self.pot + diff
            player.change_player_pot(diff)
            player.change_money(-diff)



    def poker_raise(self, player):
        #ask with the GUI how much should raise
        while True:
            amount = input('How much do you want to raise with?')
            if type(amount) == int and amount <= player.money:
                break
            #GUI with an error saying to type in a whole number
            print('not enough money or not an int') # with an GUI

        self.pot = self.pot + amount
        player.change_in_pot(amount)
        player.change_money(-amount)


    def fold(self, player):

        self.remove_active_player(player)
        return 'fold'

    def remove_active_player(self, player):
        self.active_players[self.players.index(player)] = 0


    def pot_winner(self):
        winner_index = self.active_players.index(1)
        print(f'the winner of the pot is {self.players[winner_index].name}')
        return winner_index

         #check who is the winner


    def game_winner(self):




