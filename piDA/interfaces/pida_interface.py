from .interface import Interface
from .input_channel import InputChannel
from ..converters.mcp3202 import MCP3202
from ..links.spi_data_link import SPIDataLink

class piDAInterface(Interface):
    def __init__(self):
        identifier = "piDA Interface 2.0"
        description = ""
        link0 = SPIDataLink(0, 0, 100000)
        adc0 = MCP3202(3.3, link0)
        link1 = SPIDataLink(0, 1, 100000)
        adc1 = MCP3202(3.3, link1)
        channel_list = [
            InputChannel(0, "", adc0, 1),
            InputChannel(1, "", adc0, 0),
            InputChannel(2, "", adc1, 1),
            InputChannel(3, "", adc1, 0)
            ]
        Interface.__init__(self, identifier, description, channel_list)
