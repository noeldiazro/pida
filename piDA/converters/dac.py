from abc import ABCMeta, abstractmethod
from .converter import Converter

class DAC(Converter):
    '''Abstract base class for classes that manage Digital/Analog converter operation'''
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, vref, bits, channels, data_link):
        Converter.__init__(self, identifier, description, vref, bits, channels, data_link)
        self._factor = self._levels / self._vref  

    @abstractmethod
    def write_code(self, value, channel):
        pass

    def write(self, value, channel):
        return self.write_code(int(value * self._factor), channel)
