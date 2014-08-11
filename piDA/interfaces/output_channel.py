from .channel import Channel

class OutputChannel(Channel):
    '''Class that manages an output channel of an interface'''

    def __init__(self, identifier, description, converter, converter_channel):
        Channel.__init__(self, identifier, description, converter, converter_channel)

    def write(self, value):
        return self._converter.write(value, self._converter_channel)
