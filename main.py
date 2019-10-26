from networking import sio

from src.matchmaking import Matchmaking
from src.pong.game import Game
import curses, sys

def run_host(stdscr):
    game = Game(stdscr, sio, host=True)
    game.run()

def run_client(stdscr):
    game = Game(stdscr, sio, host=False)
    game.run()

def main(stdscr):
    match = Matchmaking(stdscr, sio)
    match.run()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "host":
            curses.wrapper(run_host)
        elif sys.argv[1] == "client":
            curses.wrapper(run_client)
    else:
        stdscr = curses.initscr()
        stdscr.nodelay(True)
        curses.wrapper(main)
