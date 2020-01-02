import random
import curses
from state import State
from genie import Genie
from arena import Arena
from player import Player


class Game:

    def __init__(self):
        game_str = [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(25)]
        game_str = "".join(game_str)
        self.genie = Genie()
        self.state = State(genie=self.genie, game_str=game_str)
        self.game_str = game_str
        self.genie.awake(game_str)
        self.player = Player(genie=self.genie, state=self.state)
        self.arena = Arena(state=self.state, start_y=1, start_x=2, mode="hvm", player=self.player)

    def run(self):
        draw_arena = self.arena.generate_draw_func()
        curses.wrapper(draw_arena)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
