import curses
import datetime
from state import State
import utils


class Arena:

    def __init__(self, state: State, start_y=0, start_x=0, mode=None, player=None):
        self.cursor_y = 0
        self.cursor_x = 0
        self.state = state
        self.start_y = start_y
        self.start_x = start_x
        self.show_recommendation = False
        self.page_number = 0
        self.game_mode = mode
        self.player = player

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
        tile_state = self.state.get_tile_state(cursor_y, cursor_x)

        if tile_state == 1:
            color_id = 1
        elif tile_state == -1:
            color_id = 3

        if color_id != 0 and self.state.is_protected_tile(cursor_y, cursor_x):
            color_id += 1

        return color_id

    def draw_tile(self, screen, y, x):
        center_y = self.start_y + 4 + y * 2
        center_x = self.start_x + 2 + x * 4
        color_id = self.tile_color(y, x)

        screen.attron(curses.color_pair(color_id))
        screen.addstr(center_y, center_x + 1, ' ')
        screen.addstr(center_y, center_x - 1, ' ')
        screen.addstr(center_y, center_x, self.state.get_letter(y, x))
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
        score = self.state.get_score()
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
        input_str = self.state.get_selected_letters()
        screen.addstr(self.start_y + 2, self.start_x, "play: ")
        screen.attron(curses.A_UNDERLINE)
        screen.addstr(self.start_y + 2, self.start_x + 6, input_str)
        screen.attroff(curses.A_UNDERLINE)

    def draw_wordlist(self, screen):
        words = self.state.get_played_words()
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
        current_line = 6 + self.start_y
        x = self.start_x + 50

        screen.addstr(current_line, x, "┃ Saved Games: p.{}".format(self.page_number))
        current_line += 1

        filenames = utils.get_files("Game_*")

        for i, fn in enumerate(filenames[self.page_number*10:self.page_number*10+10]):
            screen.addstr(current_line, x, "┃ {}. {}".format(i, fn))
            current_line += 1

    def draw_recommendation(self, screen):
        if self.show_recommendation is False:
            return

        current_line = 4 + self.start_y
        x = self.start_x + 50

        screen.addstr(current_line, x, "┃ Best Move: {}".format(self.state.get_recommendation()))
        screen.addstr(current_line + 1, x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def save_game(self):
        filename = "Game_" + "_".join(datetime.datetime.now().strftime("%c").split(" "))
        utils.write_str_to_file(self.state.to_str(), filename=filename)

    def load_game(self, key):
        filenames = utils.get_files("Game_*")
        result = utils.read_str_from_file(filename=filenames[self.page_number * 10 + key - ord('0')])
        self.state.from_str(result)

    def generate_draw_func(self):
        def draw_func(screen):
            k = 0

            # Clear and refresh the screen for a blank canvas
            screen.clear()
            screen.refresh()

            # Start colors in curses
            curses.start_color()
            curses.init_pair(1, 12, curses.COLOR_BLACK)  # bright blue
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(3, 9, curses.COLOR_BLACK)  # bright red
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

            # Loop where k is the last character pressed
            while k != ord('q'):

                self.show_recommendation = False

                if k == ord('a'):
                    self.state.select_tile(self.cursor_y, self.cursor_x)
                elif k == ord('u'):
                    self.state.undo_selection()
                elif k == ord('x'):
                    self.state.play_selected_word()
                elif k == ord('s'):
                    self.save_game()
                elif k == ord('r'):
                    self.show_recommendation = True
                elif k == ord('t'):
                    self.state.rotate()
                elif k == ord('v'):
                    self.state.flip()
                elif k == ord('b'):
                    self.state.flip(vertical=False)
                elif k == ord('['):
                    if self.page_number > 0:
                        self.page_number -= 1
                elif k == ord(']'):
                    self.page_number += 1
                elif k == ord(';'):
                    self.state.replay()
                elif ord('0') <= k <= ord('9'):
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
                self.draw_recommendation(screen)

                for i in range(5):
                    for j in range(5):
                        if not self.state.is_selected_tile(i, j):
                            self.draw_tile(screen, i, j)

                self.move_cursor(screen, k)

                # refresh the screen
                screen.refresh()

                # players play the game
                if self.game_mode == "mvh":
                    self.player.play("blue")
                elif self.game_mode == "hvm":
                    self.player.play("red")
                elif self.game_mode == "mvm":
                    self.player.play("blue")
                    self.player.play("red")
                    if self.state.is_finished():
                        self.save_game()
                        break

                # wait for next input
                if self.game_mode != "mvm":
                    k = screen.getch()

        return draw_func


def start_game():
    state = State(genie=None)
    arena = Arena(state=state, start_y=1, start_x=2)
    draw_func = arena.generate_draw_func()
    curses.wrapper(draw_func)


if __name__ == "__main__":
    start_game()
