from .dac import DAC

class MCP4802(DAC):
    '''This class manages MCP4802 Digital-to-Analog converter'''
#    def __init__(self, vref=2.048, data_link):
    def __init__(self, vref, data_link):
        identifier = "MCP4802"
        description = ""
        bits = 8
        channels = 2
        DAC.__init__(self, identifier, description, vref, bits, channels, data_link)

    def write_code(self, value, channel):
        b1 = (channel << 7) + (0b011 << 4) + (value >> 4)
        b2 = (value << 4) & 0xFF
        r = self._data_link.transfer([b1, b2])
