class GameStates:

  def __init__(self):
    self.game_str = "a"*25
    self.game_state = [0]*25
    self.history = []
    self.selected_tiles = []


  def save_game_to_file(self, filename):
    rec = self.game_state_to_str()
    with open(filename, 'w') as fn:
      fn.write("{}\n".format(rec))


  def load_game_from_file(self, filename):
    with open(filename, 'r') as fn:
      line = fn.readline()
      line = line.strip()
      result = self.load_game_state_from_str(line)

      if not result:
        print("Failed to load game from file")
        return False

    return True


  def game_state_to_str(self):
    entry = self.game_str
    entry += ";"
    entry += ",".join([str(s) for s in self.game_state])
    entry += ";"

    histitems = [",".join([str(it) for it in item]) for item in self.history]
    entry += "|".join(histitems)
    entry += "#"
    return entry


  def load_game_state_from_str(self, s):
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

    if entries[2][-1] != "#": # check sanity
      return False

    self.history = [[int(it) for it in row.split(",")] for row in entries[2][:-1].split("|")]

    for row in self.history:
      for it in row:
        if it < 0 or it > 24:
          return False

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


  def play_selected_word(self):
    word = self.get_selected_letters()

    for tiles in self.history:
      if word == self.get_word(tiles):
        return False

    self.history.append(self.selected_tiles)

    modified_tiles = []
    for s in self.selected_tiles:
      if not self.is_protected_tile(int(s/5), s%5):
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


  def is_protected_tile(self, y, x):
    tile_state = self.game_state[5*y+x]

    if tile_state == 0:
      return False
    
    if y - 1 >= 0 and self.game_state[5*y+x-5] != tile_state:
      return False
    
    if y + 1 <= 4 and self.game_state[5*y+x+5] != tile_state:
      return False
    
    if x - 1 >= 0 and self.game_state[5*y+x-1] != tile_state:
      return False
    
    if x + 1 <= 4 and self.game_state[5*y+x+1] != tile_state:
      return False

    return True
