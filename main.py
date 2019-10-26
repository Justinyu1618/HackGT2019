import curses

from networking import sio
from networking.delegate import NetworkingDelegate

"""
class PongDelegate(NetworkingDelegate):

    def connected(self):
        print("connected!")
        pass

    def received_data(self, data):
        pass

    def disconnected(self):
        pass

d = PongDelegate()
sio.start(d)
"""

MAX_PLAYERS = 4

class Player:

    def __init__(self, host):
        self.host = host

class Matchmaking:

    def __init__(self, stdscr):
        self.screen = stdscr
        self.H = curses.LINES
        self.W = curses.COLS

        self.players = []
        self.player_wind = stdscr.derwin(self.H // 2, self.W, self.H // 2, 0)
        self.player_wind.box()

        self.player_winds = {}
        self.add_player(Player(True))

    def refresh(self):
        self.player_wind.clear()
        self.player_wind.box()
        self.player_wind.refresh()

        self.display_players()

    def sleep(self, time):
        self.screen.timeout(time)
        self.screen.getch()
        self.screen.timeout(-1)

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            return

        self.players.append(player)

    def display_player(self, i):
        h, w = self.player_winds[i].getmaxyx()

        name = f"Player {i+1}"
        self.player_winds[i].addstr(1, (w - len(name)) // 2, name)
        self.player_winds[i].refresh()

    def display_players(self):
        height, width = stdscr.getmaxyx()

        for i, wind in enumerate(self.players):
            wind = self.player_wind.derwin(0, width // len(self.players), 0,
                    (width // len(self.players)) * i)
            wind.box()
            wind.refresh()

            self.player_winds[i] = wind
            self.display_player(i)

    def handle_input(self, char):
        if char == ord("n"):
            self.add_player(Player(False))

    def run(self):
        while True:
            self.handle_input(self.screen.getch())
            self.refresh()
            self.sleep(50)

def main(stdscr):
    match = Matchmaking(stdscr)
    match.run()

stdscr = curses.initscr()
stdscr.nodelay(True)
curses.wrapper(main)
