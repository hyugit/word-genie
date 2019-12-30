from states import GameStates
from genie import Genie
from ui import GameUI
import random
import curses


class Game:

    def __init__(self):
        game_str = [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(25)]
        game_str = "".join(game_str)
        self.genie = Genie()
        self.state = GameStates(genie=self.genie, game_str=game_str)
        self.game_str = game_str
        self.ui = GameUI(state=self.state, start_y=1, start_x=2)

    def run(self):
        draw_ui = self.ui.generate_draw_func()
        curses.wrapper(draw_ui)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
