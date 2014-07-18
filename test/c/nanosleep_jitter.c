#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> /* atoi */
#include <sched.h>
#include <string.h>
#include <sys/mman.h>
#include "tsop.h"
#include <math.h>

#define INNER_LOOP 1000

void test1(struct timespec sleep_time, int n_iter, struct timespec result[][2])
{
  int i = 0;
  struct timespec request;
  struct sched_param sp;

  memset(&sp, 0, sizeof(sp));
  sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
  sched_setscheduler(0, SCHED_FIFO, &sp);
  mlockall(MCL_CURRENT | MCL_FUTURE);

  for (i = 0; i < n_iter; i++)
    {
      clock_gettime(CLOCK_MONOTONIC, &result[i][0]);
      if (i == 0) {
	request = ts_add(result[i][0], sleep_time);
      } else {
	request = ts_add(request, sleep_time);
      }
      result[i][1] = request;

      clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &request, NULL);
    }
  
  clock_gettime(CLOCK_MONOTONIC, &result[n_iter][0]);
}

void test2(struct timespec sleep_time, int n_iter, struct timespec result[][2])
{
  int i = 0;
  struct timespec request;
  struct sched_param sp;

  memset(&sp, 0, sizeof(sp));
  sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
  sched_setscheduler(0, SCHED_FIFO, &sp);
  mlockall(MCL_CURRENT | MCL_FUTURE);

  for (i = 0; i < n_iter; i++)
    {
      clock_gettime(CLOCK_MONOTONIC, &result[i][0]);
      request = ts_add(result[i][0], sleep_time);
      result[i][1] = request;

      clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &request, NULL);
    }
  
  clock_gettime(CLOCK_MONOTONIC, &result[n_iter][0]);
}

int main(int argc, char* argv[])
{
  int i = 0;
  int j;
  
  struct timespec sleep_time_array[] = {
    ts_create(0, 100 * NS_PER_MS), // 100 msec -    10 Hz
    ts_create(0,  50 * NS_PER_MS), //  50 msec -    20 Hz
    ts_create(0,  20 * NS_PER_MS), //  20 msec -    50 Hz
    ts_create(0,  10 * NS_PER_MS), //  10 msec -   100 Hz
    ts_create(0,   5 * NS_PER_MS), //   5 msec -   200 Hz
    ts_create(0,   2 * NS_PER_MS), //   2 msec -   500 Hz
    ts_create(0,   1 * NS_PER_MS), //   1 msec -  1000 Hz
    ts_create(0, 0.5 * NS_PER_MS), // 0.5 msec -  2000 Hz
    ts_create(0, 0.2 * NS_PER_MS), // 0.2 msec -  5000 Hz
    ts_create(0, 0.1 * NS_PER_MS)  // 0.1 msec - 10000 Hz
  };

  struct timespec sleep_time;

  float min, max, diff, mean, variance, total;
  struct timespec expected_iter_time;
  struct timespec tested_iter_time;

  struct timespec result[INNER_LOOP + 1][2];


  if (geteuid() != 0) {
    printf("You must run test as super user\n");
    return 0;
  }
  
  printf("     Sleep time (ms)"
	 "  Sampling Rate (Hz)"
	 "   Expected Time (s)"
	 "    Elapsed Time (s)"
	 "Total Deviation (ms)"
	 "     Total error (%%)"
	 "  Min Deviation (us)"
	 "       Min error (%%)"
	 "  Max Deviation (us)"
	 "       Max error (%%)"
	 "           Mean (us)"
	 "            Variance\n");

  for (i = 0; i < (sizeof(sleep_time_array) / sizeof(sleep_time_array[0])); i++)
    {
      sleep_time = sleep_time_array[i];

      test2(sleep_time, INNER_LOOP, result);
      
      /* Process test  results */
      expected_iter_time = ts_scalar_product(sleep_time, INNER_LOOP);

      /* Calculate minimum and maximum oversleeping */
      min = (ts_to_ns(ts_subtract(result[1][0], result[0][0])) - ts_to_ns(sleep_time)) / NS_PER_US;
      max = min;

      for (j = 1; j < INNER_LOOP; j++)
	{
	  diff = (ts_to_ns(ts_subtract(result[j + 1][0], result[j][0])) - ts_to_ns(sleep_time)) / NS_PER_US;

	  min = min > diff ? diff : min;
	  max = max < diff ? diff : max;
	}
      
      /* Calculate iteration elapsed time */
      tested_iter_time = ts_subtract(result[INNER_LOOP][0], result[0][0]);

      /* Mean and variance */
      total = 0;
      for (j = 0; j < INNER_LOOP; j++) {
	diff = (ts_to_ns(ts_subtract(result[j + 1][0], result[j][0])) - ts_to_ns(sleep_time)) / NS_PER_US;
	total += diff;
      }
      mean = total / INNER_LOOP;

      total = 0;
      for (j = 0; j < INNER_LOOP; j++) {
	diff = (ts_to_ns(ts_subtract(result[j + 1][0], result[j][0])) - ts_to_ns(sleep_time)) / NS_PER_US;
	total += pow(diff-mean, 2);
      }
      variance = total / INNER_LOOP;

      printf("%20.3f%20.3f%20.3f%20.3f%20.3f%20.2f%20.3f%20.2f%20.3f%20.2f%20.3f%20.3f\n",
	     ts_to_ms(sleep_time),
	     1/ts_to_s(sleep_time),
	     ts_to_s(expected_iter_time), 
	     ts_to_s(tested_iter_time),
	     ts_to_ms(ts_subtract(tested_iter_time, expected_iter_time)),
	     ts_to_ns(ts_subtract(tested_iter_time, expected_iter_time))/ts_to_ns(expected_iter_time)*100,
	     min,
	     min/ts_to_us(sleep_time)*100,
	     max,
	     max/ts_to_us(sleep_time)*100,
	     mean,
	     variance);
    }

  return 0;
}
