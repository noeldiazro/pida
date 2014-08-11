from abc import ABCMeta

class Channel():
    '''This class representes a channel of an interface'''
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, converter, converter_channel):
        self._identifier = identifier
        self._description = description
        self._converter = converter
        self._converter_channel = converter_channel

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def converter(self):
        return self._converter
    
    @property
    def converter_channel(self):
        return self._converter_channel

    def open(self):
        self._converter.open()

    def close(self):
        self._converter.close()
