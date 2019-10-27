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

fire = [[
"      *          ",
"        )        ",
"       (  )      ",  
"   '    )     '  ",
"    )     )      ",
"   (   /\   (    ",
"    ) // |   )   ",
" _ -;._/ \\-_._  ",
"(_;-// | \ \-'.\ ",
"( `.__ _  ___,') ",
" `'(_ )_)(_)_)'  ",
],[
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
]]

avatar1 = [
'  _O/     ',
'    \     ',
'    /\_   ',
'    \  `  ',
'    `     ',
]

avatar2 = [
"      ,   ",
"     /    ",
"  `\_\    ",
"      \   ",
"     /O\  ",
]

avatar3 = [   
"           ",   
"           ",
"      ,    ",
"   O/ /    ",
"   /\|/\.  ",
]

avatar4 = [
"     \O_  ",
"  ,/\/    ",
"    /     ",
"    \     ",
"    `     ",
]

blank_avatar = [
"          ",
"          ",
"          ",
"          ",
"          ",
]

AVATAR_WIDTH = 10
AVATAR_HEIGHT = 5 

finished = False
number_players = 0

def main(stdscr, game_code):
  global finished, number_players

  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.timeout(200)
  sh, sw = stdscr.getmaxyx()
  box = [[3, 3], [sh-3, sw-3]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

  curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

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

  AVATAR_X_POSITIONS = {
    1: [sw//2 - AVATAR_WIDTH//2],
    2: [sw//2 - AVATAR_WIDTH, sw//2],
    3: [sw//2 - AVATAR_WIDTH - AVATAR_WIDTH//2, sw//2 - AVATAR_WIDTH//2, sw//2 + AVATAR_WIDTH//2],
    4: [sw//2 - 2*AVATAR_WIDTH, sw//2 - AVATAR_WIDTH, sw//2, sw//2 + AVATAR_WIDTH],
  }

  motion = [4, 3]
  frame = 1

  game_code_msg = f'Game Code: {game_code}'
  start_msg = 'Press (s) to start!'
  add_msg = f'More players can join! ({number_players}/4)'
  full_msg = 'Lobby is full!'

  stdscr.addstr(sh//2 - 1, sw//2 - len(game_code_msg)//2, game_code_msg)
  stdscr.addstr(sh//2 + 1, sw//2 - len(start_msg)//2, start_msg)

  display_fire(stdscr, frame, sw, 'left')
  display_fire(stdscr, frame, sw, 'right')

  display_avatar( stdscr, avatar = avatar1, color = 1, num_players = 1, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
  
  while not finished:
    add_msg = f'More players can join! ({number_players}/4)'
    if number_players < 4:
      stdscr.addstr(sh//2 + 3, sw//2 - len(add_msg)//2, add_msg)
    elif number_players == 4:
      stdscr.addstr(sh//2 + 3, sw//2 - len(add_msg)//2, " "*len(add_msg))
      stdscr.addstr(sh//2 + 3, sw//2 - len(full_msg)//2, full_msg)

    key = stdscr.getch()
    if key == ord('s'):
      break
    
    if frame == 1:
      frame = 0
    elif frame == 0:
      frame = 1

    motion[0], motion[1] = motion[1], motion[0]

    display_fire(stdscr, frame, sw, 'left')
    display_fire(stdscr, frame, sw, 'right')

    clear_avatars(stdscr, sh, sw)

    if number_players == 1:
      display_avatar( stdscr, avatar = avatar1, color = 1, num_players = 1, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
    
    if number_players == 2:
      display_avatar( stdscr, avatar = avatar1, color = 1, num_players = 2, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar2, color = 2, num_players = 2, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

    if number_players == 3:
      display_avatar( stdscr, avatar = avatar1, color = 1, num_players = 3, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar2, color = 2, num_players = 3, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar3, color = 3, num_players = 3, player = 3, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

    if number_players == 4:
      display_avatar( stdscr, avatar = avatar1, color = 1, num_players = 4, player = 1, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar2, color = 2, num_players = 4, player = 2, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar3, color = 3, num_players = 4, player = 3, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)
      display_avatar( stdscr, avatar = avatar4, color = 4, num_players = 4, player = 4, positions = AVATAR_X_POSITIONS, sh = sh, motion = motion)

    stdscr.refresh()

  stdscr.getch()

def clear_avatars(stdscr, sh, sw):
  for i in range(AVATAR_HEIGHT + 2):
    stdscr.addstr(sh - 5 - AVATAR_HEIGHT + i, sw//2 - 2*AVATAR_WIDTH, " "*(4*AVATAR_WIDTH))


def display_avatar(stdscr, avatar, color, num_players, player, positions, sh, motion):
  stdscr.attron(curses.color_pair(color))
  counter = 0
  for line in avatar:
    if player % 2 == 0:
      stdscr.addstr(sh - motion[0] - AVATAR_HEIGHT + counter, positions[num_players][player - 1], line)
    else:
      stdscr.addstr(sh - motion[1] - AVATAR_HEIGHT + counter, positions[num_players][player - 1], line)
    counter += 1
  stdscr.attroff(curses.color_pair(color))
  
def display_fire(stdscr, fire_frame, sw, position):
  if fire_frame == 0:
    color = 5
  elif fire_frame == 1:
    color = 6
  stdscr.attron(curses.color_pair(color))
  counter = 1
  for line in fire[fire_frame]:
    if position == 'left':
      stdscr.addstr(counter + 5, sw//6 - len(line)//2, line)
      counter += 1
    else:
      stdscr.addstr(counter + 5, 5*(sw//6) - len(line)//2, line)
      counter += 1
  stdscr.attroff(curses.color_pair(color))

#curses.wrapper(main)
