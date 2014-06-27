import time
import spidev

class Acquisition:
    '''This class represents an acquisition object'''

    def __init__(self, sampling_rate=1, channel=0):
        self.__sampling_rate = sampling_rate
        self.__sampling_period = 1.0/sampling_rate
        self.__channel = channel
        self.__data = []
        self.__status = 'waiting'
        self.__spi = spidev.SpiDev()

    def set_sampling_rate(self, sampling_rate):
        self.__sampling_rate = sampling_rate
        self.__sampling_period = 1.0/sampling_rate

    def get_sampling_rate(self):
        return self.__sampling_rate

    def set_channel(self, channel):
        self.__channel = channel

    def get_channel(self):
        return self.__channel

    def start(self):
        try:
            self.__spi.open(0, 0)
            self.__status = 'running'
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                adc_value = self.__get_adc_value()
                self.__data.append([elapsed_time, adc_value])
                print(elapsed_time, adc_value)
                time.sleep(self.__sampling_period)
        except KeyboardInterrupt:
            self.__spi.close()

    def stop(self):
        self.__status = 'stopped'
        self.__spi.close()

    def get_data(self):
        return self.__data

    def get_status(self):
        return self.__status

    def __get_adc_value(self):
        # MCP3008
        #ret = self.__spi.xfer2([1, (8 + self.get_channel()) << 4, 0])
        #return ((ret[1]&3) << 8) + ret[2]
        # MCP3002
        #r = self.__spi.xfer2([1,(2+self.get_channel()) << 6,0])
        #return ((r[1]&31) << 6) + (r[2]>>2)
        # MCP3202
        r = self.__spi.xfer2([1,(2+self.get_channel()) << 6,0])
        return ((r[1] & 0b00001111) << 8) + r[2]
