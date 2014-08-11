from .adc import ADC

class MCP3202(ADC):
    '''Class that manages MCP3202 Analog-to-Digital converter'''
    def __init__(self, vref, data_link):
        identifier = "MCP3202"
        description = ""
        bits = 12
        channels = 2
        ADC.__init__(self, identifier, description, vref, bits, channels, data_link)

    def read_code(self, channel):
        r = self._data_link.transfer([1,(2+channel) << 6,0])
        return ((r[1] & 0b00001111) << 8) + r[2]
