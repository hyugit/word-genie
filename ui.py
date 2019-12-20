import sys,os
import curses
import datetime
import fnmatch
from states import GameStates


class GameUI:

  def __init__(self, state, start_y = 0, start_x = 0):
    self.cursor_y = 0
    self.cursor_x = 0
    self.game_state = state
    self.start_y = start_y
    self.start_x = start_x


  def draw_frame(self, stdscr):
    current_line = self.start_y + 2

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
    tile_state = self.game_state.get_tile_state(cursor_y, cursor_x)

    if tile_state == 1:
      color_id = 1
    elif tile_state == -1:
      color_id = 3

    if color_id != 0 and self.game_state.is_protected_tile(cursor_y, cursor_x):
      color_id += 1

    return color_id


  def draw_tile(self, stdscr, y, x):
    center_y = self.start_y + 3 + y * 2
    center_x = self.start_x + 2 + x * 4
    color_id = self.tile_color(y, x)

    stdscr.attron(curses.color_pair(color_id))
    stdscr.addstr(center_y, center_x + 1, ' ')
    stdscr.addstr(center_y, center_x - 1, ' ')
    stdscr.addstr(center_y, center_x, self.game_state.get_letter(y, x))
    stdscr.attroff(curses.color_pair(color_id))


  def move_cursor(self, stdscr, key):
    y = self.cursor_y
    x = self.cursor_x

    if key == ord('j'):
      y = y + 1
    elif key == ord('k'):
      y = y - 1
    elif key == ord('l'):
      x = x + 1
    elif key == ord('h'):
      x = x - 1

    x = max(0, x)
    x = min(4, x)

    y = max(0, y)
    y = min(4, y)

    stdscr.move(
      self.start_y + 3 + 2 * y,
      self.start_x + 2 + 4 * x
    )
    
    self.cursor_y = y
    self.cursor_x = x


  def draw_title(self, stdscr):
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(self.start_y, self.start_x + 1, "Letterpress Console")
    stdscr.attroff(curses.A_BOLD)


  def draw_input(self, stdscr):
    input_str = self.game_state.get_selected_letters()
    stdscr.addstr(self.start_y + 1, self.start_x, "play: ")
    stdscr.attron(curses.A_UNDERLINE)
    stdscr.addstr(self.start_y + 1, self.start_x + 6, input_str)
    stdscr.attroff(curses.A_UNDERLINE)
    
  def draw_wordlist(self, stdscr):
    words = self.game_state.get_played_words()
    current_line = 3 + self.start_y
    current_row = 23 + self.start_x
    i = 1
    for word in words:
      stdscr.addstr(current_line, current_row, "{}. {}".format(i, word))
      current_line += 1
      i += 1


  def save_game(self):
    filename = "Game_" + "_".join(datetime.datetime.now().strftime("%c").split(" "))
    self.game_state.save_game_to_file(filename=filename)


  def get_game_files(self):
    filenames = []
    for f in os.listdir("."):
      if fnmatch.fnmatch(f, "Game_"):
        filenames.append(f)

    return filenames[:9]


  def draw_dir(self, stdscr):
    current_line = self.start_y + 14
    i = 1
    for fn in self.get_game_files():
      stdscr.addstr(current_line, self.start_x + 1, "{}. {}".format(i, fn))
      current_line += 1
      i += 1


  def load_game(self, filename):
    result = self.game_state.load_game_from_file(filename=filename)


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
        
        load_game = False
      
        if k == ord('a'):
          self.game_state.select_tile(self.cursor_y, self.cursor_x)
        elif k == ord('u'):
          self.game_state.undo_selection()
        elif k == ord('x'):
          self.game_state.play_selected_word()
        elif k == ord('s'):
          self.save_game()
        elif k == ord('i'):
          load_game = True
        elif k >= ord('1') and k <= ord('9'):
          filenames = self.get_game_files()
          self.load_game(filenames[k - ord('1')])

        # Initialization
        stdscr.clear()

        # Rendering the board
        self.draw_title(stdscr)
        self.draw_frame(stdscr)
        self.draw_input(stdscr)
        self.draw_wordlist(stdscr)

        if load_game:
          self.draw_dir(stdscr)

        for i in range(5):
          for j in range(5):
            if not self.game_state.is_selected_tile(i, j):
              self.draw_tile(stdscr, i, j)

        self.move_cursor(stdscr, k)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    return draw_func

def ui():
  states = GameStates()
  ui = GameUI(state = states, start_y = 1, start_x = 2)
  draw_func = ui.generate_draw_func()
  curses.wrapper(draw_func)

if __name__ == "__main__":
  ui()
