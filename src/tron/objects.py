import curses

class Car:

    def __init__(self, x, y, direction=0):
        self.x = x
        self.y = y
        self.direction = 0

    def update(self, window, keys):
        if curses.KEY_LEFT in keys:
            self.direction = 3
        elif curses.KEY_UP in keys:
            self.direction = 0
        elif curses.KEY_RIGHT in keys:
            self.direction = 1
        elif curses.KEY_DOWN in keys:
            self.direction = 2

        if self.direction == 3:
            self.x -= 1
        elif self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1

    def draw(self, window):
        window.addch(self.y, self.x, "%")

    def serialize(self):
        return {k: v for k, v in self.__dict__.items()}

    def populate(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
