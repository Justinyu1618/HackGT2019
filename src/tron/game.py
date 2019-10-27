import curses
import time

from .objects import Car

FREQ = 150

class Game:
    def __init__(self, window, sio, host, match_code, sid, players, size=None):
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

        self.sid = sid
        self.players = players

        self.cars = []
        self.cars.append(Car(10, 10, 1, 0))
        self.cars.append(Car(max_x - 10, 10, 2, 0))

        if len(players) >= 3:
            self.cars.append(Car(10, 12, 3, 2))

        if len(players) == 4:
            self.cars.append(Car(max_x - 10, 12, 4, 2))

        self.scorex = 0
        self.scorey = 0
        self.host = host
        self.opponent_data = {}
        self.sio = sio
        self.finished = False

    def display_winner(self, sid):
        h, w = self.window.getmaxyx()

        line1 = "GAME OVER"
        self.window.addstr(h // 2 - 1, (w - len(line1)) // 2 - 1, line1)

        if sid == self.sid:
            line2 = "YOU WIN"
        else:
            line2 = "YOU LOSE"

        self.window.addstr(h // 2, (w - len(line2)) // 2 - 1, line2)

    def update(self, keys):
        if self.finished:
            return None

        for i in range(len(self.players)):
            if self.players[i].sid not in keys:
                keys[self.players[i].sid] = {}

            self.window.addch(self.cars[i].y, self.cars[i].x, "+",
                    curses.color_pair(1))
            self.cars[i].update(self.window, keys[self.players[i].sid])

        h, w = self.window.getmaxyx()
        num_dead = 0
        sid_winner = ""

        for i in range(len(self.cars)):
            if self.cars[i].x < 0 or self.cars[i].x >= w or self.cars[i].y < 0 or \
                    self.cars[i].y >= h or chr(self.window.inch(self.cars[i].y,
                        self.cars[i].x)) != " ":
                self.cars[i].dead = True

            if self.cars[i].dead:
                num_dead += 1
            else:
                sid_winner = self.players[i].sid

        if num_dead >= len(self.players) - 1:
            self.finished = True
            self.sio.emit("data", {"code": self.match_code, "winner":
                sid_winner})
            self.display_winner(sid_winner)

        if self.finished:
            return None

        return {"cars": self.cars}
    
    def render(self, game_state, unserialize=False):
        if not self.host:
            for car in self.cars:
                self.window.addch(car.y, car.x, "+")

        if unserialize:
            cars = game_state["cars"]
            [self.cars[i].populate(cars[i]) for i in range(len(cars))]
            
            for o in self.cars:
                o.draw(self.window)

    def data_received(self, event, data):
        if event == "data":
            if "winner" in data:
                self.finished = True
                self.display_winner(data["winner"])
            else:
                self.opponent_data[data["sid"]] = data

    def i_from_sid(self, sid):
        i = 0

        for player in self.players:
            if player.sid == sid:
                return i
            i += 1

        return -1

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
                op_keys = {}
                for key in self.opponent_data:
                    if self.cars[self.i_from_sid(key)].dead:
                        continue

                    op_keys[key] = set(self.opponent_data[key]["keys"])

                if not self.cars[self.i_from_sid(self.sid)].dead:
                    op_keys[self.sid] = keys
                self.opponent_data = {}
                game_state = self.update(op_keys)
                if game_state is not None:
                    self.render(game_state)
                    self.sio.emit('data', {
                        'code': self.match_code,
                        'state':{k: [x.serialize() for x in v] for k,v in game_state.items()},
                        'timestep':timestep
                    })
            else:
                for key in self.opponent_data:
                    self.render(self.opponent_data[key]["state"],
                            unserialize=True)
                self.opponent_data = {}
                #if self.opponent_data and 'state' in self.opponent_data:# and 'timestep' in self.opponent_data and self.opponent_data['timestep'] > timestep:
                #    self.render(self.opponent_data['state'], unserialize=True)
                #    self.opponent_data = None

                if len(keys) > 0:
                    keys_event = {
                        "code": self.match_code,
                        "keys": list(keys)
                    }

                if timestep % 20 == 0 and keys_event is not None:
                    self.sio.emit('data', keys_event)
                    keys_event = None

            curses.flushinp()
            
            if self.host:
                curses.napms(max(0,int(FREQ - (time.time() - start_time))))
            else:
                curses.napms(10)

            timestep += 1
