from abc import ABCMeta, abstractmethod

class DataLink(object):
    '''Abstract base class for classes that manage data links'''
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, max_speed):
        self._identifier = identifier
        self._description = description
        self._max_speed = max_speed

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def max_speed(self):
        return self._max_speed

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def transfer(self, data):
        pass
