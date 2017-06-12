from benchmark import Benchmark
from pida.clock import time

class ClockTest(Benchmark):

    def test_estimate_clock_resolution(self):
        n_samples = 10000
        times = [time() for _ in range(n_samples)]
        diffs = self.get_diffs(times)
        estimated_resolution = min(diffs)
        self.print_result(estimated_resolution)
