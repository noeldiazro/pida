from abc import ABCMeta, abstractmethod, abstractproperty

class ADC:
    '''Abstract base class for classes that manage Analog/Digital converters operation'''
    __metaclass__ = ABCMeta

    def __init__(self, vref, bits):
        self._vref = vref * 1.0
        self._bits = bits
        self._levels = 2 ** bits
        self._factor = self._vref / self._levels

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read_code(self, channel):
        pass

    def read(self, channel):
        return self.read_code(channel) * self._factor
    
    @property
    def vref(self):
        return self._vref

    @property
    def bits(self):
        return self._bits

    @property
    def levels(self):
        return self._levels
