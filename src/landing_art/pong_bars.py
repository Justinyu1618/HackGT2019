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
  stdscr.timeout(400)
  sh, sw = stdscr.getmaxyx()
  box = [[3, 3], [sh-3, sw-3]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

  curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

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

  stdscr.attron(curses.color_pair(5))
  counter = 1
  for line in fire:
    stdscr.addstr(counter + 5, sw//6 - len(line)//2, line)
    counter += 1

  counter = 1
  for line in fire:
    stdscr.addstr(counter + 5, 5*(sw//6) - len(line)//2, line)
    counter += 1  
  stdscr.attroff(curses.color_pair(5))


  paddle = '[=====]'
  clear_paddle = '       '

  vertical_paddle = [
  '--',
  '||',
  '||',
  '||',
  "--"
  ]

  clear_vertical_paddle = [
  '    ',
  '    ',
  '    ',
  '    ',
  '    ',
  "    "
  ]

  start_msg = 'Press (s) to start!'

  top_paddle_position = sw//2 - len(paddle)//2
  bottom_paddle_position = sw//2 - len(paddle)//2

  left_paddle_position = 18*(sh//20) + 1
  right_paddle_position = 18*(sh//20) + 1

  stdscr.attron(curses.color_pair(1))
  stdscr.addstr(sh//2, top_paddle_position, paddle)
  stdscr.attroff(curses.color_pair(1))

  stdscr.attron(curses.color_pair(2))
  stdscr.addstr(4*(sh//5), bottom_paddle_position, paddle)
  stdscr.attroff(curses.color_pair(2))

  counter = 0
  stdscr.attron(curses.color_pair(3))
  for line_left in vertical_paddle:
    stdscr.addstr(left_paddle_position - len(vertical_paddle)//2 + counter, 1*(sw//3), line_left)
    counter += 1
  stdscr.attroff(curses.color_pair(3))

  counter = 0
  stdscr.attron(curses.color_pair(4))
  for line_right in vertical_paddle:
    stdscr.addstr(right_paddle_position - len(vertical_paddle)//2 + counter, 2*(sw//3), line_right)
    counter += 1
  stdscr.attroff(curses.color_pair(4))

  stdscr.addstr(18*(sh//20), sw//2 - len(start_msg)//2, start_msg)

  LEFT_MAX = 2*(sw//5) - len(paddle)//2
  RIGHT_MAX = 3*(sw//5) - len(paddle)//2

  TOP_MAX = sh//2 - 5
  BOTTOM_MAX = 4*(sh//5) + 5

  top_direction = 'LEFT'
  bottom_direction = 'RIGHT'
  left_direction = 'UP'
  right_direction = 'DOWN'

  number_players = 1
  
  while 1:
    key = stdscr.getch()
    if key == ord('s'):
      break

    stdscr.addstr(sh//2, top_paddle_position, clear_paddle)
    stdscr.addstr(4*(sh//5), bottom_paddle_position, clear_paddle)

    counter = 0
    stdscr.attron(curses.color_pair(3))
    for line_left in clear_vertical_paddle:
      stdscr.addstr(left_paddle_position - len(vertical_paddle)//2 + counter, 1*(sw//3), line_left)
      counter += 1
    stdscr.attroff(curses.color_pair(3))

    counter = 0
    stdscr.attron(curses.color_pair(4))
    for line_right in clear_vertical_paddle:
      stdscr.addstr(right_paddle_position - len(vertical_paddle)//2 + counter, 2*(sw//3), line_right)
      counter += 1
    stdscr.attroff(curses.color_pair(4))

    # stdscr.addstr(left_paddle_position, 1*(sw//3), clear_vertical_paddle)
    # stdscr.addstr(right_paddle_position, 2*(sw//3), clear_vertical_paddle)

    if top_paddle_position <= LEFT_MAX and top_direction == 'LEFT':
      top_direction = 'RIGHT'
    elif top_paddle_position >= RIGHT_MAX and top_direction == 'RIGHT':
      top_direction = 'LEFT'

    if bottom_paddle_position <= LEFT_MAX and bottom_direction == 'LEFT':
      bottom_direction = 'RIGHT'
    elif bottom_paddle_position >= RIGHT_MAX and bottom_direction == 'RIGHT':
      bottom_direction = 'LEFT'

    if left_paddle_position <= BOTTOM_MAX and left_direction == 'DOWN':
      left_direction = 'UP'
    elif left_paddle_position >= TOP_MAX and left_direction == 'UP':
      left_direction = 'DOWN'

    if right_paddle_position <= BOTTOM_MAX and right_direction == 'DOWN':
      right_direction = 'UP'
    elif right_paddle_position >= TOP_MAX and right_direction == 'UP':
      right_direction = 'DOWN'

    if top_direction == 'LEFT':
      top_paddle_position -= 1
    else:
      top_paddle_position += 1

    if bottom_direction == 'LEFT':
      bottom_paddle_position -= 1
    else:
      bottom_paddle_position += 1

    if left_direction == 'DOWN':
      left_paddle_position += 1
    else:
      left_paddle_position -= 1

    if right_direction == 'DOWN':
      right_paddle_position += 1
    else:
      right_paddle_position -= 1

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(sh//2, top_paddle_position, paddle)
    stdscr.attroff(curses.color_pair(1))

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(4*(sh//5), bottom_paddle_position, paddle)
    stdscr.attroff(curses.color_pair(2))

    # stdscr.attron(curses.color_pair(3))
    # stdscr.addstr(left_paddle_position, 1*(sw//3), vertical_paddle)
    # stdscr.attroff(curses.color_pair(3))

    counter = 0
    stdscr.attron(curses.color_pair(3))
    for line_left in vertical_paddle:
      stdscr.addstr(left_paddle_position - len(vertical_paddle)//2 + counter, 1*(sw//3), line_left)
      counter += 1
    stdscr.attroff(curses.color_pair(3))

    # stdscr.attron(curses.color_pair(4))
    # stdscr.addstr(right_paddle_position, 2*(sw//3), vertical_paddle)
    # stdscr.attroff(curses.color_pair(4))

    counter = 0
    stdscr.attron(curses.color_pair(4))
    for line_right in vertical_paddle:
      stdscr.addstr(right_paddle_position - len(vertical_paddle)//2 + counter, 2*(sw//3), line_right)
      counter += 1
    stdscr.attroff(curses.color_pair(4))

    stdscr.refresh()

  stdscr.getch()

curses.wrapper(main)