import os
import fnmatch


def write_str_to_file(s, filename):
    with open(filename, 'w') as fn:
        fn.write("{}\n".format(s))


def read_str_from_file(filename):
    with open(filename, 'r') as fn:
        line = fn.readline()
        s = line.strip()
        return s


def get_local_files(match_str):
    filenames = []
    for f in os.listdir("."):
        if fnmatch.fnmatch(f, match_str):
            filenames.append(f)

    return filenames[:9]

