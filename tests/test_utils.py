import unittest
import utils


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        with open("text.txt", "w") as fn:  # clear content of test text file
            fn.write("")

    def tearDown(self) -> None:
        with open("text.txt", "w") as fn:
            fn.write("")

    def test_get_local_files(self):
        self.assertEqual(len(utils.get_local_files("*.py")), 1)  # we are in tests/ directory
        self.assertEqual(len(utils.get_local_files("text.txt")), 1)

    def test_write_str(self):
        utils.write_str_to_file("test", "text.txt")
        with open("text.txt", "r") as fn:
            line = fn.readline()
            s = line.strip()
            self.assertEqual(s, "test")

    def test_read_str(self):
        with open("text.txt", "w") as fn:
            fn.write("test")
        s = utils.read_str_from_file("text.txt")
        self.assertEqual(s, "test")


if __name__ == '__main__':
    unittest.main()
