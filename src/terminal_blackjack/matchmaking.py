from networking import sio
from .src.constants import *
from .game import Game, PlayerInterface
from .src.objects import Player
from .src.display_util import DisplayTable, PartitionManager
import curses, sys, uuid

MAX_PLAYERS = 4

# class Player:

#     def __init__(self, host):
#         self.host = host

class Matchmaking:

    def __init__(self, stdscr, sio, match_code=None):
        self.sio = sio
        self.display = DisplayTable(stdscr)
        self.display.render()
        self.screen = stdscr
        self.H = curses.LINES
        self.W = curses.COLS

        self.player = None
        self.players = []
        # self.player_wind = stdscr.derwin(self.H // 2, self.W, self.H // 2, 0)
        # self.player_wind.box()

        self.player_winds = {}

        self.host = match_code is None

        if match_code is None:
            self.player = Player(True, player_num=1)
            self.add_player(self.player)

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
        self.display.draw_players()

    def on_receive_data(self, event, data):
        if event == "match" and data["code"] == self.match_code:
            if data["status"] == "join_match":
                assert self.host
                new_player = Player(False,player_num=len(self.players)+1)
                self.add_player(new_player)
                self.refresh()
                # self.display.draw_players()

                self.sio.emit("match", {
                    "code": self.match_code,
                    "status": "players",
                    "players": [(i,p) for i, p in enumerate([p.serialize() for p in self.players])],
                    "new_player": new_player.serialize() 
                })
                self.match_size_x = min(self.match_size_x, data["size"][1])
                self.match_size_y = min(self.match_size_y, data["size"][0])
            elif data["status"] == "players":
                assert not self.host
                self.players = [Player(False, player_num=i).populate(p) for i,p in data["players"]]
                self.display.add_players_from_list(self.players)
                self.refresh()
                if self.player is None:
                    self.player = data["new_player"]
            elif data["status"] == "start":
                assert not self.host
                self.finished = True
                self.screen.refresh()

    def refresh(self):
        if self.finished:
            return

        h, w = self.screen.getmaxyx()

        # self.player_wind.clear()
        # self.player_wind.box()
        # self.player_wind.refresh()
        # self.display.draw_players()

        if self.host:
            text = "Press (s) to start!"
        else:
            text = "Waiting for host to start..."

        self.screen.addstr(5, (w - len(text)) // 2, text)

        if self.match_code is not None:
            text2 = "Match code: {}".format(self.match_code)
            self.screen.addstr(6, (w - len(text2)) // 2, text2)
        self.screen.refresh()

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            return
        self.players.append(player)
        self.display.add_player(player)
        
    def handle_input(self, char):
        if char == ord("s") and self.host:
            self.sio.emit("match", {"code": self.match_code, "status": "start"})
            self.finished = True

    def run(self):
        self.refresh()
        while not self.finished:
            self.handle_input(self.screen.getch())
            curses.napms(100)
        if self.host:
            game = Game(self.screen, self.sio, self.host, self.match_code, self.player)
            game.players = self.players
            game.display = self.display
            game.run()
        else:
            self.screen.addstr(10,10,"HELLO")
            playint = PlayerInterface(self.screen, self.sio, self.match_code, self.player)
            playint.display = self.display
            playint.run()
            



def main(stdscr, match_code=None):
    init_colors()
    match = Matchmaking(stdscr, sio, match_code)
    match.run()

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.wrapper(main)
