import sys,os
import curses

DEFAULT_STATE = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class Board:

  def __init__(self, start_y = 0, start_x = 0, game = "dmegedsnrictrxmutkhwtiake", state = DEFAULT_STATE):
    self.cursor_y = 0
    self.cursor_x = 0
    self.game_str = game
    self.game_state = state
    self.start_y = start_y
    self.start_x = start_x


  def draw_frame(self, stdscr):
    current_line = self.start_y + 1

    stdscr.addstr(current_line, self.start_x, "┏━━━┳━━━┳━━━┳━━━┳━━━┓")
    current_line += 1

    for y in range(4):
      for x in range(6):
        stdscr.addstr(current_line, self.start_x + 4*x, "┃")
      current_line += 1
      stdscr.addstr(current_line, self.start_x, "┣━━━╋━━━╋━━━╋━━━╋━━━┫")
      current_line += 1

    for x in range(6):
      stdscr.addstr(current_line, self.start_x + 4*x, "┃")
    current_line += 1
    stdscr.addstr(current_line, self.start_x, "┗━━━┻━━━┻━━━┻━━━┻━━━┛")


  def tile_color(self, cursor_y, cursor_x):
    color_id = 0
    tile_state = self.game_state[5*cursor_y+cursor_x]

    if tile_state == 1:
      color_id = 1
    elif tile_state == -1:
      color_id = 3

    if color_id != 0 and self.surrounded(cursor_y, cursor_x):
      color_id += 1

    return color_id


  def surrounded(self, cursor_y, cursor_x):
    tile_state = self.game_state[5*cursor_y+cursor_x]
    
    for i in [-1, 1]:
      if cursor_y + i > 4 or cursor_y + i < 0:
        continue
      if self.game_state[5*(cursor_y+i)+cursor_x] != tile_state:
        return False
    
    for i in [-1, 1]:
      if cursor_x + i > 4 or cursor_x + i < 0:
        continue
      if self.game_state[5*(cursor_y)+cursor_x+i] != tile_state:
        return False

    return True


  def draw_tile(self, stdscr, cursor_y, cursor_x):
    center_y = self.start_y + 2 + cursor_y * 2
    center_x = self.start_x + 2 + cursor_x * 4
    color_id = self.tile_color(cursor_y, cursor_x)

    stdscr.attron(curses.color_pair(color_id))
    stdscr.addstr(center_y, center_x + 1, ' ')
    stdscr.addstr(center_y, center_x - 1, ' ')
    stdscr.addstr(center_y, center_x, self.game_str[5*cursor_y+cursor_x])
    stdscr.attroff(curses.color_pair(color_id))


  def move_cursor(self, stdscr, key):
    cursor_y = self.cursor_y
    cursor_x = self.cursor_x

    if key == ord('j'):
      cursor_y = cursor_y + 1
    elif key == ord('k'):
      cursor_y = cursor_y - 1
    elif key == ord('l'):
      cursor_x = cursor_x + 1
    elif key == ord('h'):
      cursor_x = cursor_x - 1

    cursor_x = max(0, cursor_x)
    cursor_x = min(4, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(4, cursor_y)

    stdscr.move(2 + 2 * cursor_y, 2 + 4 * cursor_x)
    
    self.cursor_y = cursor_y
    self.cursor_x = cursor_x


  def draw_title(self, stdscr):
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(self.start_y, self.start_x + 1, "Letterpress Console")
    stdscr.attroff(curses.A_BOLD)


  def generate_draw_func(self):
    def draw_func(stdscr):
      k = 0

      # Clear and refresh the screen for a blank canvas
      stdscr.clear()
      stdscr.refresh()

      # Start colors in curses
      curses.start_color()
      curses.init_pair(1, 12, curses.COLOR_BLACK) # bright blue
      curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
      curses.init_pair(3, 9, curses.COLOR_BLACK) # bright red
      curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

      # Loop where k is the last character pressed
      while (k != ord('q')):

        # Initialization
        stdscr.clear()

        self.draw_title(stdscr)

        # Rendering the board
        self.draw_frame(stdscr)
        for i in range(5):
          for j in range(5):
            self.draw_tile(stdscr, i, j)

        self.move_cursor(stdscr, k)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    return draw_func

def ui():
  board = Board(start_y = 0, start_x = 0, game = "dmegedsnrictrxmutkhwtiake")
  draw_func = board.generate_draw_func()
  curses.wrapper(draw_func)

if __name__ == "__main__":
  ui()
