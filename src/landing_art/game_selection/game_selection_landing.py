import random, curses, time
from curses import textpad
from pics import *

menu = [tron, pong, blackjack]

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
  curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

  draw_pic(stdscr, picture = game_selection, y = 3, x = sw//2, color = 4, counter = 0, extra=[0, 0] )

  current_row_idx = 0
  print_menu(stdscr, current_row_idx)

  while 1:
    key = stdscr.getch()
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

  stdscr.getch()

# Print Menu
def print_menu(stdscr, current_row_idx):
  sh, sw = stdscr.getmaxyx()

  counter = 1
  for pic in menu:
    x_pos = sw//2 - len(pic[0])//2
    y_pos = len(game_selection) + 5 + counter*5
    if counter == current_row_idx:
      stdscr.attron(curses.color_pair(7))
      draw_pic(stdscr, picture = pic, y = y_pos, x = x_pos, color = 2, counter = 0)
      stdscr.attroff(curses.color_pair(7))
    else:
      draw_pic(stdscr, picture = pic, y = y_pos, x = x_pos, color = 2, counter = 0)

    counter += 1
    stdscr.refresh()

# Draw Picture
def draw_pic(stdscr, picture, y, x, color, counter, extra = [0,0]):
  stdscr.attron(curses.color_pair(color))
  count_step = counter
  for line in picture:
    # stdscr.addstr(y + count_step + extra[0], x - len(line)//2 + extra[1], line)
    stdscr.addstr(y - count_step, x - len(line)//2, line)
    count_step += 1
  stdscr.attroff(curses.color_pair(color))

# Clear Picture
def clear_pic(stdscr, picture, y, x, counter, extra = [0,0]):
  count_step = counter
  for line in picture:
    stdscr.addstr(y + count_step + extra[0], x - len(line)//2 + extra[1], " "*len(line))
    count_step += 1

curses.wrapper(main)