import random
from genie import Genie
from state import State


class Player:

    def __init__(self, genie: Genie, state: State):
        self.genie = genie
        self.state = state

    def play(self, color):
        if not self.should_play(color):
            return False

        if self.state.is_finished():
            return False

        indices = []
        while not indices:
            targets = [random.choice(range(0, 24)) for _ in range(4)]
            self.genie.awake(self.state.game_str)
            indices = self.genie.recommend(targets, self.state)

        self.state.select_tiles(indices)
        self.state.play_selected_word()

        return True

    def should_play(self, color):
        if self.state.get_current_player() == color:
            return True

        return False
