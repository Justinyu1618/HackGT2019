from src.networking import sio
import sys
from src.menu import Menu
from src.matchmaking import Matchmaking
from src.pong.game import Game as Pong 
from src.tron.game import Game as Tron
from src.terminal_blackjack.game import Game as Blackjack
import curses, sys
from src.terminal_blackjack import Matchmaking as Matchmaking_BJ


def main(stdscr, match_code=None):
    from src.landing_art.ascii_arcade import ascii_arcade_landing

    match_tron = Matchmaking(stdscr, sio, Tron, match_code)
    match_pong = Matchmaking(stdscr, sio, Pong, match_code)
    # match_blackjack = Matchmaking_BJ(stdscr, sio, match_code)

    stdscr.clear()
    stdscr.timeout(-1)
    curses.curs_set(0)                                                   
    main_menu_items = [                                                  
            ('pong', match_pong.run),#match_pong.run),                                       
            ('tron', match_tron.run),#match_tron.run),                                     
            ('blackjack', lambda :print("LOL"))                                 
            ]                                                            
    main_menu = Menu(main_menu_items, stdscr)                   
    main_menu.display()
    while(True):
        try:
            key = stdscr.getch()
            if key == ord("0"):
                stdscr.clear()
                match_pong.run()
            elif key == ord("1"):
                stdscr.clear()
                match_tron.run()
            # elif key == ord("2"):
            #     stdscr.clear()
            #     match_blackjack.run()
        except KeyboardInterrupt:
            continue
    

    

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
        # stdscr.nodelay(True)
        curses.wrapper(main)
