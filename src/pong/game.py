import random, curses, time
from .objects import Ball, Paddle, Score
# from .networking import NetworkingDelegate

TICKRATE = 20
FREQ = 33

from abc import ABC, abstractmethod

class NetworkingDelegate(ABC):

    @abstractmethod
    def connected(self):
        pass

    @abstractmethod
    def received_data(self):
        pass

    @abstractmethod
    def disconnected(self):
        pass

class PongDelegate(NetworkingDelegate):

    def __init__(self, data_received):
        self.data_received = data_received

    def connected(self):
        print("connected!")
        pass

    def received_data(self, event, data):
        if event == "data":
            self.data_received(data)

    def disconnected(self):
        pass

class Game():
    def __init__(self, window, sio, host, match_code):
        self.window = window
        self.window.nodelay(True)
        self.window.keypad(True)
        curses.cbreak()
        curses.curs_set(0)

        self.match_code = match_code

        max_y, max_x = self.window.getmaxyx()

        self.ball = Ball(2, 2)
        self.paddle1 = Paddle(0, 0, 10, [curses.KEY_LEFT, curses.KEY_RIGHT])
        self.paddle2 = Paddle(0, max_y - 1, 10, [curses.KEY_LEFT, curses.KEY_RIGHT])
        self.scorex = 0
        self.scorey = 0
        self.score = Score(1, 1, "Score: 0:0")
        self.host = host
        self.delegate = PongDelegate(self.data_received)
        self.opponent_data = None
        self.sio = sio


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
        self.window.clear()
        draworder = sorted(game_state.values(), key=lambda o:o.x)
        for o in draworder:
            o.draw(self.window)
        self.window.refresh()

    def data_received(self, data):
        self.opponent_data = data

    def run(self):
        self.window.clear()
        #self.sio.start(self.delegate)
        self.sio.update_delegate(self.delegate)
        while True:
            start_time = time.time()
            keys, c = set(), self.window.getch()
            while(c != -1):
                keys.add(c)
                c = self.window.getch()
            if self.host:
                op_keys = set()
                if self.opponent_data and 'keys' in self.opponent_data:
                    op_keys = set(self.opponent_data['keys'])
                    self.opponent_data = None
                game_state = self.update(keys, op_keys)
                self.render(game_state)
                self.sio.emit('data', {'code': self.match_code, 'state':{k:v.serialize() for k,v in game_state.items()}})
            else:
                # self.print(str(len(self.opponent_data)))
                #self.print(str(self.opponent_data))
                if self.opponent_data and 'state' in self.opponent_data:
                    self.render(self.opponent_data['state'], unserialize=True)
                    self.opponent_data = None
                else:
                    game_state = self.update(keys, set())
                    self.render(game_state)
                    # msg = "" if len(self.opponent_data)==0 else self.opponent_data[0]
                    # self.print(str(msg))
                    pass
                self.sio.emit('data', {'code': self.match_code, 'keys': list(keys)})
            curses.flushinp()
            # curses.napms(int(1000 / TICKRATE))
            # self.print(str(time.time() - start_time))
            curses.napms(max(0,int(FREQ - (time.time() - start_time))))

        
    def print(self, msg):
        max_y, max_x = self.window.getmaxyx()
        self.window.addstr(int(max_y*3/8), max(0,int(max_x*1/2-len(msg)/2)), msg)
        self.window.refresh()
        
# def main(stdscr):
#     g = Game(stdscr, host=True)
#     g.run()

# if __name__ == '__main__':
#     curses.wrapper(main)
