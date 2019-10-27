import random, curses, time
from curses import textpad
from pics import *

def main(stdscr):
  curses.curs_set(0)
  sh, sw = stdscr.getmaxyx()
  box = [[2, 2], [sh-2, sw-2]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

  draw_pic(stdscr, picture = game_selection, y = 3, x = sw//2, color = 4, counter = 0, extra=[0, 0] )

  while 1:
    key = stdscr.getch()
    if key == ord('w'):
      break

    stdscr.refresh()

  stdscr.getch()

# Draw Picture
def draw_pic(stdscr, picture, y, x, color, counter, extra = [0,0]):
  stdscr.attron(curses.color_pair(color))
  count_step = counter
  for line in picture:
    stdscr.addstr(y + count_step + extra[0], x - len(line)//2 + extra[1], line)
    count_step += 1
  stdscr.attroff(curses.color_pair(color))

# Clear Picture
def clear_pic(stdscr, picture, y, x, counter, extra = [0,0]):
  count_step = counter
  for line in picture:
    stdscr.addstr(y + count_step + extra[0], x - len(line)//2 + extra[1], " "*len(line))
    count_step += 1

curses.wrapper(main)