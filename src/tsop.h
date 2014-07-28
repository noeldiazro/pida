#include <time.h>

#define NS_PER_S  1000000000L
#define NS_PER_MS 1000000L
#define NS_PER_US 1000L

struct timespec ts_create(long, long);

double ts_to_ns (struct timespec);

double ts_to_s (struct  timespec);

double ts_to_ms (struct timespec);

double ts_to_us (struct timespec);

struct  timespec  ts_add (struct  timespec, struct  timespec);

struct  timespec  ts_subtract (struct  timespec, struct  timespec);

struct timespec ts_scalar_product (struct timespec, int);

struct timespec double_to_ts(double);
