import sys
sys.path.append('..')

from Acquisition import Acquisition
import threading

# Sample Frequency list
l_fs = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000] 
running_time_per_test = 10

print('Target Sampling Rate & Number of samples & Elapsed Time & Avg Sampling Period & Avg Sampling Rate & Error')
for fs in l_fs:
    # Creates an Acquisition for each sampling rate
    n_count = fs * running_time_per_test
    a = Acquisition(fs, 0, n_count)

    a.start()
    a.join()

    elapsed_time = a.get_elapsed_time()
    avg_sampling_period = elapsed_time / n_count
    avg_sampling_rate = 1 / avg_sampling_period
    error = ( avg_sampling_rate - fs) / fs * 100
    print(str(fs) + ' & ' +
          str(n_count) + ' & ' +
          '{:.6f}'.format(elapsed_time) + ' & ' +
          '{:.6f}'.format(avg_sampling_period) + ' & ' +
          '{:.6f}'.format(avg_sampling_rate) + ' & ' +
          '{:.2f}'.format(error) + ' \\\\')
