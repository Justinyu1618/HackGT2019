from networking import sio

from src.tron.game import Game
import curses, sys, uuid

MAX_PLAYERS = 4

class Player:

    def __init__(self, host):
        self.host = host

class Matchmaking:

    def __init__(self, stdscr, sio, match_code=None):
        self.sio = sio

        self.screen = stdscr
        self.H = curses.LINES
        self.W = curses.COLS

        self.players = []
        self.player_wind = stdscr.derwin(self.H // 2, self.W, self.H // 2, 0)
        self.player_wind.box()

        self.player_winds = {}
        self.add_player(Player(True))

        self.host = match_code is None
        self.match_code = match_code

        self.match_size_y, self.match_size_x = self.screen.getmaxyx()

        self.sio.start(self.on_connect, self.on_receive_data)

        self.finished = False

    def on_connect(self):
        if self.match_code is None:
            match_code = str(uuid.uuid4())[:4]
            self.match_code = match_code

            self.sio.emit("match", {"code": match_code, "status": "new_match"})
        else:
            self.sio.emit("match", {"code": self.match_code, "status": "join_match", "size":(self.screen.getmaxyx())})

        self.refresh()

    def on_receive_data(self, event, data):
        if event == "match" and data["code"] == self.match_code:
            if data["status"] == "join_match":
                assert self.host
                self.add_player(Player(False))
                self.refresh()

                self.sio.emit("match", {
                    "code": self.match_code,
                    "status": "players",
                    "players": [i for i, _ in enumerate(self.players)]
                })
                self.match_size_x = min(self.match_size_x, data["size"][1])
                self.match_size_y = min(self.match_size_y, data["size"][0])
            elif data["status"] == "players":
                assert not self.host
                self.players = [Player(False) for _ in data["players"]]
                self.refresh()
            elif data["status"] == "start":
                assert not self.host
                self.finished = True

    def refresh(self):
        if self.finished:
            return

        h, w = self.screen.getmaxyx()

        self.player_wind.clear()
        self.player_wind.box()
        self.player_wind.refresh()
        self.display_players()

        if self.host:
            text = "Press (s) to start!"
        else:
            text = "Waiting for host to start..."

        self.screen.addstr(5, (w - len(text)) // 2, text)

        if self.match_code is not None:
            text2 = "Match code: {}".format(self.match_code)
            self.screen.addstr(6, (w - len(text2)) // 2, text2)

        self.screen.refresh()

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
        height, width = self.screen.getmaxyx()

        for i, wind in enumerate(self.players):
            wind = self.player_wind.derwin(0, width // len(self.players), 0,
                    (width // len(self.players)) * i)
            wind.box()
            wind.refresh()

            self.player_winds[i] = wind
            self.display_player(i)

    def handle_input(self, char):
        if char == ord("s") and self.host:
            self.sio.emit("match", {"code": self.match_code, "status": "start"})
            self.finished = True

    def run(self):
        self.refresh()
        while not self.finished:
            self.handle_input(self.screen.getch())
            curses.napms(100)
        game = Game(self.screen, self.sio, self.host, self.match_code, (self.match_size_x, self.match_size_y))
        game.run()
