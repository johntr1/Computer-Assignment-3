
from cardlib import *




class Player(name):
    def __int__(self):
       # self.name = name
        self.hand = None
        self.money = 10000
        self.in_pot = 0

    def create_new_hand(self): #Kanske att handen ska skapas i init
        self.hand = Hand()
        return self.hand

    def in_pot(self):
        return self.in_pot()

    def change_in_pot(self, amount):
        self.in_pot = self.in_pot + amount

    def change_money(self, amount):
        self.money = self.money + amount
        if self.money < 0:
            print('No money')#ha ett stop här eller någon annanstans


class TexasHoldEm:
    def __int__(self):
        self.players = []
        self.pot = 0


        #start the gui and for players and names
       while True: # Check that all players have money
           new_round()



    def new_round(self):
        deck = StandardDeck()
        deck = deck.shuffle()

        #reset in_pot to 0 for all players

        for player in  self.players():
            hand = player.create_new_hand()
            for j in range(2):
                hand.add_card(deck.draw())

        for player in self.players():
            #choose to call fold or bet

    def call(self, player):

        index = self.players.index(player)-1
        if self.players[index].in_pot() > player.in_pot: #if the player before has more in the pot
            diff = self.players[index].in_pot() - player.in_pot
            self.pot = self.pot + diff
            player.change_in_pot(diff)
            player.change_money(-diff)


    def rasie(self, player):
        #ask with the GUI how much should raise
        if not type(amount) == int:
            #GUI with an error saying to type in a whole number
        if amount > player.money:
            print('not enough money') # with an GUI

        self.pot = self.pot + amount
        player.change_in_pot(amount)
        player.change_money(-amount)













