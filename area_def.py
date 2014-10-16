class Area:
    def __init__(self, player, name):
        self.area = [0, 0, 0, 0, 0]
        self.player = player
        self.name = name
        self.size = 0

    def add(self, basic):
        self.area[basic.value] += 1
        self.size += 1

    def take(self, basic):
        if self.area[basic.value] > 0:
            self.area[basic.value] -= 1
            self.size -= 1
            return
        raise GameException("no {0} in {1}'s {2}".format(basic.name, self.player.name, self.name))

    def look(self, basic):
        return self.area[basic.value]

    def is_tribal(self):
        return 0 not in self.area

    def __len__(self):
        return self.size

    def __str__(self):
        return "{0}'s {1}: {2}".format(self.player.name, self.name, str(self.area))
