import sys
import random
import curses
from state import State
from genie import Genie
from arena import Arena
from player import Player


class Game:

    def __init__(self):
        game_mode = Game.parse_args() or "hvh"
        game_str = [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(25)]
        game_str = "".join(game_str)

        self.game_str = game_str
        self.genie = Genie()
        self.genie.awake(game_str)
        self.state = State(genie=self.genie, game_str=game_str)
        self.player = Player(genie=self.genie, state=self.state)
        self.arena = Arena(state=self.state, start_y=1, start_x=2, mode=game_mode, player=self.player)

    def run(self):
        draw_arena = self.arena.generate_draw_func()
        curses.wrapper(draw_arena)

    @classmethod
    def parse_args(cls):
        if len(sys.argv) < 2:
            return None

        mode = sys.argv[1]  # determine game mode: --hvm (human v machine), mvh, mvm, hvh
        if len(mode) != 5 or mode[0:2] != "--":
            raise Exception("Invalid argument", mode)

        mode = mode[2:5]

        if not mode[0] in ["h", "m"] or not mode[2] in ["h", "m"] or mode[1] != "v":
            raise Exception("Invalid argument", mode)

        return mode


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
