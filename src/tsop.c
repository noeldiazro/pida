#include "tsop.h"
#include <math.h>

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

struct timespec double_to_ts(double t) {
  long sec;
  long nsec;

  sec = (long)floor(t);
  nsec = (long)((t-sec)*NS_PER_S);
  
  return ts_create(sec, nsec);
}
