from networking import sio
from networking.delegate import NetworkingDelegate

from src.pong.game import Game
import curses, sys

def run_host(stdscr):
    game = Game(stdscr, sio, host=True)
    game.run()

def run_client(stdscr):
    game = Game(stdscr, sio, host=False)
    game.run()


if __name__ == '__main__':
    if sys.argv[1] == "host":
        curses.wrapper(run_host)
    elif sys.argv[1] == "client":
        curses.wrapper(run_client)