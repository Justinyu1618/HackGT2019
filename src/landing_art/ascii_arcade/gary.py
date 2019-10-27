import random, curses, time
from curses import textpad
from pics import *

MAX_FRAME = 12
MAX_CAR_FRAME = 36

def main(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(1)
  stdscr.timeout(250)
  sh, sw = stdscr.getmaxyx()
  box = [[2, 2], [sh-2, sw-2]]
  textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
  curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


  # Arcade Letters

  stdscr.attron(curses.color_pair(1))
  counter = 0
  for line in arcade:
    stdscr.addstr(3 + counter, sw//2 - len(line)//2, line)
    counter += 1
  stdscr.attroff(curses.color_pair(1))

  frame = 1
  car_frame = 1

  # Enter to start 
  display_press_enter(stdscr, sh, sw, frame)

# Helicopter

  display_helicopter(stdscr, sh, sw, frame)

  # Alien abduction
  
  display_alien_left(stdscr, sh, sw, frame)
  display_alien_abduction(stdscr, sh, sw, frame)
  display_alien_right(stdscr, sh, sw, frame)

  # Pacman

  stdscr.attron(curses.color_pair(4))
  counter = -2
  for line in pacman:
    stdscr.addstr(sh//8 + counter, 8*(sw//9) - len(line)//2 - 4, line)
    counter += 1
  stdscr.attroff(curses.color_pair(4))

  # Pokeball

  stdscr.attron(curses.color_pair(2))
  counter = 1
  for line in pokeball:
    stdscr.addstr(sh//3 + counter, (sw//8) - len(line)//2 - 1, line)
    counter += 1
  stdscr.attroff(curses.color_pair(2))

  # Mario

  display_mario(stdscr, sh, sw, frame)

  ## Space Invaders

  # Player Ship

  stdscr.attron(curses.color_pair(4))
  counter = -1
  for line in invader_player:
    stdscr.addstr(sh//4 + counter, (sw//8) - len(line)//2, line)
    counter += 1
  stdscr.attroff(curses.color_pair(4))

  # Alien Ships
  display_alien_invader_left(stdscr, sh, sw, frame)
  display_alien_invader_middle(stdscr, sh, sw, frame)
  display_alien_invader_right(stdscr, sh, sw, frame)

  # Racecar

  # stdscr.attron(curses.color_pair(2))
  # counter = 4
  # for line in racecar:
  #   stdscr.addstr(4*(sh//5) + counter, (sw//3) - len(line)//2, line)
  #   counter += 1
  # stdscr.attroff(curses.color_pair(2))

  display_car(stdscr, sh, sw, car_frame)

  while 1:
    key = stdscr.getch()
    if key == 10:#ord('w'):
      break

    if frame < MAX_FRAME:
      frame += 1
    elif frame == MAX_FRAME:
      frame = 1

    if car_frame < MAX_CAR_FRAME:
      car_frame += 1
    elif car_frame == MAX_CAR_FRAME:
      car_frame = 1

    # Press enter
    display_press_enter(stdscr, sh, sw, frame)

    # Helicopter
    display_helicopter(stdscr, sh, sw, frame)

    # Alien abduction
    display_alien_left(stdscr, sh, sw, frame)
    display_alien_right(stdscr, sh, sw, frame)
    display_alien_abduction(stdscr, sh, sw, frame)

    # Mario
    display_mario(stdscr, sh, sw, frame)

    # Space invaders
    display_alien_invader_left(stdscr, sh, sw, frame)
    display_alien_invader_middle(stdscr, sh, sw, frame)
    display_alien_invader_right(stdscr, sh, sw, frame)

    # Race Car
    display_car(stdscr, sh, sw, car_frame)

    stdscr.refresh()

  stdscr.getch()


## Animations ##

# Press Enter

def display_press_enter(stdscr, sh, sw, frame):
  step_count = 0
  if frame in [1, 2, 3, 6, 7, 8]:
    draw_pic(stdscr, picture = press_enter, y = sh//2, x = sw//2, color = 2, counter = step_count)
  else:
    clear_pic(stdscr, picture = press_enter, y = sh//2, x = sw//2, counter = step_count)

# Helicopter

def display_helicopter(stdscr, sh, sw, frame):
  step_count = -3
  if frame in [1, 4, 7, 10]:
    clear_pic(stdscr, picture = helicopter3, y = 3*(sh//4), x = sw//2, counter = step_count, extra = [0, 0])
    draw_pic(stdscr, picture = helicopter1, y = 3*(sh//4), x = sw//2, color = 5, counter = step_count, extra = [0, 0])
  elif frame in [2, 5, 8, 11]:
    clear_pic(stdscr, picture = helicopter1, y = 3*(sh//4), x = sw//2, counter = step_count, extra = [0, 0])
    draw_pic(stdscr, picture = helicopter2, y = 3*(sh//4), x = sw//2, color = 5, counter = step_count, extra = [0, 0])
  else:
    clear_pic(stdscr, picture = helicopter2, y = 3*(sh//4), x = sw//2, counter = step_count, extra = [0, 0])
    draw_pic(stdscr, picture = helicopter3, y = 3*(sh//4), x = sw//2, color = 5, counter = step_count, extra = [0, 0])

# Alien abduction

# Left Alien
def display_alien_left(stdscr, sh, sw, frame):
  step_count = 2
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = alien, y = 3*(sh//4), x = sw//10, counter = step_count, extra = [-1, -5])
    draw_pic(stdscr, picture = alien, y = 3*(sh//4), x = sw//10, color = 6, counter = step_count, extra = [0, -5])
  else:
    clear_pic(stdscr, picture = alien, y = 3*(sh//4), x = sw//10, counter = step_count, extra = [0, -5])
    draw_pic(stdscr, picture = alien, y = 3*(sh//4), x = sw//10, color = 6, counter = step_count, extra = [-1, -5])

# Abduction
def display_alien_abduction(stdscr, sh, sw, frame):
  step_count = 0
  draw_pic(stdscr, picture = abduction, y = 3*(sh//4), x = sw//6, color = 5, counter = step_count, extra = [3, -4])

# Right Alien
def display_alien_right(stdscr, sh, sw, frame):
  step_count = 2
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = alien, y = 3*(sh//4), x = 2*sw//10, counter = step_count, extra = [0, 5])
    draw_pic(stdscr, picture = alien, y = 3*(sh//4), x = 2*sw//10, color = 6, counter = step_count, extra = [-1, 5])
  else:
    clear_pic(stdscr, picture = alien, y = 3*(sh//4), x = 2*sw//10, counter = step_count, extra = [-1, 5])
    draw_pic(stdscr, picture = alien, y = 3*(sh//4), x = 2*(sw//10), color = 6, counter = step_count, extra = [0, 5])

# Mario
def display_mario(stdscr, sh, sw, frame):
  step_count = 4
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = mario, y = sh//3, x = 7*(sw//8), counter = step_count, extra = [0, 0])
    draw_pic(stdscr, picture = mario, y = sh//3, x = 7*(sw//8), color = 3, counter = step_count, extra = [-2, 0])
  else:
    clear_pic(stdscr, picture = mario, y = sh//3, x = 7*(sw//8), counter = step_count, extra = [-2, 0])
    draw_pic(stdscr, picture = mario, y = sh//3, x = 7*(sw//8), color = 3, counter = step_count, extra = [0, 0])

# Space invaders
# Left Alien Invader
def display_alien_invader_left(stdscr, sh, sw, frame):
  step_count = -6
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, counter = step_count, extra = [-1, -15])
    draw_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [0, -15])
  else:
    clear_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, counter = step_count, extra = [0, -15])
    draw_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [-1, -15])

def display_alien_invader_middle(stdscr, sh, sw, frame):
  step_count = -6
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, counter = step_count, extra = [0, 0])
    draw_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [-1, 0])
  else:
    clear_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, counter = step_count, extra = [-1, 0])
    draw_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [0, 0])

# Right Alien Invader
def display_alien_invader_right(stdscr, sh, sw, frame):
  step_count = -6
  if frame in [1, 2, 3, 7, 8, 9]:
    clear_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, counter = step_count, extra = [-1, 15])
    draw_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [0, 15])
  else:
    clear_pic(stdscr, picture = invader_alien, y = sh//5, x = sw//8, counter = step_count, extra = [0, 15])
    draw_pic(stdscr, picture = invader_alien2, y = sh//5, x = sw//8, color = 4, counter = step_count, extra = [-1, 15])

# Race car
def display_car(stdscr, sh, sw, car_frame):
  step_count = 4

  clear_pic(stdscr, picture = racecar, y = 4*(sh//5), x = sw//3, counter = step_count, extra = [0, 2*car_frame - 2])
  draw_pic(stdscr, picture = racecar, y = 4*(sh//5), x = sw//3, color = 4, counter = step_count, extra = [0, 2*car_frame])
  if car_frame == 1:
    clear_pic(stdscr, picture = racecar, y = 4*(sh//5), x = sw//3, counter = step_count, extra = [0, 2*MAX_CAR_FRAME])

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
