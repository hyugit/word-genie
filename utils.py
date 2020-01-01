import os
import fnmatch


def write_str_to_file(s, filename, directory="saved_games"):
    with open("./" + directory + "/" + filename, 'w') as fn:
        fn.write("{}\n".format(s))


def read_str_from_file(filename, directory="saved_games"):
    with open("./" + directory + "/" + filename, 'r') as fn:
        line = fn.readline()
        s = line.strip()
        return s


def get_files(match_str, directory="saved_games"):
    filenames = []
    for f in os.listdir("./" + directory):
        if fnmatch.fnmatch(f, match_str):
            filenames.append(f)

    return filenames

