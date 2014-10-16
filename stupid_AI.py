import random
from player_def import *
from basic_def import *

class Stupid_AI(Player):
    # -1: Pass
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    def landfall(self):
        self.check_in_game()
        to_decide = []
        possible = []
        for basic in list(Basic):
            if (self.hand.look(basic) > 0):
                possible.append(basic)
                if (self.battlefield.look(basic) == 0):
                    to_decide.append(basic)
        if len(to_decide) > 0:
            basic = to_decide[random.randint(0, len(to_decide) - 1)]
        elif len(possible) > 0:
            basic = possible[random.randint(0, len(possible) - 1)]
        else:
            return Pass(self, self.game)
        if basic is Basic.mountain:
            least = 11
            least_oppo_basic = None
            for oppo_basic in Basic:
                temp_num = self.game.look_oppo_battlefield(self, oppo_basic);
                if temp_num < least and temp_num > 0:
                    least = self.game.look_oppo_battlefield(self, oppo_basic)
                    least_oppo_basic = oppo_basic
            return basic.action(self, self.game, least_oppo_basic)
        elif basic is Basic.forest:
            least = 21
            least_take_basic = None
            for take_basic in Basic:
                if (self.hand.look(take_basic) + self.battlefield.look(take_basic)) < least and self.graveyard.look(take_basic):
                    least = self.hand.look(take_basic) + self.battlefield.look(take_basic)
                    least_take_basic = take_basic
            return basic.action(self, self.game, least_take_basic)
        return basic.action(self, self.game)

    # -1: Pass
    # 0: Counter
    def daze(self, target):
        self.check_in_game()
        if target is Basic.islands:
            if self.hand.look(Basic.islands) > 1:
                return Counter(self, self.game)
        else:
            if self.hand.look(Basic.islands) and self.hand.look(target):
                return Counter(self, self.game)
        return Pass(self, self.game)

    # -1: Empty hand
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    def ravened(self):
        self.check_in_game()
        possible = []
        for basic in Basic:
            if (self.hand.look(basic) > 0):
                possible.append(basic)
        if len(possible) > 0:
            basic = possible[random.randint(0, len(possible) - 1)]
            return Ravened(self, self.game, basic)
        return Pass(self, self.game)
