import copy


class GameStates:

    def __init__(self, genie, game_str="a"*25, game_state=None, history=None):
        self.game_str = game_str

        if game_state is None:
            game_state = [0] * 25
        self.game_state = game_state

        if history is None:
            history = []
        self.history = history

        self.selected_tiles = []
        self.genie = genie

    def __deepcopy__(self, memo=None):
        gs = GameStates(
            genie=self.genie,
            game_str=copy.deepcopy(self.game_str),
            game_state=copy.deepcopy(self.game_state),
            history=copy.deepcopy(self.history)
        )

        gs.selected_tiles = []

        return gs

    def to_str(self):
        entry = self.game_str
        entry += ";"

        entry += ",".join([str(s) for s in self.game_state])
        entry += ";"

        items = [",".join([str(it) for it in item]) for item in self.history]
        entry += "|".join(items)
        entry += "#"

        return entry

    def from_str(self, s):
        entries = s.split(";")

        if len(entries) != 3:
            return False

        if len(entries[0]) != 25 or not entries[0].isalpha() or not entries[0].islower():
            return False

        self.game_str = entries[0]
        self.game_state = [int(item) for item in entries[1].split(",")]

        if len(self.game_state) != 25:
            return False

        for s in self.game_state:
            if s > 1 or s < -1:
                return False

        if entries[2][-1] != "#":  # check sanity
            return False

        self.history = []

        if entries[2] != "#":
            self.history = [[int(it) for it in row.split(",")] for row in entries[2][:-1].split("|")]

            for row in self.history:
                for it in row:
                    if it < 0 or it > 24:
                        return False

        self.selected_tiles = []

        if not self.is_finished():
            self.genie.awake(self.game_str)

        return True

    def get_tile_state(self, y, x):
        return self.game_state[5*y+x]

    def get_letter(self, y, x):
        return self.game_str[5*y+x]

    def select_tile(self, y, x):
        for s in self.selected_tiles:
            if 5*y+x == s:
                return False

        self.selected_tiles.append(5*y+x)
        return True

    def select_tiles(self, indices: [int]):
        for i in indices:
            if 0 <= i <= 24:
                self.selected_tiles.append(i)
            else:
                return False

        return True

    def get_playable_options_from_letters(self, letters, hint=None):
        if len(letters) is 0:
            return []

        if hint is None:
            hint = []

        # TODO: import & use numpy and setup virtual env

        # initialize indices matrix
        idx_mat = [[i for i, x in enumerate(self.game_str) if x is l] for l in letters]

        # prune indices matrix using hint
        for h in hint:
            for i, idx_col in enumerate(idx_mat):
                if h in idx_col:
                    idx_mat[i] = [h]
                    for col in idx_mat[i+1:]:
                        if h in col:
                            col.remove(h)

        # calc dimensions and least common multiple
        dims = [len(idx) for idx in idx_mat]
        lcm = 1
        for d in dims:
            lcm *= d

        # initialize the options matrix
        opt_mat = [[]]*lcm
        for i in range(len(opt_mat)):
            opt_mat[i] = copy.copy([0]*len(letters))

        # populate the options matrix
        step = 1
        for i, d in enumerate(dims):
            for j in range(lcm):
                opt_mat[(j*step) % lcm + (j*step) // lcm][i] = idx_mat[i][j % d]
            step *= d

        # remove columns that contain duplicates
        opt_mat = [opt for opt in opt_mat if len(set(opt)) is len(letters)]

        return opt_mat

    def get_recommendation(self):
        if len(self.selected_tiles) > 0:
            return self.genie.recommend(self.selected_tiles, self)

        return []

    def undo_selection(self):
        if self.selected_tiles:
            self.selected_tiles.pop()
            return True

        return False

    def is_selected_tile(self, y, x):
        for s in self.selected_tiles:
            if 5*y+x == s:
                return True

        return False

    def get_selected_letters(self):
        return self.get_word(self.selected_tiles)

    def get_word(self, tiles):
        word = ""
        for t in tiles:
            word += self.game_str[t]

        return word

    def get_score(self):
        blue = self.game_state.count(1)
        red = self.game_state.count(-1)
        return {"blue": blue, "red": red}

    def get_protected_tiles(self):
        blue = 0
        red = 0
        for i, s in enumerate(self.game_state):
            if s == 1 and self.is_protected_tile(0, 0, idx=i):
                blue += 1
            if s == -1 and self.is_protected_tile(0, 0, idx=i):
                red += 1

        return {"blue": blue, "red": red}

    def get_efficiency(self):
        ptiles = self.get_protected_tiles()
        scores = self.get_score()

        efficiencies = {}
        for player in ["blue", "red"]:
            if scores[player] is 0:
                efficiencies[player] = 0
            else:
                efficiencies[player] = ptiles[player] / scores[player]

        return efficiencies

    def is_finished(self):
        if 0 in self.game_state:
            return False

        return True

    def play_selected_word(self):
        word = self.get_selected_letters()

        if self.is_finished():
            return False

        if not self.genie.verify(word):
            return False

        for tiles in self.history:
            if word == self.get_word(tiles):
                return False

        self.history.append(self.selected_tiles)

        modified_tiles = []
        for s in self.selected_tiles:
            if not self.is_protected_tile(s // 5, s % 5):
                modified_tiles.append(s)

        for s in modified_tiles:
            if len(self.history) % 2 == 1:
                self.game_state[s] = 1
            else:
                self.game_state[s] = -1

        self.selected_tiles = []

        return True

    def get_played_words(self):
        return [self.get_word(item) for item in self.history]

    def get_current_player(self):
        if len(self.history) % 2 == 1:
            return "red"

        return "blue"

    def is_protected_tile(self, y, x, idx=None):
        if idx is None:
            idx = 5 * y + x
        else:
            y = idx // 5
            x = idx % 5

        tile_state = self.game_state[idx]

        if tile_state == 0:
            return False

        if 0 <= y - 1 <= 4 and self.game_state[idx-5] != tile_state:
            return False

        if 0 <= y + 1 <= 4 and self.game_state[idx+5] != tile_state:
            return False

        if 0 <= x - 1 <= 4 and self.game_state[idx-1] != tile_state:
            return False

        if 0 <= x + 1 <= 4 and self.game_state[idx+1] != tile_state:
            return False

        return True
