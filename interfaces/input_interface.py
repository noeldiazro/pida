from abc import ABCMeta, abstractmethod

class InputInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        print 1

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def read(self, channel):
        pass
