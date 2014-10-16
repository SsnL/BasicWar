from basic_def import *
from deck_def import *
from player_def import *
from exception_def import *
from stupid_AI import *
from nn_AI import *

class Game:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.is_end = True
        self.stack = []

    def check_in_game(self):
        if not self.start:
            raise GameException("no valid started game")

    def check_win(self):
        self.check_in_game()
        if self.p0.battlefield.is_tribal():
            return self.p0
        if self.p1.battlefield.is_tribal():
            return self.p1
        return False

    def initialize(self, first_player):
        self.p0.initialize(self, Deck(self.p0, self))
        self.p1.initialize(self, Deck(self.p1, self))
        self.is_end = False
        first_player.draw(4)
        self.get_oppo(first_player).draw(5)

    def start(self):
        try:
            curr_player, oppo_player = 0, 1
            player = [0, 0]
            player[0] = self.p1 if random.random() < 0.5 else self.p0
            player[1] = self.get_oppo(player[0])
            self.initialize(player[0])
            while not self.is_end:
                self.log("")
                player[curr_player].begin_turn()
                self.push_stack(player[curr_player].landfall())
                if type(self.peek_stack()) is Play:
                    self.push_stack(player[oppo_player].daze(self.peek_stack().basic))
                while not self.is_empty_stack():
                    self.pop_stack().apply()
                curr_player, oppo_player = oppo_player, curr_player
                self.log(str(self.p0.battlefield))
                self.log(str(self.p1.battlefield))
                player[curr_player].end_turn()
                self.is_end = self.check_win()
            self.is_end.win()
            self.get_oppo(self.is_end).lose()
            return self.is_end.name
        except DrawFailure as e:
            self.get_oppo(e.player).win()
            e.player.lose()
            return self.get_oppo(e.player).name

    def get_oppo(self, player):
        self.check_in_game()
        if player is self.p0:
            return self.p1
        return self.p0

    # Returns the last element of currect stack.
    def peek_stack(self):
        return self.stack[len(self.stack) - 1]

    def pop_stack(self):
        return self.stack.pop()

    def push_stack(self, action):
        self.stack.append(action)

    def is_empty_stack(self):
        return len(self.stack) == 0

    def look_oppo_battlefield(self, player, basic):
        self.check_in_game()
        return self.get_oppo(player).battlefield.look(basic)

    def look_oppo_graveyard(self, player, basic):
        self.check_in_game()
        return self.get_oppo(player).graveyard.look(basic)

    def look_oppo_hand_size(self, player):
        self.check_in_game()
        return len(self.get_oppo(player).hand)

    def look_oppo_deck_size(self, player):
        self.check_in_game()
        return len(self.get_oppo(player).deck)

    def apply(self, action):
        self.check_in_game()
        action.apply(self)

    def log(self, str):
        print(str)
