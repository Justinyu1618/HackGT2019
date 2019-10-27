import random, curses, time
from curses import textpad
from ascii_pics import *

def main(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.timeout(500)
  sh, sw = stdscr.getmaxyx()
  box = [[2, 2], [sh-2, sw-2]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

#   # Arcade Letters

#   stdscr.attron(curses.color_pair(1))
#   counter = 0
#   for line in arcade:
#     stdscr.addstr(3 + counter, sw//2 - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(1))

#   # Enter to start 

#   stdscr.attron(curses.color_pair(2))
#   counter = 0
#   for line in press_enter:
#     stdscr.addstr(sh//2 + counter, sw//2 - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

# # Helicopter

#   stdscr.attron(curses.color_pair(3))
#   counter = -3
#   for line in helicopter:
#     stdscr.addstr(3*(sh//4) + counter, sw//2 - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(3))

#   # Aliens

#   stdscr.attron(curses.color_pair(2))
#   counter = 2
#   for line in alien:
#     stdscr.addstr(3*(sh//4) + counter, sw//10 - len(line)//2 - 4, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   stdscr.attron(curses.color_pair(2))
#   counter = 3
#   for line in abduction:
#     stdscr.addstr(3*(sh//4) + counter, sw//6 - len(line)//2 - 3, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   stdscr.attron(curses.color_pair(3))
#   counter = 2
#   for line in alien:
#     stdscr.addstr(3*(sh//4) + counter, 2*(sw//10) - len(line)//2 + 5, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(3))

#   # Pacman

#   stdscr.attron(curses.color_pair(2))
#   counter = -2
#   for line in pacman:
#     stdscr.addstr(sh//8 + counter, 8*(sw//9) - len(line)//2 - 4, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   # Pokeball

#   stdscr.attron(curses.color_pair(2))
#   counter = 1
#   for line in pokeball:
#     stdscr.addstr(sh//3 + counter, (sw//8) - len(line)//2 - 1, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   # Pokeball

#   stdscr.attron(curses.color_pair(2))
#   counter = 1
#   for line in mario:
#     stdscr.addstr(sh//3 + counter, 7*(sw//8) - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   ## Space Invaders

#   # Player Ship

#   stdscr.attron(curses.color_pair(2))
#   counter = -1
#   for line in invader_player:
#     stdscr.addstr(sh//4 + counter, (sw//8) - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   # Alien Ship

#   stdscr.attron(curses.color_pair(2))
#   counter = -6
#   for line in invader_alien:
#     stdscr.addstr(sh//5 + counter, (sw//8) - len(line)//2 - 15, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   stdscr.attron(curses.color_pair(2))
#   counter = -7
#   for line in invader_alien2:
#     stdscr.addstr(sh//5 + counter, (sw//8) - len(line)//2, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

#   stdscr.attron(curses.color_pair(2))
#   counter = -6
#   for line in invader_alien:
#     stdscr.addstr(sh//5 + counter, (sw//8) - len(line)//2 + 15, line)
#     counter += 1
#   stdscr.attroff(curses.color_pair(2))

  # # Racecar

  # stdscr.attron(curses.color_pair(2))
  # counter = 4
  # for line in racecar:
  #   stdscr.addstr(4*(sh//5) + counter, (sw//3) - len(line)//2, line)
  #   counter += 1
  # stdscr.attroff(curses.color_pair(2))

  while 1:
    key = stdscr.getch()
    if key == ord('w'):
      break

    stdscr.refresh()

  stdscr.getch()
curses.wrapper(main)