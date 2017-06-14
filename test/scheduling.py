import unittest
import pida.scheduling

class SchedulingTest(unittest.TestCase):

    def test_get_priority_range(self):
        min_priority, max_priority = pida.scheduling.get_priority_range(pida.scheduling.SCHED_OTHER)
