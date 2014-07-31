from .adc import ADC
import spidev

class MCP3002(ADC):
    def __init__(self):
        self._spi = spidev.SpiDev()

    def open(self):
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 1000000

    def read(self, channel):
        r = self._spi.xfer2([1,(2+channel) << 6,0])
        return ((r[1]&31) << 6) + (r[2]>>2)

    def close(self):
        self._spi.close()
