from .channel import Channel

class InputChannel(Channel):
    '''Class that manages an input channel of an interface'''
    
    def __init__(self, identifier, description, converter, converter_channel):
        Channel.__init__(self, identifier, description, converter, converter_channel)

    def read(self):
        return self._converter.read(self._converter_channel)
