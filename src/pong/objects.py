import curses


class Movable:
    def __init__(self, x, y, velx=0, vely=0):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely

    def update(self, window):
        new_x = self.x + self.velx
        new_y = self.y + self.vely
        max_y, max_x = window.getmaxyx()
        self.x = max(0, min(max_x - 1, new_x))
        self.y = max(0, min(max_y - 1, new_y))

    def draw(self, window):
        window.insch(int(self.y), int(self.x), "●")

    def serialize(self):
        return {k: v for k, v in self.__dict__.items()}

    def populate(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)


class Paddle(Movable):
    def __init__(self, x, y, w, keys, VEL_X=2):
        super(Paddle, self).__init__(x, y)
        self.w = w
        self.y = y
        self.k_l = keys[0]
        self.k_r = keys[1]
        self.VEL_X = VEL_X

    def update(self, window, keys):
        self.velx = (-1 * (self.k_l in keys) + (self.k_r in keys)) * self.VEL_X
        super(Paddle, self).update(window)

    def draw(self, window):
        if self.y == 0:
            paddle = "█" + ("▄" * (self.w - 2)) + "█"
        else:
            paddle = "█" + ("▀" * (self.w - 2)) + "█"
        window.insstr(round(self.y), round(self.x), paddle) 


class Ball(Movable):
    def __init__(self, x, y, velx=0.5, vely=0.5):
        super(Ball, self).__init__(x, y, velx, vely)

    def update(self, window, obstacles):
        super(Ball, self).update(window)
        ret = None
        scrh, scrw = window.getmaxyx()

        if self.x == (scrw - 1) or self.x == 0:
            self.velx *= -1
        if self.y == (scrh - 1):
            ret = "bottom"
            self.vely *= -1
        if self.y == 0:
            ret = "top"
            self.vely *= -1
        for obstacle in obstacles:
            if ((self.x >= obstacle.x and self.x <= (obstacle.x + obstacle.w + 1)) and 
               ((self.y >= (obstacle.y - 1)) and (self.y <= (obstacle.y + 1)))):
                self.vely *= -1
        return ret

    def draw(self, window):
        window.insch(round(self.y), round(self.x), "o")


class Score:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.score1 = 0
        self.score2 = 0

    def draw(self, window):
        window.insstr(self.y, self.x, self.text)

    def update(self, edge_hit):
        if edge_hit == "bottom":
            self.score2 += 1
        elif edge_hit == "top":
            self.score1 += 1
        self.text = f"Score: {self.score1}:{self.score2}"

    def serialize(self):
        return {k: v for k, v in self.__dict__.items()}

    def populate(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

