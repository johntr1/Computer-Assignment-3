from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *



class Player(QObject):

    def __init__(self, name):
        self.name = name
        self.hand = None
        self.money = 10000
        self.player_pot = 0

    def create_new_hand(self): #Kanske att handen ska skapas i init
        self.hand = Hand()
        return self.hand

    def player_pot(self):
        return self.in_pot()

    def change_player_pot(self, amount):
        self.in_pot = self.in_pot + amount

    def change_money(self, amount):
        self.money = self.money + amount
        if self.money < 0:
            print('No money')#ha ett stop här eller någon annanstans


class TexasHoldEm:
    def __init__(self):
        self.players = []
        self.active_players =[]
        self.pot = 0
        self.deck = None
        self.big_blind_player = 0


        #start the gui and for players and names
        #reset active players

        self.hand_out_cards()



    def hand_out_cards(self):
        self.deck = StandardDeck()
        self.deck = self.deck.shuffle()

        #reset in_pot to 0 for all players

        for player in self.players():
            hand = player.create_new_hand()
            for j in range(2):
                hand.add_card(self.deck.draw())

        self.big_and_little_blind()


    def big_and_little_blind(self):

        #big blind
        amount = 100
        self.pot = self.pot + amount
        self.players[self.big_blind].change_in_pot(amount)
        self.players[self.big_blind].change_money(-amount)

        #small blind
        amount = 50
        self.pot = self.pot + amount
        self.players[self.big_blind-1].change_in_pot(amount)
        self.players[self.big_blind-1].change_money(-amount)

    def pre_flop(self):

        self.players[self.big_blind + 1]


    def choose(self):


    def call(self, player):

        index = self.players.index(player)-1
        if self.players[index].player_pot() > player.player_pot: #if the player before has more in the pot
            diff = self.players[index].player_pot() - player.player_pot
            self.pot = self.pot + diff
            player.change_player_pot(diff)
            player.change_money(-diff)


    def poker_raise(self, player):
        #ask with the GUI how much should raise
        if not type(amount) == int:
            #GUI with an error saying to type in a whole number
        if amount > player.money:
            print('not enough money') # with an GUI

        self.pot = self.pot + amount
        player.change_in_pot(amount)
        player.change_money(-amount)


    def fold(self):





    def remove_active_player(self, player):










