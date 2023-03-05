from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cardsview import CardsView
from cardlib import *
from cardsmodel import HandModel
from pokermodel import *
import sys

hand = Hand()
hand.add_card(JackCard(Suit.Spades))
hand.add_card(KingCard(Suit.Hearts))

cards = HandModel(hand.cards)
print(cards)
cards.cards.append(NumberedCard(2, Suit.Spades))
print(cards)

