import neurolab
import pickle
import numpy
from os import path
from player_def import *
from basic_def import *
from exception_def import GameException

class NN_AI(Player):
    # hand = [Plains, Mountain, Islands, Forest, Swamp]

    def __init__(self, name):
        super(NN_AI, self).__init__(name)
        self.states = list()
        self.record_path = name + "_record.obj"
        self.nn_path = name + "_nn.obj"
        # record[0] = list of inputs, record[1] = list of ouputs
        self.record = self.initialize_record(self.record_path)
        self.nn = self.initialize_nn(self.nn_path)

    def initialize_nn(self, file_path):
        if path.isfile(file_path):
            return pickle.load(open(file_path, "rb"))
        nn = neurolab.net.newff([[0, 10]] * 25 + [[0, 50]] * 2 + [[0, 7], [1, 60]], [5, 1])
        nn.trainf = neurolab.train.train_gdm
        nn.transf = neurolab.trans.LogSig
        return nn

    def initialize_record(self, file_path):
        if path.isfile(file_path):
            return pickle.load(open(file_path, "rb"))
        return [numpy.array([]), numpy.array([])]

    # [~5 interleaved ~(self.hand, self.battlefield, self.graveyard,
    #  oppo.battlefield, oppo.graveyard), self.deck_size, oppo.deck_size,
    #  oppo.hand_size self.turn]
    def get_nn_inputs(self):
        self.check_in_game()
        inputs = list()
        for basic in Basic:
            inputs.append(self.hand.look(basic))
            inputs.append(self.battlefield.look(basic))
            inputs.append(self.graveyard.look(basic))
            inputs.append(self.game.look_oppo_battlefield(self, basic))
            inputs.append(self.game.look_oppo_graveyard(self, basic))
        inputs.append(len(self.deck))
        inputs.append(self.game.look_oppo_deck_size(self))
        inputs.append(self.game.look_oppo_hand_size(self))
        inputs.append(self.turn)
        return numpy.array(inputs).reshape(1, len(inputs))

    def win(self):
        self.generate_record(1)

    def lose(self):
        self.generate_record(0)

    # record[0] = list of inputs, record[1] = list of ouputs
    def generate_record(self, game_result):
        l_in = list()
        for inp in self.states:
            l_in.append(inp[0])
        l_out = [[game_result]] * len(self.states)
        for i in range(len(self.record[0])):
            l_in.append(self.record[0][i])
            l_out.append(self.record[1][i])
        self.record = [numpy.array(l_in), numpy.array(l_out)]
        self.states.clear()
        self.save_record()

    def record_state(self, inputs):
        self.states.append(inputs)

    def save_record(self):
        pickle.dump(self.record, open(self.record_path, "wb"))

    def merge_record(self, record_1):
        l_in = list()
        l_out = list()
        for i in range(len(self.record[0])):
            l_in.append(self.record[0][i])
            l_out.append(self.record[1][i])
        for i in range(len(record_1[0])):
            l_in.append(record_1[0][i])
            l_out.append(record_1[1][i])
        self.record = [numpy.array(l_in), numpy.array(l_out)]
        self.save_record()

    def save_nn(self):
        pickle.dump(self.nn, open(self.nn_path, "wb"))

    def train_nn(self):
        if len(self.states) != 0:
            raise GameException("{0} has unprocessed game record".format(self.name))
        if not self.enough_record:
            raise GameException("{0} doesn't have enough game record".format(self.name))
        error = self.nn.train(self.record[0], self.record[1], epochs = 1500, show = 10, goal = 0.00001)
        self.record[0] = numpy.array([])
        self.record[1] = numpy.array([])
        self.save_record()
        self.save_nn()

    def end_turn(self):
        super(NN_AI, self).end_turn()
        if self.turn > 1:
            self.record_state(self.get_nn_inputs())

    @property
    def enough_record(self):
        return len(self.record[0]) > 1200

    def num_record(self):
        return len(self.record[0])

    def count_deck(self, basic):
        self.check_in_game()
        return 10 - self.hand.look(basic) - self.graveyard.look(basic) \
            - self.battlefield.look(basic)

    # -1: Pass
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    # [~5 interleaved ~(self.hand, self.battlefield, self.graveyard,
    #  oppo.battlefield, oppo.graveyard), self.deck_size, oppo.deck_size,
    #  oppo.hand_size self.turn]
    def landfall(self):
        self.check_in_game()
        max_move = -1
        inputs = self.get_nn_inputs()
        max_val = self.nn.sim(inputs)
        # Plains
        if inputs[0][0] and len(self.deck):
            inputs[0][0] -= 1
            inputs[0][1] += 1
            inputs[0][25] -= 1
            t = 0
            for basic in Basic:
                inputs[0][basic.value * 5] += 1
                t += self.count_deck(basic) * self.nn.sim(inputs)
                inputs[0][basic.value * 5] -= 1
            inputs[0][0] += 1
            inputs[0][1] -= 1
            inputs[0][25] += 1
            t /= len(self.deck)
            if max_val <= t:
                max_val = t
                max_move = 0
        # Mountain
        if inputs[0][5]:
            inputs[0][5] -= 1
            inputs[0][6] += 1
            t = self.nn.sim(inputs)
            if max_val <= t:
                max_val = t
                max_move = 1
                additional = None
            for oppo_basic in Basic:
                if self.game.look_oppo_battlefield(self, oppo_basic) > 0:
                    inputs[0][oppo_basic.value * 5 + 3] -= 1
                    inputs[0][oppo_basic.value * 5 + 4] += 1
                    t = self.nn.sim(inputs)
                    if max_val <= t:
                        max_val = t
                        max_move = 1
                        additional = oppo_basic
                    inputs[0][oppo_basic.value * 5 + 3] += 1
                    inputs[0][oppo_basic.value * 5 + 4] -= 1
            inputs[0][5] += 1
            inputs[0][6] -= 1
        # Islands
        if inputs[0][10]:
            inputs[0][10] -= 1
            inputs[0][11] += 1
            t = self.nn.sim(inputs)
            if max_val <= t:
                max_val = t
                max_move = 2
            inputs[0][10] += 1
            inputs[0][11] -= 1
        # Forest
        if inputs[0][15]:
            inputs[0][15] -= 1
            inputs[0][16] += 1
            t = self.nn.sim(inputs)
            if max_val <= t:
                max_val = t
                max_move = 3
                additional = None
            for grave_basic in Basic:
                if self.graveyard.look(grave_basic) > 0:
                    inputs[0][grave_basic.value * 5 + 2] -= 1
                    inputs[0][grave_basic.value * 5] += 1
                    t = self.nn.sim(inputs)
                    if max_val <= t:
                        max_val = t
                        max_move = 3
                        additional = grave_basic
                    inputs[0][grave_basic.value * 5 + 2] += 1
                    inputs[0][grave_basic.value * 5] -= 1
            inputs[0][15] += 1
            inputs[0][16] -= 1
        # Swamp
        if inputs[0][20]:
            inputs[0][20] -= 1
            inputs[0][21] += 1
            if inputs[0][27]:
                inputs[0][27] -= 1
                t = 0
                n = 0
                for basic in Basic:
                    inputs[0][basic.value * 5 + 3] += 1
                    left_n = 10 - inputs[0][basic.value * 5 + 3] - inputs[0][basic.value * 5 + 4]
                    n += left_n
                    t += left_n * self.nn.sim(inputs)
                    inputs[0][basic.value * 5 + 3] -= 1
                t /= n
                inputs[0][27] += 1
            else:
                t = self.nn.sim(inputs)
            if max_val <= t:
                max_val = t
                max_move = 4
            inputs[0][20] += 1
            inputs[0][21] -= 1
        if max_move == 3 or max_move == 1:
            return Basic(max_move).action(self, self.game, additional)
        if max_move == -1:
            return Pass(self, self.game)
        return Basic(max_move).action(self, self.game)

    # -1: Pass
    # 0: Counter
    # [~5 interleaved ~(self.hand, self.battlefield, self.graveyard,
    #  oppo.battlefield, oppo.graveyard), self.deck_size, oppo.deck_size,
    #  oppo.hand_size self.turn]
    def daze(self, target):
        self.check_in_game()
        inputs = self.get_nn_inputs()
        if target is Basic.islands and self.hand.look(Basic.islands) > 1:
            # counter
            inputs[0][14] += 1
            inputs[0][27] -= 1
            inputs[0][10] -= 2
            inputs[0][12] += 2
            counter_val = self.nn.sim(inputs)
            inputs[0][14] -= 1
            inputs[0][27] += 1
            inputs[0][10] += 2
            inputs[0][12] -= 2
            # pass
            inputs[0][13] += 1
            inputs[0][27] -= 1
            pass_val = self.nn.sim(inputs)
            inputs[0][13] -= 1
            inputs[0][27] += 1
            if counter_val > pass_val:
                return Counter(self, self.game)
        elif self.hand.look(Basic.islands) and self.hand.look(target):
            # counter
            inputs[0][target.value * 5 + 4] += 1
            inputs[0][27] -= 1
            inputs[0][target.value * 5] -= 1
            inputs[0][target.value * 5 + 2] += 1
            inputs[0][10] -= 1
            inputs[0][12] += 1
            counter_val = self.nn.sim(inputs)
            inputs[0][target.value * 5 + 4] -= 1
            inputs[0][27] += 1
            inputs[0][target.value * 5] += 1
            inputs[0][target.value * 5 + 2] -= 1
            inputs[0][10] += 1
            inputs[0][12] -= 1
            if target is Basic.plains:
                if inputs[0][26]:
                    # pass
                    inputs[0][3] += 1
                    inputs[0][26] -= 1
                    pass_val = self.nn.sim(inputs)
                    inputs[0][3] -= 1
                    inputs[0][26] += 1
                else:
                    pass_val = float("inf")
            elif target is Basic.mountain:
                # pass
                inputs[0][8] += 1
                inputs[0][27] -= 1
                pass_val = self.nn.sim(inputs)
                for basic in Basic:
                    if self.battlefield.look(basic):
                        inputs[0][basic.value * 5 + 1] -= 1
                        inputs[0][basic.value * 5 + 2] += 1
                        pass_val = min(pass_val, self.nn.sim(inputs))
                        inputs[0][basic.value * 5 + 1] += 1
                        inputs[0][basic.value * 5 + 2] -= 1
                inputs[0][8] -= 1
                inputs[0][27] += 1
            elif target is Basic.forest:
                # pass
                inputs[0][18] += 1
                inputs[0][27] -= 1
                pass_val = self.nn.sim(inputs)
                inputs[0][27] += 1
                for basic in Basic:
                    if self.game.look_oppo_graveyard(self, basic):
                        inputs[0][basic.value * 5 + 4] -= 1
                        pass_val = min(pass_val, self.nn.sim(inputs))
                        inputs[0][basic.value * 5 + 4] += 1
                inputs[0][18] -= 1
            else:
                would = self.ravened().basic
                # pass
                inputs[0][23] += 1
                inputs[0][27] -= 1
                inputs[would.value * 5] -= 1
                inputs[would.value * 5 + 2] += 1
                pass_val = self.nn.sim(inputs)
                inputs[0][23] -= 1
                inputs[0][27] += 1
                inputs[would.value * 5] += 1
                inputs[would.value * 5 + 2] -= 1
            if counter_val > pass_val:
                return Counter(self, self.game)
        return Pass(self, self.game)

    # -1: Empty hand
    # 0: Plains
    # 1: Mountain
    # 2: Islands
    # 3: Forest
    # 4: Swamp
    # [~5 interleaved ~(self.hand, self.battlefield, self.graveyard,
    #  oppo.battlefield, oppo.graveyard), self.deck_size, oppo.deck_size,
    #  oppo.hand_size self.turn]
    def ravened(self):
        self.check_in_game()
        valid = False
        max_val = float("-inf")
        inputs = self.get_nn_inputs()
        for basic in Basic:
            if inputs[0][basic.value * 5]:
                valid = True
                inputs[0][basic.value * 5] -= 1
                inputs[0][basic.value * 5 + 2] += 1
                t = self.nn.sim(inputs)
                inputs[0][basic.value * 5] += 1
                inputs[0][basic.value * 5 + 2] -= 1
                if max_val <= t:
                    max_val = t
                    max_move = basic.value
        if not valid:
            return Pass(self, self.game)
        return Ravened(self, self.game, Basic(max_move))
