import time
import curses

from src.networking.btio import *
from .objects import Ball, Paddle, Score

FREQ = 33   

class Game():
    def __init__(self, window, btio, host, match_code, size=None):
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

        self.ball = Ball(2, 2)
        self.paddle1 = Paddle(0, 0, 15, [curses.KEY_LEFT, curses.KEY_RIGHT])
        self.paddle2 = Paddle(0, max_y - 1, 15, [curses.KEY_LEFT, curses.KEY_RIGHT])
        self.scorex = 0
        self.scorey = 0
        self.score = Score(1, 1, "Score: 0:0")
        self.host = host
        self.opponent_data = None
        self.btio = btio

    def update(self, keys1, keys2):
        hit_edge = self.ball.update(self.window, [self.paddle1, self.paddle2])
        self.score.update(hit_edge)
        self.paddle1.update(self.window, keys1)
        self.paddle2.update(self.window, keys2)

        return {'score':self.score, 'ball':self.ball, 'paddle1':self.paddle1, 'paddle2':self.paddle2}
    
    def render(self, game_state, unserialize=False):
        if unserialize:
            for k,v in game_state.items():
                getattr(self, k).populate(v)
                game_state[k] = getattr(self, k)
        self.window.erase()
        draworder = sorted(game_state.values(), key=lambda o:o.x)
        for o in draworder:
            o.draw(self.window)
        self.window.refresh()

    def data_received(self, event, data):
        if event == "data":
            self.opponent_data = data

    def run(self):
        self.window.clear()
        update_callbacks(recv=self.data_received)
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
                self.render(game_state)
                self.btio.write('data', {'code': self.match_code, 'state':{k:v.serialize() for k,v in game_state.items()}, 'timestep':timestep})
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
                    self.btio.write('data', keys_event)
                    keys_event = None

            curses.flushinp()
            
            if self.host:
                curses.napms(max(0,int(FREQ - (time.time() - start_time))))
            else:
                curses.napms(1)

            timestep += 1
