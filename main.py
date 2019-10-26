from networking import sio
from networking.delegate import NetworkingDelegate

from src.pong.game import Game
import curses, sys, uuid

def run_host(stdscr):
    game = Game(stdscr, sio, host=True)
    game.run()

def run_client(stdscr):
    game = Game(stdscr, sio, host=False)
    game.run()

MAX_PLAYERS = 4

class Player:

    def __init__(self, host):
        self.host = host

class MatchmakingDelegate(NetworkingDelegate):

    def __init__(self, connected, data):
        self.connected = connected
        self.received_data = data

    def connected(self):
        pass

    def received_data(self, event, data):
        if event == "match":
            pass

    def disconnected(self):
        pass

class Matchmaking:

    def __init__(self, stdscr, sio):
        self.sio = sio

        self.screen = stdscr
        self.H = curses.LINES
        self.W = curses.COLS

        self.players = []
        self.player_wind = stdscr.derwin(self.H // 2, self.W, self.H // 2, 0)
        self.player_wind.box()

        self.player_winds = {}
        self.add_player(Player(True))

        delegate = MatchmakingDelegate(self.on_connect, None)
        self.sio.start(delegate)

    def on_connect(self):
        match_code = str(uuid.uuid4())[:4]
        self.sio.emit("match", {"code": match_code, "status": "new_match"})

    def refresh(self):
        h, w = self.screen.getmaxyx()

        self.player_wind.clear()
        self.player_wind.box()
        self.player_wind.refresh()
        self.display_players()

        if self.players[0].host:
            text = "Press (s) to start!"
        else:
            text = "Waiting for host to start..."

        self.screen.addstr(5, (w - len(text)) // 2, text)

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
    match = Matchmaking(stdscr, sio)
    match.run()

stdscr = curses.initscr()
stdscr.nodelay(True)
curses.wrapper(main)

"""
if __name__ == '__main__':
    if sys.argv[1] == "host":
        curses.wrapper(run_host)
    elif sys.argv[1] == "client":
        curses.wrapper(run_client)
"""
