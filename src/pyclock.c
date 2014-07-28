#include "Python.h"
#include "tsop.h"

/* Destructor function for timespecs */
static void del_timespec(PyObject *obj) {
  free(PyCapsule_GetPointer(obj, "timespec"));
}

/* Utility functions */
static PyObject *timespec_to_pyobject(struct timespec *ts, int must_free) {
  return PyCapsule_New(ts, "timespec", must_free ? del_timespec : NULL);
}

static struct timespec *pyobject_to_timespec(PyObject *obj) {
  return (struct timespec *) PyCapsule_GetPointer(obj, "timespec");
}

/* Create a new timespec python object */
static PyObject *py_timespec(PyObject *self, PyObject *args) {
  struct timespec *ts;
  long sec, nsec;
  if (!PyArg_ParseTuple(args, "ll", &sec, &nsec)) {
    return NULL;
  }
  ts = (struct timespec *) malloc(sizeof(struct timespec));
  ts->tv_sec = sec;
  ts->tv_nsec = nsec;
  return timespec_to_pyobject(ts, 1);
}  

/* Returns number of seconds in a timespec */
static PyObject *py_ts_to_s(PyObject *self, PyObject *args) {
  struct timespec *ts;
  PyObject *py_ts;
  double result;

  if (!PyArg_ParseTuple(args, "O", &py_ts)) {
    return NULL;
  }

  if (!(ts = pyobject_to_timespec(py_ts))) {
    return NULL;
  }

  result = ts_to_s(*ts);

  return Py_BuildValue("d", result);
}

/* Returns number of milliseconds in a timespec */
static PyObject *py_ts_to_ms(PyObject *self, PyObject *args) {
  struct timespec *ts;
  PyObject *py_ts;
  double result;

  if (!PyArg_ParseTuple(args, "O", &py_ts)) {
    return NULL;
  }

  if (!(ts = pyobject_to_timespec(py_ts))) {
    return NULL;
  }

  result = ts_to_ms(*ts);

  return Py_BuildValue("d", result);
}

/* Returns number of microseconds in a timespec */
static PyObject *py_ts_to_us(PyObject *self, PyObject *args) {
  struct timespec *ts;
  PyObject *py_ts;
  double result;

  if (!PyArg_ParseTuple(args, "O", &py_ts)) {
    return NULL;
  }

  if (!(ts = pyobject_to_timespec(py_ts))) {
    return NULL;
  }

  result = ts_to_us(*ts);

  return Py_BuildValue("d", result);
}

/* Returns number of nanoseconds in a timespec */
static PyObject *py_ts_to_ns(PyObject *self, PyObject *args) {
  struct timespec *ts;
  PyObject *py_ts;
  double result;

  if (!PyArg_ParseTuple(args, "O", &py_ts)) {
    return NULL;
  }

  if (!(ts = pyobject_to_timespec(py_ts))) {
    return NULL;
  }

  result = ts_to_ns(*ts);

  return Py_BuildValue("d", result);
}

/* Returns a timespec with the current value of CLOCK_MONOTONIC */
static PyObject *py_time(PyObject *self, PyObject *args) {
  struct timespec *result;

  result = (struct timespec *) malloc(sizeof(struct timespec));
  clock_gettime(CLOCK_MONOTONIC, result);

  return timespec_to_pyobject(result, 1);
} 

static PyObject *py_ts_add(PyObject *self, PyObject *args) {
  struct timespec *ts1, *ts2;
  PyObject *py_ts1, *py_ts2;
  struct timespec *result;

  if (!PyArg_ParseTuple(args, "OO", &py_ts1, &py_ts2)) {
    return NULL;
  }
  if (!(ts1 = pyobject_to_timespec(py_ts1))) {
    return NULL;
  }
  if (!(ts2 = pyobject_to_timespec(py_ts2))) {
    return NULL;
  }
  
  result = (struct timespec *) malloc(sizeof(struct timespec));
  *result = ts_add(*ts1, *ts2);
  /*  printf("ts1: s = %ld ns = %ld\n", ts1->tv_sec, ts1->tv_nsec);
  printf("ts2: s = %ld ns = %ld\n", ts2->tv_sec, ts2->tv_nsec);
  printf("result: s = %ld ns = %ld\n", result->tv_sec, result->tv_nsec); */
  return timespec_to_pyobject(result, 1);
}

static PyObject *py_clock_nanosleep(PyObject *self, PyObject *args) {
  struct timespec *request;
  PyObject *py_request;
  int result;

  if (!PyArg_ParseTuple(args, "O", &py_request)) {
    return NULL;
  }
  if (!(request = pyobject_to_timespec(py_request))) {
    return NULL;
  }

  result = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, request, NULL);
  return Py_BuildValue("i", result);
}

/* Module method table */
static PyMethodDef clock_methods[] = {
  /*  {"timespec", py_timespec, METH_VARARGS, "Creates a timespec."},
  {"ts_to_s", py_ts_to_s, METH_VARARGS, "Returns number of seconds."},
  {"ts_to_ms", py_ts_to_ms, METH_VARARGS, "Returns number of milliseconds."},
  {"ts_to_us", py_ts_to_us, METH_VARARGS, "Returns number of microseconds."},
  {"ts_to_ns", py_ts_to_ns, METH_VARARGS, "Returns number of nanoseconds."}, */
  {"time", py_time, METH_VARARGS, "Returns current instant."},
  /*  {"ts_add", py_ts_add, METH_VARARGS, "Adds two timespecs."},
      {"clock_nanosleep", py_clock_nanosleep, METH_VARARGS, "Sleeps specified duration"},*/
  {NULL, NULL, 0, NULL}
};

/* Module initialization function */
PyMODINIT_FUNC initclock(void)
{
  PyObject *m = Py_InitModule3("clock", clock_methods, "High-performance clocking.");
  if (m == NULL)
    return;
}
