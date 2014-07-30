from abc import ABCMeta, abstractmethod

class Interface:
    '''Abstract base class for classes that manage data acquisition interfaces operation'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_channel_list(self):
        pass

    @abstractmethod
    def get_channel_by_id(self, identifier):
        pass
