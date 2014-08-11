from abc import ABCMeta

class Converter(object):
    '''Abstract base class for classes that manage data converters'''
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, vref, bits, channels, data_link):
        self._identifier = identifier
        self._description = description
        self._vref = vref * 1.0
        self._bits = bits
        self._levels = 2 ** self._bits
        self._channels = channels
        self._data_link = data_link
        
    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    def open(self):
        self._data_link.open()

    def close(self):
        self._data_link.close()

    @property
    def vref(self):
        return self._vref

    @property
    def bits(self):
        return self._bits

    @property
    def levels(self):
        return self._levels

    @property
    def channels(self):
        return self._channels

    @property
    def data_link(self):
        return self._data_link
