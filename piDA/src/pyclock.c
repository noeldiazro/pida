#include <Python.h>
#include "tsop.h"
#include <stdio.h>

PyDoc_STRVAR(py_time_doc,
	     "time() \n\n"
	     "Return current instant.\n");

/* Returns a timespec with the current value of CLOCK_MONOTONIC */
static PyObject *py_time(PyObject *self, PyObject *args) {
  struct timespec result;
  
  Py_BEGIN_ALLOW_THREADS
  clock_gettime(CLOCK_MONOTONIC, &result);
  Py_END_ALLOW_THREADS

  return Py_BuildValue("d", ts_to_s(result));
} 


PyDoc_STRVAR(py_sleep_doc,
	     "sleep(sleep_time)\n\n"
	     "Sleep specified interval\n");

static PyObject *py_sleep(PyObject *self, PyObject *args) {
  struct timespec request;
  double request_d;
  int result;

  if (!PyArg_ParseTuple(args, "d", &request_d)) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  request = double_to_ts(request_d);
  
  result = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &request, NULL);
  Py_END_ALLOW_THREADS

  return Py_BuildValue("i", result);
}

/* Module method table */
static PyMethodDef clock_methods[] = {
  {"time", py_time, METH_VARARGS, py_time_doc},
  {"sleep", py_sleep, METH_VARARGS, py_sleep_doc},
  {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(clock_module_doc,
	     ":mod:`clock`\n"
	     "~~~~~~~~~~~~\n"
	     "\n"
	     "High-performance clocking.\n");


/* Module initialization function */
PyMODINIT_FUNC initclock(void)
{
  PyObject *m = Py_InitModule3("clock", clock_methods, clock_module_doc);
  if (m == NULL)
    return;
}
