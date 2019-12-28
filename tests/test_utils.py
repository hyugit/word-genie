import unittest
import utils


class TestStringMethods(unittest.TestCase):

    def test_get_local_files(self):
        self.assertEqual(len(utils.get_local_files("*")), 1)  # we are in tests/ directory


if __name__ == '__main__':
    unittest.main()