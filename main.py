from networking import sio
import sys

if len(sys.argv) == 1:
    from src.landing_art.ascii_arcade import ascii_arcade_landing

from src.matchmaking import Matchmaking
from src.pong.game import Game
import curses, sys

def main(stdscr, match_code=None):
    match = Matchmaking(stdscr, sio, match_code)
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
            curses.wrapper(main, sys.argv[1])
    else:
        stdscr = curses.initscr()
        stdscr.erase()
        curses.start_color()
        stdscr.nodelay(True)
        curses.wrapper(main)
