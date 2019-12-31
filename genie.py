import copy
from states import GameStates


DEFAULT_WORDLIST = "wordlist"
DEFAULT_DICTIONARY = "dictionary"


class Genie:

    def __init__(self):
        self.game_str = "a"*25
        self.dictionary = {}

    def awake(self, game):
        if game == self.game_str:
            print("Already on the same game...")
            return

        if not game.isalpha() or not game.islower() or len(game) != 25:
            print("Invalid game string, going back to sleep...")
            return

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

    def recommend(self, indices, game_state: GameStates):
        working_states = copy.deepcopy(game_state)
        working_states.select_tiles(indices)
        letters = working_states.get_selected_letters()
        played_words = set(working_states.get_played_words())
        working_scores = working_states.get_score()
        current_player = "blue"

        # if *blue* just played, then we are playing as *red*
        if len(played_words) % 2 == 1:
            current_player = "red"

        best_score = working_scores[current_player]  # baseline
        best_opt = None

        # get full matches
        full_matches = set(self.ask(letters))
        matches = full_matches.difference(played_words)

        # get partial matches
        if len(matches) is 0:
            partial_letters = ["".join([i for i in letters if i is not j]) for j in letters]
            for partial in partial_letters:
                partial_matches = set(self.ask(partial))
                matches.union(partial_matches)

        # get top 20 best play by score
        matches = sorted(list(matches), key=len, reverse=True)
        matches = matches[0:10]

        for m in matches:
            plays = working_states.get_playable_options_from_letters(m, hint=indices)
            for play in plays:
                tmp_states = copy.deepcopy(working_states)
                tmp_states.select_tiles(play)
                tmp_states.play_selected_word()
                scores = tmp_states.get_score()
                score = scores[current_player]

                if score > best_score:
                    best_opt = play
                    best_score = score

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
            line = wl.readline()

            while line:
                line = wl.readline()
                word = line.strip()
                index = "".join(sorted(word))

                if index in self.dictionary:
                    self.dictionary[index].append(word)

                else:
                    self.dictionary[index] = [word]

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
        print("Writing dictionary...")

        with open(DEFAULT_DICTIONARY, 'w') as df:
            for k in sorted(list(self.dictionary), key=len, reverse=True):
                words = ",".join(self.dictionary.get(k) or [])
                df.write("%s:%s\n" % (k, words))


