#include <Python.h>
#include <sched.h>

PyDoc_STRVAR(get_policy_doc,
	     "Return the scheduling policy for the process with PID *pid*. A *pid* of 0 means the calling process. The result is one of the scheduling policy constants above."
	     );

static PyObject *get_policy(PyObject *self, PyObject *args)
{
  int policy;

  policy = sched_getscheduler(0);

  return Py_BuildValue("i", policy);
}

PyDoc_STRVAR(set_policy_doc,
	     "Set the scheduling policy for the process with PID *pid*. A *pid* of 0 means the calling process."
	     );

static PyObject *set_policy(PyObject *self, PyObject *args)
{
  int policy;
  int priority;

  if (!PyArg_ParseTuple(args, "ii", &policy, &priority)) {
    return NULL;
  }
  const struct sched_param scheduling_params = { .sched_priority = priority};
  sched_setscheduler(0, policy, &scheduling_params);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef scheduling_methods[] = {
  {"get_policy", get_policy, METH_VARARGS, get_policy_doc},
  {"set_policy", set_policy, METH_VARARGS, set_policy_doc}, 
  {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(py_scheduling_doc,
	     "This module provides functions to control how a process is allocated CPU time by the operating system."
	     );

PyMODINIT_FUNC initscheduling(void) {
  PyObject *module = Py_InitModule3("scheduling", scheduling_methods, py_scheduling_doc);
  if (module == NULL)
    return;

  PyModule_AddIntMacro(module, SCHED_OTHER);
  PyModule_AddIntMacro(module, SCHED_BATCH);
  PyModule_AddIntMacro(module, SCHED_IDLE);
  PyModule_AddIntMacro(module, SCHED_FIFO);
  PyModule_AddIntMacro(module, SCHED_RR);
}
