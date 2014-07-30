from abc import ABCMeta, abstractmethod

class OutputInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def open(self):
        print 1

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, value, channel):
        pass
