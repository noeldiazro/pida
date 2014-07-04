import time
import spidev
import threading

class Acquisition(threading.Thread):
    '''This class represents an acquisition object'''

    def __init__(self, sampling_rate=0, channel=0, max_count=0):
        threading.Thread.__init__(self)
        self.__sampling_rate = sampling_rate
        if sampling_rate != 0:
            self.__sampling_period = 1.0/sampling_rate
        else:
            self.__sampling_period = 0
        self.__channel = channel
        self.__max_count = max_count
        self.__data = []
        self.__status = 'waiting'
        self.__spi = spidev.SpiDev()
        self.__running = True
        self.__elapsed_time = 0

    def set_sampling_rate(self, sampling_rate):
        self.__sampling_rate = sampling_rate
        self.__sampling_period = 1.0/sampling_rate

    def get_sampling_rate(self):
        return self.__sampling_rate

    def set_channel(self, channel):
        self.__channel = channel

    def get_channel(self):
        return self.__channel

    def set_max_count(self, max_count):
        self.__max_count = max_count
    
    def get_max_count(self):
        return self.__max_count

#    def start(self):
    def run(self):
            self.__spi.open(0, 0)
            self.__spi.max_speed_hz = 1000000
            self.__status = 'running'
            start_time = time.time()
            i = 0
            while self.__running and (self.__max_count == 0 or i < self.__max_count):
                self.__elapsed_time = time.time() - start_time
                adc_value = self.__get_adc_value()
                self.__data.append([self.__elapsed_time, adc_value])
                time.sleep(self.__sampling_period)
                i = i + 1
            self.__elapsed_time = time.time() - start_time
            self.__spi.close()
            self.__status = 'stopped'

    def stop(self):
        self.__running = False

    def get_data(self, n_count=0):
        return self.__data[-n_count:]

    def get_status(self):
        return self.__status
    
    def get_elapsed_time(self):
        return self.__elapsed_time

    def print_data(self, n_count=0):
        print("Elapsed Time\tADC Value")
        for [elapsed_time, adc_value] in self.get_data(n_count):
            print("{:.6f}".format(elapsed_time) + "\t" + str(adc_value))

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
