from abc import ABCMeta, abstractmethod

class ADC:
    '''Abstract base class for classes that manage Analog/Digital converters operation'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read(self, channel):
        pass
