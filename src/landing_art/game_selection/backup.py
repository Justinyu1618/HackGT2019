import time
import curses
from curses import textpad
from pics import *

menu = ['TRON', 'PONG', 'BLACKJACK']

def print_menu(stdscr, current_row_idx):
  stdscr.clear()
  h, w = stdscr.getmaxyx()

  for idx, row in enumerate(menu):
    x = w//2 - len(row)//2
    y = h//2 - len(menu)//2 + idx
    if idx == current_row_idx:
      stdscr.attron(curses.color_pair(1))
      stdscr.addstr(y, x, row)
      stdscr.attroff(curses.color_pair(1))
    else:
      stdscr.addstr(y, x, row)

  stdscr.refresh()

def main(stdscr):
  curses.curs_set(0)
  sh, sw = stdscr.getmaxyx()

  box = [[2, 2], [sh-2, sw-2]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
  
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
  
  draw_pic(stdscr, picture = game_selection, y = 3, x = sw//2, color = 4, counter = 0, extra=[0, 0] )

  current_row_idx = 0

  print_menu(stdscr, current_row_idx)

  while 1:
    key = stdscr.getch()

    stdscr.clear()

    if key == curses.KEY_UP and current_row_idx > 0:
      current_row_idx -= 1
    elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
      current_row_idx += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
      stdscr.addstr(14, 52, "You press {}".format(menu[current_row_idx])) 
      stdscr.refresh()
      stdscr.getch()
      if current_row_idx == len(menu) - 1:
        break

    print_menu(stdscr, current_row_idx)
    
    stdscr.refresh()

# Draw Picture
def draw_pic(stdscr, picture, y, x, color, counter, extra = [0,0]):
  stdscr.attron(curses.color_pair(color))
  count_step = counter
  for line in picture:
    # stdscr.addstr(y + count_step + extra[0], x - len(line)//2 + extra[1], line)
    stdscr.addstr(y + count_step + extra[0], x - len(line) + extra[1], line)
    count_step += 1
  stdscr.attroff(curses.color_pair(color))

curses.wrapper(main)
