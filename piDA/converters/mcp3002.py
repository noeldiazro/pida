from .adc import ADC

class MCP3002(ADC):
    '''Class that manages MCP3002 Analog-to-Digital converter'''
    def __init__(self, vref, data_link):
        identifier = "MCP3002"
        description = ""
        bits = 10
        channels = 2
        ADC.__init__(self, identifier, description, vref, bits, channels, data_link)

    def read_code(self, channel):
        r = self._data_link.transfer([1,(2+channel) << 6,0])
        return ((r[1] & 0b00011111) << 6) + (r[2]>>2)
