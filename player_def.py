from area_def import *
from basic_def import *

class Player:
    # hand = [Plains, Mountain, Islands, Forest, Swamp]

    def __init__(self, name):
        self.name = name

    def initialize(self, game, deck):
        self.hand = Area(self, "hand")
        self.battlefield = Area(self, "battlefield")
        self.graveyard = Area(self, "graveyard")
        self.deck = deck
        self.game = game
        self.turn = 0

    def check_in_game(self):
        if not (hasattr(self, "game") and hasattr(self, "deck") \
           and hasattr(self, "hand") and hasattr(self, "battlefield") \
           and hasattr(self, "graveyard")) or self.game.check_in_game():
            raise GameException("no valid game for player {0}".format(self.name))

    def draw(self, amount = 1):
        self.check_in_game()
        for _ in range(amount):
            self.hand.add(self.deck.draw())
        self.game.log("{0} draws {1} card".format(self.name, amount))

    def begin_turn(self):
        self.turn += 1
        self.draw(1)

    def end_turn(self):
        while len(self.hand) > 7:
            self.discard(self.ravened().basic)

    def play(self, basic):
        self.check_in_game()
        self.hand.take(basic)
        self.battlefield.add(basic)
        self.game.log("{0} plays {1}".format(self.name, basic.name))

    def regrowth(self, basic):
        self.check_in_game()
        self.hand.add(basic)
        self.graveyard.take(basic)
        self.game.log("{0} regrowths {1}".format(self.name, basic.name))

    def destroyed(self, basic):
        self.check_in_game()
        self.battlefield.take(basic)
        self.graveyard.add(basic)
        self.game.log("{0}'s {1} is destroyed".format(self.name, basic.name))

    def discard(self, basic):
        self.check_in_game()
        self.hand.take(basic)
        self.graveyard.add(basic)
        self.game.log("{0} discards {1}".format(self.name, basic.name))

    def counter(self, opponent, basic):
        self.check_in_game()
        self.discard(Basic.islands)
        self.discard(basic)
        self.game.log("{0} counters {1}'s {2}".format(self.name, opponent.name, basic.name))

    def win(self):
        pass

    def lose(self):
        pass

    # -1: Pass
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    def landfall(self):
        self.check_in_game()
        raise GameException("incomplete Player class {0}".format(self.name))
        return

    # -1: Pass
    # 0: Counter
    def daze(self, target):
        self.check_in_game()
        raise GameException("incomplete Player class {0}".format(self.name))
        return

    # -1: Empty hand
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    def ravened(self):
        self.check_in_game()
        raise GameException("incomplete Player class {0}".format(self.name))
        return
