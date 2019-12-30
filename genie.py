DEFAULT_WORDLIST = "wordlist"
DEFAULT_DICTIONARY = "dictionary"


class Genie:

    def __init__(self):
        self.dictionary = {}

    def awake(self, game):
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

    # TODO: def recommend(self, letters, game_state):

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


