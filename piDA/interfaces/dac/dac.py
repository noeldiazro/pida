from abc import ABCMeta, abstractmethod

class DAC:
    '''Abstract base class for classes that manage Digital/Analog converters operation'''
    __metaclass__ = ABCMeta

    def __init__(self, vref, bits):
        self._vref = vref * 1.0
        self._bits = bits
        self._levels = 2 ** bits
        self._factor = self._levels / self._vref

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write_code(self, value, channel):
        pass

    def write(self, value, channel):
        self.write_code(int(value * self._factor), channel)

    @property
    def vref(self):
        return self._vref

    @property
    def bits(self):
        return self._bits

    @property
    def levels(self):
        return self._levels
