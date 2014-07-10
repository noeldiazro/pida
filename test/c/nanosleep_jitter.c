#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> /* atoi */
#include <sched.h>
#include <string.h>
#include <sys/mman.h>

#define INNER_LOOP 1000
#define NS_PER_S  1000000000L
#define NS_PER_MS 1000000L
#define NS_PER_US 1000L

struct timespec ts_create(long s, long ns) {
  struct timespec result;

  result.tv_sec = s;
  result.tv_nsec = ns;

  return result;
}

double ts_to_ns (struct timespec ts)
{
  return ts.tv_sec * (double)NS_PER_S + ts.tv_nsec;
}

double ts_to_s (struct  timespec  ts)
{
  return ts_to_ns(ts) / NS_PER_S;
}

double ts_to_ms (struct timespec ts)
{
  return ts_to_ns(ts) / NS_PER_MS;
}

double ts_to_us (struct timespec ts)
{
  return ts_to_ns(ts) / NS_PER_US;
}

struct  timespec  ts_add (
			 struct  timespec  ts1,
			 struct  timespec  ts2)
{   
  struct  timespec  result ;
  
  /* Add the two times together. */
  result.tv_sec = ts1.tv_sec + ts2.tv_sec ;
  result.tv_nsec = ts1.tv_nsec + ts2.tv_nsec ;
  if (result.tv_nsec >= NS_PER_S) {		/* Carry? */
    result.tv_sec++ ;  result.tv_nsec = result.tv_nsec - NS_PER_S;
  }
  return (result) ;
}

struct  timespec  ts_subtract (
			      struct  timespec  ts1,
			      struct  timespec  ts2)
{    
  struct  timespec  result ;

  /* Subtract the second time from the first. */
  if ((ts1.tv_sec < ts2.tv_sec) ||
      ((ts1.tv_sec == ts2.tv_sec) &&
       (ts1.tv_nsec <= ts2.tv_nsec))) {		/* TS1 <= TS2? */
    result.tv_sec = result.tv_nsec = 0 ;
  } else {						/* TS1 > TS2 */
    result.tv_sec = ts1.tv_sec - ts2.tv_sec ;
    if (ts1.tv_nsec < ts2.tv_nsec) {
      result.tv_nsec = ts1.tv_nsec + NS_PER_S - ts2.tv_nsec ;
      result.tv_sec-- ;				/* Borrow a second. */
    } else {
      result.tv_nsec = ts1.tv_nsec - ts2.tv_nsec ;
    }
  }
  return (result) ;
}

struct timespec ts_scalar_product (struct timespec ts, int factor) {
  int i;

  struct timespec result;

  result = ts_create(0L, 0L);

  for (i = 0; i < factor; i++) {
    result = ts_add(result, ts);
  }

  return result;
}

/* Default arguments */
//struct timespec sleep_time = {50, 1000 * NS_PER_US}; /* 1000 usec */

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

  float min, max, diff;
  struct timespec expected_iter_time;
  struct timespec tested_iter_time;

  struct timespec res;

  struct timespec nano_time[INNER_LOOP + 1];
  struct timespec request;

  FILE *f = fopen("test.tex", "w");
  
  if (geteuid() != 0) {
    printf("You must run test as super user\n");
    return 0;
  }

  if (atoi(argv[1]) == 1) {
    struct sched_param sp;
    memset(&sp, 0, sizeof(sp));
    sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
    sched_setscheduler(0, SCHED_FIFO, &sp);
    mlockall(MCL_CURRENT | MCL_FUTURE);
  }
  
  printf("Sleep time (ms)\t"
	 "Sampling Rate (Hz)\t"
	 "Expected Time (s)\t"
	 "Elapsed Time (s)\t"
	 "Total Deviation (ms)\t"
	 "Total error (%%)\t"
	 "Min Deviation (us)\t"
	 "Min error (%%)\t"
	 "Max Deviation (us)\t"
	 "Max error (%%)\n");
  fprintf(f, "\\begin{table}\n");
  fprintf(f, "\\centering\n");
  fprintf(f, "\\begin{tabularx}{\\textwidth}{|X|X|X|X|X|X|X|X|X|X|}\n");
  fprintf(f, "\\hline\n");
  fprintf(f, "\\textbf{TS (ms)} & "
	  "\\textbf{FS (Hz)} & "
	  "\\textbf{TE (s)} & "
	  "\\textbf{TM (s)} & "
	  "\\textbf{DT (ms)} & "
	  "\\textbf{ET (\\%%)} & "
	  "\\textbf{DMin (us)} & "
	  "\\textbf{Emin (\\%%)} & "
	  "\\textbf{DMax (us)} & "
	  "\\textbf{EMax (\\%%)} \\\\ \n");
  fprintf(f, "\\hline\n");
  fprintf(f, "\\hline\n");

  for (i = 0; i < (sizeof(sleep_time_array) / sizeof(sleep_time_array[0])); i++)
    {
      sleep_time = sleep_time_array[i];
      expected_iter_time = ts_scalar_product(sleep_time, INNER_LOOP);
      for (j = 0; j < INNER_LOOP; j++)
	{
	  clock_gettime(CLOCK_MONOTONIC, &nano_time[j]);

	  request = ts_add(nano_time[j], sleep_time);
	  clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &request, NULL);
	}
      clock_gettime(CLOCK_MONOTONIC, &nano_time[INNER_LOOP]);
      
      /* Calculate minimum and maximum oversleeping */
      min = ts_to_us(ts_subtract(ts_subtract(nano_time[1], nano_time[0]), sleep_time));
      max = min;

      for (j = 1; j < INNER_LOOP; j++)
	{
	  diff = ts_to_us(ts_subtract(ts_subtract(nano_time[j+1], nano_time[j]), sleep_time));
	  min = min > diff ? diff : min;
	  max = max < diff ? diff : max;
	}
      
      /* Calculate iteration elapsed time */
      tested_iter_time = ts_subtract(nano_time[INNER_LOOP], nano_time[0]);

      printf("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.2f\t%.3f\t%.2f\t%.3f\t%.2f\n",
	     ts_to_ms(sleep_time),
	     1/ts_to_s(sleep_time),
	     ts_to_s(expected_iter_time), 
	     ts_to_s(tested_iter_time),
	     ts_to_ms(ts_subtract(tested_iter_time, expected_iter_time)),
	     ts_to_ns(ts_subtract(tested_iter_time, expected_iter_time))/ts_to_ns(expected_iter_time)*100,
	     min,
	     min/ts_to_us(sleep_time)*100,
	     max,
	     max/ts_to_us(sleep_time)*100);

      fprintf(f, "%.3f & %.3f & %.3f & %.3f & %.3f & %.2f & %.3f & %.2f & %.3f & %.2f \\\\ \n",
	     ts_to_ms(sleep_time),
	     1/ts_to_s(sleep_time),
	     ts_to_s(expected_iter_time), 
	     ts_to_s(tested_iter_time),
	     ts_to_ms(ts_subtract(tested_iter_time, expected_iter_time)),
	     ts_to_ns(ts_subtract(tested_iter_time, expected_iter_time))/ts_to_ns(expected_iter_time)*100,
	     min,
	     min/ts_to_us(sleep_time)*100,
	     max,
	     max/ts_to_us(sleep_time)*100);
    }
  
  fprintf(f, "\\hline\n");
  fprintf(f, "\\end{tabularx}\n");
  fprintf(f, "\\caption{test}");
  fprintf(f, "\\label{tab:slee_test}\n");
  fprintf(f, "\\end{table}\n");
  fclose(f);

  return 0;
}
