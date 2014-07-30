from abc import ABCMeta, abstractmethod

class DAC:
    '''Abstract base class for classes that manage Digital/Analog converters operation'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, value, channel):
        pass
