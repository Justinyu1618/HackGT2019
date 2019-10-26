import random, curses, time
from curses import textpad

art_lines = [
'.______     ______   .__   __.   _______ ',
'|   _  \   /  __  \  |  \ |  |  /  _____|',
'|  |_)  | |  |  |  | |   \|  | |  |  __  ',
'|   ___/  |  |  |  | |  . `  | |  | |_ | ',
"|  |      |  `--'  | |  |\   | |  |__| | ",
'| _|       \______/  |__| \__|  \______| ',
]

instructions = [\
' ____          ',
'| -> | _  Move ',
'|____|    right',
' ____          ',
'| <- | _  Move ',
'|____|    left ',
]

instructions2 = [\
' ____          ',
'|ESC | _  Exit ',
'|____|         ',
]

fire = [
"      (          ",
"       )         ",
"      (  (       ",  
"          )      ",
"    (    (       ",
"     ) /\  )     ",
"   (  // | ( '   ",
" _ -.;_/ \\--._  ",
"(_;-// | \ \-'.\ ",
"( `.__ _  ___,') ",
" `'(_ )_)(_)_)'  ",
]

def main(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.timeout(75)
  sh, sw = stdscr.getmaxyx()
  box = [[3, 3], [sh-3, sw-3]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

  counter = 1
  for line in art_lines:
    stdscr.addstr(counter + 5, sw//2 - len(line)//2, line)
    counter += 1

  counter = 1
  for instruc in instructions:
    stdscr.addstr(counter + (sh - len(instructions) - 5), sw - len(instruc) - 5, instruc)
    counter += 1

  counter = 1
  for instruc2 in instructions2:
    stdscr.addstr(counter + (sh - len(instructions) - 2), len(instruc) - 10, instruc2)
    counter += 1

  stdscr.attron(curses.color_pair(3))
  counter = 1
  for line in fire:
    stdscr.addstr(counter + 5, sw//6 - len(line)//2, line)
    counter += 1

  counter = 1
  for line in fire:
    stdscr.addstr(counter + 5, 5*(sw//6) - len(line)//2, line)
    counter += 1  
  stdscr.attroff(curses.color_pair(3))


  paddle = '[=====]'
  clear_paddle = '       '

  start_msg = 'Press (s) to start!'

  top_paddle_position = sw//2 - len(paddle)//2
  bottom_paddle_position = sw//2 - len(paddle)//2

  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(sh//2, top_paddle_position, paddle)
  stdscr.attroff(curses.color_pair(1))

  stdscr.attron(curses.color_pair(2))
  stdscr.addstr(4*(sh//5), bottom_paddle_position, paddle)
  stdscr.attroff(curses.color_pair(2))

  stdscr.addstr(18*(sh//20), sw//2 - len(start_msg)//2, start_msg)

  LEFT_MAX = 2*(sw//5) - len(paddle)//2
  RIGHT_MAX = 3*(sw//5) - len(paddle)//2

  top_direction = 'LEFT'
  bottom_direction = 'RIGHT'
  
  while 1:
    key = stdscr.getch()
    stdscr.addstr(sh//2, top_paddle_position, clear_paddle)
    stdscr.addstr(4*(sh//5), bottom_paddle_position, clear_paddle)

    if top_paddle_position <= LEFT_MAX and top_direction == 'LEFT':
      top_direction = 'RIGHT'
    elif top_paddle_position >= RIGHT_MAX and top_direction == 'RIGHT':
      top_direction = 'LEFT'

    if bottom_paddle_position <= LEFT_MAX and bottom_direction == 'LEFT':
      bottom_direction = 'RIGHT'
    elif bottom_paddle_position >= RIGHT_MAX and bottom_direction == 'RIGHT':
      bottom_direction = 'LEFT'

    if top_direction == 'LEFT':
      top_paddle_position -= 1
    else:
      top_paddle_position += 1

    if bottom_direction == 'LEFT':
      bottom_paddle_position -= 1
    else:
      bottom_paddle_position += 1

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(sh//2, top_paddle_position, paddle)
    stdscr.attroff(curses.color_pair(1))

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(4*(sh//5), bottom_paddle_position, paddle)
    stdscr.attroff(curses.color_pair(2))

    stdscr.refresh()

  stdscr.getch()

curses.wrapper(main)