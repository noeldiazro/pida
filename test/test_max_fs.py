import sys
sys.path.append('..')

from Acquisition import Acquisition
import threading

# Sample count list
l_n_count = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
print('Sample count & Elapsed Time & Max Sampling Period & Max Sampling Rate')
for n_count in l_n_count:
    # Creates an Acquisition that tries to sampling at maximum speed
    a = Acquisition(0, 0, n_count)

    a.start()
    a.join()

    elapsed_time = a.get_elapsed_time()
    max_sampling_period = elapsed_time / n_count
    max_sampling_rate = 1 / max_sampling_period
    print(str(n_count) + ' & ' +
          '{:.6f}'.format(elapsed_time) + ' & ' +
          '{:.6f}'.format(max_sampling_period) + ' & ' +
          '{:.6f}'.format(max_sampling_rate) + ' \\\\')
