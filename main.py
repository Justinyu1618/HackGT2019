from networking import sio
import sys

if len(sys.argv) == 1:
    from src.landing_art.ascii_arcade import ascii_arcade_landing

from src.matchmaking import Matchmaking
from src.pong.game import Game
import curses, sys

def main(stdscr, game, match_code=None):
    match = Matchmaking(stdscr, sio, game, match_code)
    match.run()

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        stdscr = curses.initscr()
        stdscr.nodelay(True)
        curses.wrapper(main, sys.argv[1], sys.argv[2])
    else:
        stdscr = curses.initscr()
        stdscr.erase()
        curses.start_color()
        stdscr.nodelay(True)
        curses.wrapper(main, sys.argv[1])
