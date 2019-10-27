import sys
import curses

from src.matchmaking import Matchmaking
from src.pong.game import Game


def main(stdscr, match_code=None):
    match = Matchmaking(stdscr, match_code)
    match.run()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        stdscr = curses.initscr()
        stdscr.nodelay(True)
        curses.wrapper(main, sys.argv[1])
    else:
        stdscr = curses.initscr()
        curses.start_color()
        stdscr.nodelay(True)
        curses.wrapper(main)
