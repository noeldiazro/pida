from abc import ABCMeta
import unittest

class Benchmark(unittest.TestCase):
    __metaclass__ = ABCMeta
    
    def print_result(self, result):
        print("\n{0}".format(result))

    def get_diffs(self, times):
        return [j - i for i, j in zip(times[:-1], times[1:])]

