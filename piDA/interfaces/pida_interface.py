from .interface import Interface
from .input_channel import InputChannel
from ..converters.mcp3202 import MCP3202
from ..links.spi_data_link import SPIDataLink

class piDAInterface(Interface):
    def __init__(self):
        identifier = "piDA Interface"
        description = ""
        link0 = SPIDataLink(0, 0, 1000000)
        adc0 = MCP3202(3.3, link0)
        channel_list = [
            InputChannel(0, "", adc0, 0),
            InputChannel(1, "", adc0, 1)
            ]
        Interface.__init__(self, identifier, description, channel_list)
