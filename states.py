class GameStates:

  def __init__(self):
    self.game_str = "a"*25
    self.game_state = [0]*25
    self.history = []
    self.selected_tiles = []


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
    return map(self.get_word, self.history)


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
