from networking import sio

from src.tron.game import Game
import curses, sys, uuid

from src.landing_art.pong.pong_host import *

MAX_PLAYERS = 4

class Player:

    def __init__(self, sid, host):
        self.sid = sid
        self.host = host

    def serialize(self):
        return {k: v for k, v in self.__dict__.items()}

    def populate(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

class Matchmaking:

    def __init__(self, stdscr, sio, match_code=None):
        if match_code is None:
            self.match_code = str(uuid.uuid4())[:4]
            self.host = True
        else:
            self.match_code = match_code
            self.host = False

        self.sio = sio

        self.screen = stdscr
        self.H = curses.LINES
        self.W = curses.COLS

        self.players = []

        self.match_size_y, self.match_size_x = self.screen.getmaxyx()

        self.sio.start(self.on_connect, self.on_receive_data)

        self.finished = False
        self.sid = None

    def on_connect(self):
        if self.host:
            self.sio.emit("match", {"code": self.match_code, "status": "new_match"})
        else:
            self.sio.emit("match", {"code": self.match_code, "status": "join_match", "size": (self.screen.getmaxyx())})

    def on_receive_data(self, event, data):
        if event == "info":
            self.sid = data["sid"]
            self.add_player(Player(self.sid, True))
        elif event == "match" and data["code"] == self.match_code:
            if data["status"] == "join_match":
                assert self.host
                self.add_player(Player(data["sid"], False))

                self.sio.emit("match", {
                    "code": self.match_code,
                    "status": "players",
                    "players": [x.serialize() for x in self.players]
                })

                self.match_size_x = min(self.match_size_x, data["size"][1])
                self.match_size_y = min(self.match_size_y, data["size"][0])
            elif data["status"] == "players":
                assert not self.host
                self.players = []

                for p in data["players"]:
                    player = Player(None, None)
                    player.populate(p)
                    self.players.append(player)
            elif data["status"] == "start":
                assert not self.host
                self.finished = True

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            return

        self.players.append(player)

    def handle_input(self, char):
        if char == ord("s") and self.host:
            self.sio.emit("match", {"code": self.match_code, "status": "start"})
            self.finished = True

    def run(self):
        curses.curs_set(0)
        self.screen.nodelay(1)
        self.screen.timeout(200)
        sh, sw = self.screen.getmaxyx()
        box = [[3, 3], [sh-3, sw-3]]
        textpad.rectangle(self.screen, box[0][0], box[0][1], box[1][0], box[1][1])

        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)

        curses.init_pair(5, curses.COLOR_CYAN, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)

        counter = 1
        for line in art_lines:
            self.screen.addstr(counter + 5, sw//2 - len(line)//2, line)
            counter += 1

        counter = 1
        for instruc in instructions:
            self.screen.addstr(counter + (sh - len(instructions) - 5), sw - len(instruc) - 5, instruc)
            counter += 1

        counter = 1
        for instruc2 in instructions2:
            self.screen.addstr(counter + (sh - len(instructions) - 2), len(instruc) - 10, instruc2)
            counter += 1

        AVATAR_X_POSITIONS = {
            1: [sw//2 - AVATAR_WIDTH//2],
            2: [sw//2 - AVATAR_WIDTH, sw//2],
            3: [sw//2 - AVATAR_WIDTH - AVATAR_WIDTH//2, sw//2 - AVATAR_WIDTH//2, sw//2 + AVATAR_WIDTH//2],
            4: [sw//2 - 2*AVATAR_WIDTH, sw//2 - AVATAR_WIDTH, sw//2, sw//2 + AVATAR_WIDTH],
        }

        motion = [4, 3]
        frame = 1

        game_code_msg = f'Game Code: {self.match_code}'
        start_msg = 'Press (s) to start!'
        add_msg = f'More players can join! ({len(self.players)}/4)'
        full_msg = 'Lobby is full!'

        self.screen.addstr(sh//2 - 1, sw//2 - len(game_code_msg)//2, game_code_msg)
        self.screen.addstr(sh//2 + 1, sw//2 - len(start_msg)//2, start_msg)

        display_fire(self.screen, frame, sw, 'left')
        display_fire(self.screen, frame, sw, 'right')

        display_avatar( self.screen, avatar = avatar1, color = 1, num_players = 1, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
        
        while 1:
            add_msg = f'More players can join! ({len(self.players)}/4)'
            if len(self.players) < 4:
                self.screen.addstr(sh//2 + 3, sw//2 - len(add_msg)//2, add_msg)
            elif len(self.players) == 4:
                self.screen.addstr(sh//2 + 3, sw//2 - len(add_msg)//2, " "*len(add_msg))
                self.screen.addstr(sh//2 + 3, sw//2 - len(full_msg)//2, full_msg)

            if frame == 1:
                frame = 0
            elif frame == 0:
                frame = 1

            motion[0], motion[1] = motion[1], motion[0]

            display_fire(self.screen, frame, sw, 'left')
            display_fire(self.screen, frame, sw, 'right')

            clear_avatars(self.screen, sh, sw)

            if len(self.players) == 1:
                display_avatar( self.screen, avatar = avatar1, color = 1, num_players = 1, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
            
            if len(self.players) == 2:
                display_avatar( self.screen, avatar = avatar1, color = 1, num_players = 2, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar2, color = 2, num_players = 2, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

            if len(self.players) == 3:
                display_avatar( self.screen, avatar = avatar1, color = 1, num_players = 3, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar2, color = 2, num_players = 3, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar3, color = 3, num_players = 3, player = 3, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

            if len(self.players) == 4:
                display_avatar( self.screen, avatar = avatar1, color = 1, num_players = 4, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar2, color = 2, num_players = 4, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar3, color = 3, num_players = 4, player = 3, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
                display_avatar( self.screen, avatar = avatar4, color = 4, num_players = 4, player = 4, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

            self.handle_input(self.screen.getch())
            curses.napms(150)
            self.screen.refresh()

            if self.finished:
                self.screen.erase()
                game = Game(self.screen, self.sio, self.host, self.match_code,
                        self.sid, self.players, (self.match_size_x, self.match_size_y))
                game.run()
                self.screen.erase()
                self.sio.update_callbacks(self.on_connect, self.on_receive_data)
                self.finished = False
                break

        self.run()
