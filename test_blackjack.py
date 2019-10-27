from networking import sio

from src.terminal_blackjack import Matchmaking
from src.terminal_blackjack.game import Game
import curses, sys, uuid
from src.terminal_blackjack.src.constants import init_colors

MAX_PLAYERS = 4

def main(stdscr, match_code=None):
    init_colors()
    match = Matchmaking(stdscr, sio, match_code)
    match.run()

if __name__ == '__main__':
    if(len(argv) == 2):
        curses.wrapper(main, sys.argv[1])
    else:
        stdscr = curses.initscr()
        stdscr.nodelay(True)
        curses.wrapper(main)
