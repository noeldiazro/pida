#include <Python.h>
#include <sched.h>

static PyObject *posix_error(void)
{
  return PyErr_SetFromErrno(PyExc_OSError);
}

PyDoc_STRVAR(get_policy_doc,
	     "get_policy()\n\n"
	     "Devuelve la política de planificador del proceso.");

static PyObject *get_policy(PyObject *self, PyObject *args)
{
  int policy;

  if ((policy = sched_getscheduler(0)) < 0)
    return posix_error();

  return Py_BuildValue("i", policy);
}

PyDoc_STRVAR(set_policy_doc,
	     "set_policy(policy, priority)\n\n"
	     "Fija la política de planificador del proceso.\n"
	     "\n"
	     ":param policy: política de planificador.\n"
	     ":param priority: prioridad de planificador.\n"
	     "\n"
	     "Ejemplo de uso:\n"
	     "\n"
	     ">>> import pida.scheduling\n"
	     ">>> pida.scheduling.get_policy()\n"
	     "0\n"
	     ">>> pida.scheduling.set_policy(pida.scheduling.SCHED_RR, 1)\n"
	     ">>> pida.scheduling.get_policy()\n"
	     "2\n"
	     );

static PyObject *set_policy(PyObject *self, PyObject *args)
{
  int policy;
  int priority;

  if (!PyArg_ParseTuple(args, "ii", &policy, &priority)) {
    return NULL;
  }
  
  const struct sched_param scheduling_params = { .sched_priority = priority};
  if ((sched_setscheduler(0, policy, &scheduling_params)) < 0)
    return posix_error();

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(get_priority_range_doc,
	     "get_priority_range(policy)\n"
	     "\n"
	     "Devuelve una tupla con las prioridades mínima y máxima\n"
	     "de la política de planificación.\n"
	     "\n"
	     ":param policy: política de planificador.\n"
	     "\n"
	     "Ejemplo de uso:\n"
	     "\n"
	     ">>> import pida.scheduling\n"
	     ">>> min_priority, max_priority = pida.scheduling.get_priority_range(pida.scheduling.SCHED_RR)\n"
	     ">>> min_priority\n"
	     "1\n"
	     ">>> max_priority\n"
	     "99\n"
	     );

static PyObject *get_priority_range(PyObject *self, PyObject *args)
{
  int policy;
  int min_priority;
  int max_priority;
  
  if (!PyArg_ParseTuple(args, "i", &policy)) {
    return NULL;
  }

  if ((min_priority = sched_get_priority_min(policy)) < 0)
    return posix_error();

  if ((max_priority = sched_get_priority_max(policy)) < 0)
    return posix_error();

  return Py_BuildValue("ii", min_priority, max_priority);  
}

static PyMethodDef scheduling_methods[] = {
  {"get_policy", get_policy, METH_VARARGS, get_policy_doc},
  {"set_policy", set_policy, METH_VARARGS, set_policy_doc},
  {"get_priority_range", get_priority_range, METH_VARARGS, get_priority_range_doc},
  {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(py_scheduling_doc,
	     "Este módulo contiene funciones para gestionar las políticas de planificador.\n"
	     "Las políticas de planificador disponibles son:\n"
	     " - SCHED_OTHER\n"
	     " - SCHED_BATCH\n"
	     " - SCHED_IDLE\n"
	     " - SCHED_FIFO\n"
	     " - SCHED_RR\n"	     
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
