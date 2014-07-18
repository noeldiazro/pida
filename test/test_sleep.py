from __future__ import division
import time

N_SAMPLES = 1000
t_l = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]

for t in t_l:
    expected_time = t * N_SAMPLES
    start_time = time.time()
    for i in range(N_SAMPLES):
        time.sleep(t)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        "{:.3f}".format(t*1000) + " & " + 
        "{:.3f}".format(1/t) + " & " +
        "{:.3f}".format(expected_time) + " & " +
        "{:.3f}".format(elapsed_time) + " & " +
        "{:.2f}".format((elapsed_time-expected_time)/expected_time*100) + " \\\\")

