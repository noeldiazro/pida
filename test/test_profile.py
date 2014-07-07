import cProfile
import pstats
from Acquisition_nt import Acquisition

def test():
    a = Acquisition(0,0,10000)
    a.start()

cProfile.run('test()', 'profiler_stats')
stats = pstats.Stats('profiler_stats')
stats.sort_stats('cumulative')
stats.print_stats()
