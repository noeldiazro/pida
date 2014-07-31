from .dac import DAC
import spidev

class MCP4802(DAC):
    '''This class manages MCP4802 Digital/Analog Converter operation'''
    def __init__(self):
        self._spi = spidev.SpiDev()

    def open(self):
        self._spi.open(0, 1)

    def write(self, value, channel):
        b1 = (channel << 7) + (0b011 << 4) + (value >> 4)
        b2 = (value << 4) & 0xFF
        r = self._spi.xfer2([b1, b2])

    def close(self):
        self._spi.close()
