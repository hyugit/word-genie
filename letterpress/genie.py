import copy
from state import State


DEFAULT_WORDLIST = "wordlist"
DEFAULT_DICTIONARY = "dictionary"


class Genie:

    def __init__(self):
        self.game_str = "a"*25
        self.dictionary = {}

    def awake(self, game):
        if game == self.game_str:
            # print("Already on the same game...")
            return False

        if not game.isalpha() or not game.islower() or len(game) != 25:
            # print("Invalid game string, going back to sleep...")
            return False

        self.reload()
        result = self.trim(game)

        print("Woke! {} words available!".format(result))
        return result

    def ask(self, letters):
        if not letters.isalpha() or not letters.islower():
            print("Invalid query...")
            return

        result = self.find(letters)
        return result

    def recommend(self, indices, state: State):
        working_states = copy.deepcopy(state)
        working_states.select_tiles(indices)
        letters = working_states.get_selected_letters()
        current_player = working_states.get_current_player()

        # setup decision making criteria
        working_scores = working_states.get_score()
        working_defences = working_states.get_protected_tiles()
        working_efficiency = working_states.get_efficiency()

        # calculate baselines
        best_score = working_scores[current_player]  # baseline
        best_defence = working_defences[current_player]  # baseline for protected tiles
        best_efficiency = 0  # baseline for efficiency
        best_opt = None

        # get full matches
        full_matches = set(self.ask(letters))

        # remove used words
        matches = full_matches.difference(set(working_states.get_played_words()))

        # get partial matches. When there is no match,
        # instead of enumerating all the possibilities,
        # we should drop one letter from the end of the line,
        # because this approach implies an order to the letters
        # that the neural networks can learn and rely on
        if len(matches) is 0:
            # get the partial letters, but only a few within reasonable range
            partial_letters = [letters[0:-i-1] for i in range(min(3, len(letters) - 3))]
            for partial in partial_letters:
                partial_matches = set(self.ask(partial))
                matches = matches.union(partial_matches)

        matches = sorted(list(matches), key=len, reverse=True)

        for m in matches:
            for opt in working_states.get_playable_options_from_letters(m, hint=indices):
                tmp_states = copy.deepcopy(working_states)
                tmp_states.select_tiles(opt)
                tmp_states.play_selected_word()

                # get statistics
                scores = tmp_states.get_score()
                score = scores[current_player]
                defences = tmp_states.get_protected_tiles()
                defence = defences[current_player]
                efficiencies = tmp_states.get_efficiency()
                efficiency = efficiencies[current_player]

                # decision making
                # Option 1:
                # if efficiency >= best_efficiency and score >= best_score and defence >= best_defence:
                #
                # Option 2:
                # if score >= best_score and defence > best_defence:
                #
                # Option 3:
                # if defence > best_defence or \
                #         (defence == best_defence and score > best_score):
                if score > best_score and defence >= best_defence:
                    best_opt = opt
                    best_score = score
                    best_defence = defence
                    best_efficiency = efficiency

        return best_opt

    def verify(self, word):
        if not word.isalpha() or not word.islower():
            print("Invalid query...")
            return False

        key = "".join(sorted(word))
        if not self.dictionary.get(key):
            return False

        if word in self.dictionary.get(key):
            return True

        return False

    def reload(self):
        print("Reading word list...")

        with open(DEFAULT_WORDLIST) as wl:
            lines = wl.readlines()
            words = [line.strip() for line in lines]
            indices = ["".join(sorted(word)) for word in words]
            self.dictionary = {i: w for i, w in zip(indices, words)}

    def trim(self, game):
        if self.game_str == game:
            return 0

        letters = "".join(sorted(game))
        available_words = 0

        for key in list(self.dictionary):
            tmp_letter = letters

            for k in key:
                if tmp_letter.find(k) < 0:
                    self.dictionary.pop(key, None)

                else:
                    tmp_letter = tmp_letter.replace(k, "", 1)

            if self.dictionary.get(key):
                available_words += len(self.dictionary.get(key))

        self.game_str = game

        return available_words

    def find(self, word):
        letters = sorted(word)
        result = []

        for key in sorted(list(self.dictionary), key=len, reverse=True):
            tmp_key = key
            found = True

            for letter in letters:
                if tmp_key.find(letter) < 0:
                    found = False
                    break

                tmp_key = tmp_key.replace(letter, "", 1)

            if found:
                result.extend(self.dictionary.get(key) or [])

        return result

    def petrify(self):
        with open(DEFAULT_DICTIONARY, 'w') as df:
            for k in sorted(list(self.dictionary), key=len, reverse=True):
                words = ",".join(self.dictionary.get(k) or [])
                df.write("%s:%s\n" % (k, words))


