import abc
from PyQt5.QtCore import QObject, pyqtSignal  # no GUI stuff inside this file!
from cardlib import *


# NOTE: This is just given as an example of how to use CardsView.
# It is expected that you will need to adjust things to make a game out of it. 

class QABCMeta(abc.ABCMeta, type(QObject)):
    # This metaclass wrapper is necessary when dealing with multiple inherited metaclasses:
    # We want ABCMeta and the metaclass for QOBject (which does the signal handling)
    # https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
    # You don't need to understand the subtleties of this in this course.
    # The exam won't cover multiple inheritance of metaclasses.
    pass


class CardsModel(QObject, metaclass=QABCMeta):
    """ Base class that described what is expected from the CardsView widget. """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abc.abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abc.abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""

    @abc.abstractmethod
    def flip(self):
        """Returns true of cards should be drawn face down"""
    @abc.abstractmethod
    def add_card(self, card):
        pass


class HandModel(CardsModel):
    def __init__(self, cards):
        self.cards = cards
        CardsModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        # This method mutates the object, so we must of course 
        super().add_card(card)
        # Add card:
        self.cards.append(card)
        self.new_cards.emit()  # something changed, better emit the signal!

    def drop_all_cards(self):
        self.cards = []
        self.new_cards.emit()


