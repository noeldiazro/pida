from .interface import Interface

class FirstInterface(Interface):
    def open(self):
        return 1

    def close(self):
        return 0

    def read(self, channel):
        return channel
