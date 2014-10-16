import random
from basic_def import *
from exception_def import DrawFailure

class Deck:
    def __init__(self, player, game):
        self.deck = [Basic(i) for i in range(5)] * 10
        random.shuffle(self.deck)
        self.player = player
        self.game = game

    def draw(self):
        try:
            return self.deck.pop()
        except IndexError:
            raise DrawFailure("{0} loses".format(self.player.name), self.player) from None

    def __len__(self):
        return len(self.deck)
