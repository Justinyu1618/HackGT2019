import curses
import time

from .objects import Car

FREQ = 200

class Game:
    def __init__(self, window, sio, host, match_code, size=None):
        window.clear()
        window.refresh()
        bounding_wind = window.derwin(size[1], size[0],0,0)
        bounding_wind.box()
        bounding_wind.refresh()
        max_y, max_x = bounding_wind.getmaxyx()
        self.window = bounding_wind.derwin(max_y-2, max_x-2,1,1)

        self.window.nodelay(True)
        self.window.keypad(True)
        curses.cbreak()
        curses.curs_set(0)

        self.match_code = match_code

        max_y, max_x = self.window.getmaxyx()

        self.car1 = Car(15, 15, 2)
        self.car2 = Car(10, 10, 2)
        self.scorex = 0
        self.scorey = 0
        self.host = host
        self.opponent_data = None
        self.sio = sio
        self.finished = False

    def display_winner(self, i):
        h, w = self.window.getmaxyx()

        line1 = "GAME OVER"
        self.window.addstr(h // 2 - 1, (w - len(line1)) // 2 - 1, line1)

        line2 = f"PLAYER {i} WINS"
        self.window.addstr(h // 2, (w - len(line2)) // 2 - 1, line2)

    def update(self, keys1, keys2):
        if self.finished:
            return None

        self.window.addch(self.car1.y, self.car1.x, "+")
        self.window.addch(self.car2.y, self.car2.x, "+")

        self.car1.update(self.window, keys1)
        self.car2.update(self.window, keys2)

        h, w = self.window.getmaxyx()

        if self.car1.x < 0 or self.car1.x >= w or self.car1.y < 0 or \
                self.car1.y >= h or chr(self.window.inch(self.car1.y,
                    self.car1.x)) != " ":
            self.finished = True
            self.sio.emit("data", {"code": self.match_code, "winner": 2})
            self.display_winner(2)

        if self.car2.x < 0 or self.car2.x >= w or self.car2.y < 0 or \
                self.car2.y >= h or chr(self.window.inch(self.car2.y,
                    self.car2.x)) != " ":
            self.finished = True
            self.sio.emit("data", {"code": self.match_code, "winner": 1})
            self.display_winner(1)

        if self.finished:
            return None

        return {
            "car1": self.car1,
            "car2": self.car2
        }
    
    def render(self, game_state, unserialize=False):
        if not self.host:
            self.window.addch(self.car1.y, self.car1.x, "+")
            self.window.addch(self.car2.y, self.car2.x, "+")

        if unserialize:
            for k,v in game_state.items():
                getattr(self, k).populate(v)
                game_state[k] = getattr(self, k)
        draworder = sorted(game_state.values(), key=lambda o: o.x)
        for o in draworder:
            o.draw(self.window)

    def data_received(self, event, data):
        if event == "data":
            if "winner" in data:
                self.finished = True
                self.display_winner(data["winner"])
            else:
                self.opponent_data = data

    def run(self):
        self.window.clear()
        self.sio.update_callbacks(recv=self.data_received)
        timestep = 0

        keys_event = {}

        while True:
            start_time = time.time()
            keys, c = set(), self.window.getch()
            while c != -1:
                keys.add(c)
                c = self.window.getch()

            if self.host:
                op_keys = set()
                if self.opponent_data and 'keys' in self.opponent_data:
                    op_keys = set(self.opponent_data['keys'])
                    self.opponent_data = None
                game_state = self.update(keys, op_keys)
                if game_state is not None:
                    self.render(game_state)
                    self.sio.emit('data', {'code': self.match_code, 'state':{k:v.serialize() for k,v in game_state.items()}, 'timestep':timestep})
            else:
                if self.opponent_data and 'state' in self.opponent_data:# and 'timestep' in self.opponent_data and self.opponent_data['timestep'] > timestep:
                    self.render(self.opponent_data['state'], unserialize=True)
                    self.opponent_data = None

                if len(keys) > 0:
                    keys_event = {
                        "code": self.match_code,
                        "keys": list(keys)
                    }

                if timestep % 33 == 0 and keys_event is not None:
                    self.sio.emit('data', keys_event)
                    keys_event = None

            curses.flushinp()
            
            if self.host:
                curses.napms(max(0,int(FREQ - (time.time() - start_time))))
            else:
                curses.napms(1)

            timestep += 1
