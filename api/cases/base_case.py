import unittest
from lib.db import DB


class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DB()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
