import unittest
import sys

sys.path.append("../..")
from test_case.single_case.test_getranklist import GetRankList

smoke_suite = unittest.TestSuite()
smoke_suite.addTests([GetRankList('test_hot_list')])


def get_suite(suite_name):
    return globals().get(suite_name)


if __name__ == "__main__":
    print(get_suite("smoke_suite"))
