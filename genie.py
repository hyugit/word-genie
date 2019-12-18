class Genie:

  def __init__(self, wordlist = None):
    self._dictionary = {}
    self._wordlist = "wordlist"

    if wordlist != None:
      self._wordlist = str(wordlist)

  def awake(self, game):
    if not game.isalpha() or not game.islower() or len(game) != 25:
      print("Invalid game string, going back to sleep...")
      return

    self._reload()
    result = self._trim(game)

    print("Woke! {} words available!".format(result))
    return result

  def ask(self, letters):
    if not letters.isalpha() or not letters.islower():
      print("Invalid query...")
      return

    result = self._find(letters)

    return result

  def _reload(self):
    print("Reading word list...")

    with open(self._wordlist) as wl:
      line = wl.readline()

      while line:
        line = wl.readline()
        word = line.strip()
        index = "".join(sorted(word))

        if index in self._dictionary:
          self._dictionary[index].append(word)

        else:
          self._dictionary[index] = [word]

  def _trim(self, game):
    letters = "".join(sorted(game))
    available_words = 0

    for key in list(self._dictionary):
      tmp_letter = letters

      for k in key:
        if tmp_letter.find(k) < 0:
          self._dictionary.pop(key, None)

        else:
          tmp_letter = tmp_letter.replace(k, "", 1)

      if self._dictionary.get(key):
        available_words += len(self._dictionary.get(key))

    return available_words

  def _find(self, word):
    letters = sorted(word)
    result = []

    for key in sorted(list(self._dictionary), key = len, reverse = True):
      tmp_key = key
      found = True

      for letter in letters:
        if tmp_key.find(letter) < 0:
          found = False
          break

        tmp_key = tmp_key.replace(letter, "", 1)

      if found:
        result.extend(self._dictionary.get(key) or [])
        
    return result

  def petrify(self):
    dictfile = 'dictionary'
    print("Writing dictionary...")

    with open(dictfile, 'w') as df:
      for k in sorted(list(self._dictionary), key = len, reverse = True):
        words = ",".join(self._dictionary.get(k) or [])
        df.write("%s:%s\n" % (k, words))


