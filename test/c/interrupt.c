#include <stdio.h>
#include <wiringPi.h>
#include <time.h>
#include "tsop.h"
#include <math.h>

#define INNER_LOOP 1000

static volatile int globalCounter = 0;
static struct timespec result[INNER_LOOP + 1];

void myInterrupt(void) {
  if (globalCounter <= INNER_LOOP)
    {
      clock_gettime(CLOCK_MONOTONIC, &result[globalCounter]);
      ++globalCounter;
    }
}

int main (void)
{
  int i;

  float min, max, diff, total, mean, variance;
  struct timespec sleep_time = {0, 0.2 * NS_PER_MS};
  struct timespec tested_iter_time, expected_iter_time;

  wiringPiSetup();

  wiringPiISR(0, INT_EDGE_FALLING, &myInterrupt);
  
  pinMode(7, GPIO_CLOCK);

  gpioClockSet(7, (int) 1/ts_to_s(sleep_time));

  pinMode(0, INPUT);
  //  pullUpDnControl(0, PUD_UP);

  while(globalCounter <= INNER_LOOP)
    {
    }

  for (i = 0; i <= INNER_LOOP; i++) {
    printf("s=%ld, ns=%ld\n", result[i].tv_sec, result[i].tv_nsec);
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
  
  expected_iter_time = ts_scalar_product(sleep_time, INNER_LOOP);
  tested_iter_time = ts_subtract(result[INNER_LOOP], result[0]);

  /* Calculate minimum and maximum oversleeping */
  min = (ts_to_ns(ts_subtract(result[1], result[0])) - ts_to_ns(sleep_time)) / NS_PER_US;
  max = min;

  for (i = 1; i < INNER_LOOP; i++)
    {
      diff = (ts_to_ns(ts_subtract(result[i + 1], result[i])) - ts_to_ns(sleep_time)) / NS_PER_US;

      min = min > diff ? diff : min;
      max = max < diff ? diff : max;
    }

      /* Mean and variance */
  total = 0;
  for (i = 0; i < INNER_LOOP; i++) {
    diff = (ts_to_ns(ts_subtract(result[i + 1], result[i])) - ts_to_ns(sleep_time)) / NS_PER_US;
    total += diff;
  }
  mean = total / INNER_LOOP;

  total = 0;
  for (i = 0; i < INNER_LOOP; i++) {
    diff = (ts_to_ns(ts_subtract(result[i + 1], result[i])) - ts_to_ns(sleep_time)) / NS_PER_US;
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

  return(0);
}
