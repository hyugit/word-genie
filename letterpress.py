
import re

dict = {}

def load_wordlist():
  wordlist = 'wordlist'
  print("Reading word list...")

  with open(wordlist) as wl:
    line = wl.readline()

    while line:
      line = wl.readline()
      word = line.strip()
      index = "".join(sorted(word))

      if index in dict:
        dict[index].append(word)

      else:
        dict[index] = [word]

def write_dictionary():
  dictfile = 'dictionary'
  print("Writing dictionary...")

  with open(dictfile, 'w') as df:
    for k in sorted(list(dict), key = len, reverse = True):
      words = ",".join(dict[k])
      df.write("%s:%s\n" % (k, words))

def trim_dictionary(game):
  letters = "".join(sorted(game))

  for key in list(dict):
    tmp_letter = letters

    for k in key:
      if tmp_letter.find(k) < 0:
        dict.pop(key, None)

      else:
        tmp_letter = tmp_letter.replace(k, "", 1)

def find_words(word):
  letters = sorted(word)
  result = []

  for key in sorted(list(dict), key = len, reverse = True):
    tmp_key = key
    found = True

    for letter in letters:
      if tmp_key.find(letter) < 0:
        found = False
        break

      tmp_key = tmp_key.replace(letter, "", 1)

    if found:
      result.extend(dict[key])

    if len(result) > 20:
      break
      
  print(result)


standby_text = "Waiting for command: "
cmd = str(input(standby_text))

while cmd:
  filtered_cmd = re.search("^(:[a-z]{25}|[a-z]+)$", cmd)

  if cmd == "/":
    print("Exiting...")
    exit()

  else:
    if not filtered_cmd:
      print("Invalid command, please try again!")

    elif filtered_cmd.string[0] == ":":
      load_wordlist()
      write_dictionary()
      game = filtered_cmd.string[1:]
      print("Setting up game...(%s)" % game)
      trim_dictionary(game)

    elif filtered_cmd.string.isalpha():
      print("Commencing search...")
      find_words(filtered_cmd.string)

    else:
      print("Something is wrong...")

  cmd = str(input(standby_text))
