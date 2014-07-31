#include <Python.h>
#include "tsop.h"
#include <stdio.h>

/* Returns a timespec with the current value of CLOCK_MONOTONIC */
static PyObject *py_time(PyObject *self, PyObject *args) {
  struct timespec result;

  clock_gettime(CLOCK_MONOTONIC, &result);

  return Py_BuildValue("d", ts_to_s(result));
} 

static PyObject *py_sleep(PyObject *self, PyObject *args) {
  struct timespec request;
  double request_d;
  int result;

  if (!PyArg_ParseTuple(args, "d", &request_d)) {
    return NULL;
  }
  request = double_to_ts(request_d);
  
  result = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &request, NULL);
  return Py_BuildValue("i", result);
}

/* Module method table */
static PyMethodDef clock_methods[] = {
  {"time", py_time, METH_VARARGS, "Returns current instant."},
  {"sleep", py_sleep, METH_VARARGS, "Sleeps specified duration"},
  {NULL, NULL, 0, NULL}
};

/* Module initialization function */
PyMODINIT_FUNC initclock(void)
{
  PyObject *m = Py_InitModule3("clock", clock_methods, "High-performance clocking.");
  if (m == NULL)
    return;
}
