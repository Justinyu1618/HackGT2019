import random, curses, time
from curses import textpad

art_lines = [\
'.______     ______   .__   __.   _______ ',
'|   _  \   /  __  \  |  \ |  |  /  _____|',
'|  |_)  | |  |  |  | |   \|  | |  |  __  ',
'|   ___/  |  |  |  | |  . `  | |  | |_ | ',
"|  |      |  `--'  | |  |\   | |  |__| | ",
'| _|       \______/  |__| \__|  \______| ',
]

def main(stdscr):
  curses.curs_set(0)

  sh, sw = stdscr.getmaxyx()
  box = [[3, 3], [sh-3, sw-3]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  counter = 1
  for line in art_lines:
    stdscr.addstr(counter + 5, sw//2 - len(line)//2, line)
    counter += 1

  stdscr.refresh()

  stdscr.getch()

curses.wrapper(main)