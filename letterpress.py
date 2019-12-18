
import re
from genie import Genie

def letterpress():
  genie = Genie()
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
        game = filtered_cmd.string[1:]
        print("Setting up game...(%s)" % game)
        genie.awake(game)

      elif filtered_cmd.string.isalpha():
        print("Commencing search...")
        result = genie.ask(filtered_cmd.string)
        print(result[:40])

      else:
        print("Something is wrong...")

    cmd = str(input(standby_text))

if __name__ == "__main__":
    # execute only if run as a script
    letterpress()
