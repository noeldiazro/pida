# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar las E/S de propósito general."""
from enum import Enum
from time import sleep

SYSFS_GPIO_DIR = "/sys/class/gpio/"

class Direction(Enum):
    INPUT = "in"
    OUTPUT = "out"

class Status(Enum):
    LOW = "0"
    HIGH = "1"

class GPIO(object):
    """Clase para gestionar una entrada/salida de propósito general
    (GPIO = General Purpose Input/Output).
    
    :param id: identificador de la entrada/salida de propósito general.
    """

    def __init__(self, number):
        self._number = number
        self._path = SYSFS_GPIO_DIR + "gpio" + str(number) + "/"

    def _write(self, filename, value):
        with open(filename, "w") as fd:
            fd.write(str(value))

    def _read(self, filename):
        with open(filename, "r") as fd:
            return fd.read().rstrip()
    
    def open(self):
        self._write(SYSFS_GPIO_DIR + "export", self._number)
        sleep(0.25)

    def close(self):
        self._write(SYSFS_GPIO_DIR + "unexport", self._number)

    @property
    def direction(self):
        return Direction(self._read(self._path + "direction"))

    @direction.setter
    def direction(self, direction):
        self._write(self._path + "direction", direction.value)

    @property
    def status(self):
        return Status(self._read(self._path + "value"))

    @status.setter
    def status(self, status):
        self._write(self._path + "value", status.value)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
