import os
import curses
import datetime
import fnmatch
from genie import Genie
from states import GameStates


def save_game_to_file(s, filename):
    with open(filename, 'w') as fn:
        fn.write("{}\n".format(s))


def load_game_from_file(filename):
    with open(filename, 'r') as fn:
        line = fn.readline()
        line = line.strip()
        return line


def get_game_files():
    filenames = []
    for f in os.listdir("."):
        if fnmatch.fnmatch(f, "Game_*"):
            filenames.append(f)

    return filenames[:9]


class GameUI:

    def __init__(self, state, start_y=0, start_x=0):
        self.cursor_y = 0
        self.cursor_x = 0
        self.game_state = state
        self.start_y = start_y
        self.start_x = start_x

    def draw_frame(self, screen):
        current_line = self.start_y + 3

        screen.addstr(current_line, self.start_x, "┏━━━┳━━━┳━━━┳━━━┳━━━┓")
        current_line += 1

        for y in range(4):
            for x in range(6):
                screen.addstr(current_line, self.start_x + 4*x, "┃")
            current_line += 1
            screen.addstr(current_line, self.start_x, "┣━━━╋━━━╋━━━╋━━━╋━━━┫")
            current_line += 1

        for x in range(6):
            screen.addstr(current_line, self.start_x + 4*x, "┃")
        current_line += 1
        screen.addstr(current_line, self.start_x, "┗━━━┻━━━┻━━━┻━━━┻━━━┛")

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

    def draw_tile(self, screen, y, x):
        center_y = self.start_y + 4 + y * 2
        center_x = self.start_x + 2 + x * 4
        color_id = self.tile_color(y, x)

        screen.attron(curses.color_pair(color_id))
        screen.addstr(center_y, center_x + 1, ' ')
        screen.addstr(center_y, center_x - 1, ' ')
        screen.addstr(center_y, center_x, self.game_state.get_letter(y, x))
        screen.attroff(curses.color_pair(color_id))

    def move_cursor(self, screen, key):
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

        screen.move(
            self.start_y + 4 + 2 * y,
            self.start_x + 2 + 4 * x
        )

        self.cursor_y = y
        self.cursor_x = x

    def draw_title(self, screen):
        screen.attron(curses.A_BOLD)
        screen.addstr(self.start_y, self.start_x + 1, "Letterpress Console")
        screen.attroff(curses.A_BOLD)

    def draw_score(self, screen):
        score = self.game_state.get_score()
        screen.addstr(
            self.start_y + 1,
            self.start_x,
            "score: ")
        screen.addstr(
            self.start_y + 1,
            self.start_x + 7,
            str(score.get("blue")),
            curses.color_pair(2))
        screen.addstr(
            self.start_y + 1,
            self.start_x + 7 + len(str(score.get("blue"))),
            " - ")
        screen.addstr(
            self.start_y + 1,
            self.start_x + 10 + len(str(score.get("blue"))),
            str(score.get("red")),
            curses.color_pair(4))

    def draw_input(self, screen):
        input_str = self.game_state.get_selected_letters()
        screen.addstr(self.start_y + 2, self.start_x, "play: ")
        screen.attron(curses.A_UNDERLINE)
        screen.addstr(self.start_y + 2, self.start_x + 6, input_str)
        screen.attroff(curses.A_UNDERLINE)

    def draw_wordlist(self, screen):
        words = self.game_state.get_played_words()
        current_line = 4 + self.start_y
        current_row = 23 + self.start_x

        screen.addstr(current_line, current_row, "Words Played:")
        current_line += 1

        i = 1
        for word in words:
            screen.addstr(current_line, current_row, "{}. {}".format(i, word))
            current_line += 1
            i += 1

    def draw_dir(self, screen):
        current_line = 4 + self.start_y
        x = self.start_x + 50

        screen.addstr(current_line, x, "┃ Saved Games:")
        current_line += 1

        i = 1
        for fn in get_game_files():
            screen.addstr(current_line, x, "┃ {}. {}".format(i, fn))
            current_line += 1
            i += 1

    def save_game(self):
        filename = "Game_" + "_".join(datetime.datetime.now().strftime("%c").split(" "))
        save_game_to_file(self.game_state.to_str(), filename=filename)

    def load_game(self, key):
        filenames = get_game_files()
        result = load_game_from_file(filename=filenames[key - ord('1')])
        self.game_state.from_str(result)

    def generate_draw_func(self):
        def draw_func(screen):
            k = 0

            # Clear and refresh the screen for a blank canvas
            screen.clear()
            screen.refresh()

            # Start colors in curses
            curses.start_color()
            curses.init_pair(1, 12, curses.COLOR_BLACK) # bright blue
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(3, 9, curses.COLOR_BLACK) # bright red
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

            # Loop where k is the last character pressed
            while k != ord('q'):

                if k == ord('a'):
                    self.game_state.select_tile(self.cursor_y, self.cursor_x)
                elif k == ord('u'):
                    self.game_state.undo_selection()
                elif k == ord('x'):
                    self.game_state.play_selected_word()
                elif k == ord('s'):
                    self.save_game()
                elif ord('1') <= k <= ord('9'):
                    self.load_game(k)

                # Initialization
                screen.clear()

                # Rendering the board
                self.draw_title(screen)
                self.draw_frame(screen)
                self.draw_score(screen)
                self.draw_input(screen)
                self.draw_wordlist(screen)
                self.draw_dir(screen)

                for i in range(5):
                    for j in range(5):
                        if not self.game_state.is_selected_tile(i, j):
                            self.draw_tile(screen, i, j)

                self.move_cursor(screen, k)

                # Refresh the screen
                screen.refresh()

                # Wait for next input
                k = screen.getch()

        return draw_func


def ui():
    genie = Genie()
    states = GameStates(genie=genie)
    ui = GameUI(state=states, start_y=1, start_x=2)
    draw_func = ui.generate_draw_func()
    curses.wrapper(draw_func)


if __name__ == "__main__":
    ui()
