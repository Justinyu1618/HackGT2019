import random, curses, time
from curses import textpad

def main(stdscr):
  curses.curs_set(0)

  sh, sw = stdscr.getmaxyx()
  box = [[3, 3], [sh-3, sw-3]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  art_lines = []
  f = open("pong.txt", "r")
  f1 = f.readlines()
  for line in f1:
    art_lines.push(line)

  for i in len(art_lines):
    stdscr.stradd(i, sw//2 - len(art_lines[i])//2, art_lines[i])
  
  stdscr.refresh()

  stdscr.getch()

curses.wrapper(main)