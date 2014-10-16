from enum import Enum, unique
from exception_def import GameException

@unique
class Basic(Enum):
    plains = 0
    mountain = 1
    islands = 2
    forest = 3
    swamp = 4

class Action():
    def __init__(self, player, game):
        self.player = player
        self.game = game

    def apply(self):
        raise GameException("incomplete Action class {0}".format(self.name))

class Ravened(Action):
    def __init__(self, player, game, basic):
        super(Ravened, self).__init__(player, game)
        self.basic = basic

    def apply(self):
        self.player.discard(self.basic)

class Pass(Action):
    def apply(self):
        pass

class Counter(Action):
    def apply(self):
        self.player.counter(self.game.get_oppo(self.player), self.game.pop_stack().basic)

class Play(Action):
    def __init__(self, player, game, basic):
        super(Play, self).__init__(player, game)
        self.basic = basic

    def apply(self):
        self.player.play(self.basic)

class PlayIslands(Play):
    def __init__(self, player, game):
        super(PlayIslands, self).__init__(player, game, Basic.islands)

class Sinkhole(Play):
    def __init__(self, player, game, target):
        super(Sinkhole, self).__init__(player, game, Basic.mountain)
        self.target = target

    def apply(self):
        Play.apply(self)
        if self.target:
            self.game.get_oppo(self.player).destroyed(self.target)

class Cycle(Play):
    def __init__(self, player, game):
        super(Cycle, self).__init__(player, game, Basic.plains)

    def apply(self):
        Play.apply(self)
        self.player.draw()

class Raven(Play):
    def __init__(self, player, game):
        super(Raven, self).__init__(player, game, Basic.swamp)

    def apply(self):
        Play.apply(self)
        if self.game.look_oppo_hand_size(self.player) > 0:
            action = self.game.get_oppo(self.player).ravened()
            if type(action) is not Ravened:
                raise GameException("{0} must discard".format(self.player.name))
            self.game.push_stack(action)

class Regrowth(Play):
    def __init__(self, player, game, target):
        super(Regrowth, self).__init__(player, game, Basic.forest)
        self.target = target

    def apply(self):
        Play.apply(self)
        if self.target:
            self.player.regrowth(self.target)

Basic.plains.action = Cycle
Basic.mountain.action = Sinkhole
Basic.islands.action = PlayIslands
Basic.forest.action = Regrowth
Basic.swamp.action = Raven
