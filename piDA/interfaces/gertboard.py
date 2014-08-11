from .interface import Interface
from .input_channel import InputChannel
from .output_channel import OutputChannel
from ..converters.mcp3002 import MCP3002
from ..converters.mcp4802 import MCP4802
from ..links.spi_data_link import SPIDataLink

class Gertboard(Interface):
    def __init__(self):
        identifier = "Gertboard"
        description = ""
        link0 = SPIDataLink(0, 0, 1000000)
        adc0 = MCP3002(3.3, link0)
        link1 = SPIDataLink(0, 1, 1000000)
        dac0 = MCP4802(2.048, link1)
        channel_list = [
            InputChannel(0, "", adc0, 0),
            InputChannel(1, "", adc0, 1),
            OutputChannel(2, "", dac0, 0),
            OutputChannel(3, "", dac0, 1)
            ]
        Interface.__init__(self, identifier, description, channel_list)
