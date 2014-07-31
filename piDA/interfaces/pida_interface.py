from .interface import Interface
from .channel import Channel
from .mcp3202 import MCP3202

class piDAInterface(Interface):
    def __init__(self):
        adc0 = MCP3202()
        self._channel_list = [
            Channel(0, adc0, 0),
            Channel(1, adc0, 1)
            ]

    def get_channel_list(self):
        return self._channel_list

    def get_channel_by_id(self, identifier):
        return self._channel_list[identifier]
