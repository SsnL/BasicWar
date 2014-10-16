class GameException(Exception):
    pass

class DrawFailure(GameException):
    def __init__(self, msg, player):
        super(DrawFailure, self).__init__(msg)
        self.player = player
