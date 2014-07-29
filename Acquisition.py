from clock import time, sleep
import spidev
import threading

class Acquisition(threading.Thread):
    '''This class represents an acquisition object'''

    def __init__(self, sampling_rate=0, channel=0, max_count=0):
        threading.Thread.__init__(self)
        self._sampling_rate = sampling_rate
        if sampling_rate != 0:
            self._sampling_period = 1.0/sampling_rate
        else:
            self._sampling_period = 0
        self._channel = channel
        self._max_count = max_count
        self._data = []
        self._status = 'waiting'
        self._spi = spidev.SpiDev()
        self._running = True
        self._elapsed_time = 0

    def set_sampling_rate(self, sampling_rate):
        self._sampling_rate = sampling_rate
        self._sampling_period = 1.0/sampling_rate

    def get_sampling_rate(self):
        return self._sampling_rate

    def set_channel(self, channel):
        self._channel = channel

    def get_channel(self):
        return self._channel

    def set_max_count(self, max_count):
        self._max_count = max_count
    
    def get_max_count(self):
        return self._max_count

#    def start(self):
    def run(self):
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 1000000
        self._status = 'running'

        start_time = time()
        request = start_time
        while self._running and (self._max_count == 0 or i < self._max_count):
            # Calculate iteration end time
            request += self._sampling_period

            # Add new data poing
            self._elapsed_time = time() - start_time
            adc_value = self._get_adc_value()
            self._data.append([self._elapsed_time, adc_value])
            
            # Sleep till iteration end time
            sleep(request)

        self._elapsed_time = time() - start_time
        self._spi.close()
        self._status = 'stopped'

    def stop(self):
        self._running = False

    def get_data(self, n_count=0):
        return self._data[-n_count:]

    def get_status(self):
        return self._status
    
    def get_elapsed_time(self):
        return self._elapsed_time

    def print_data(self, n_count=0):
        print("Elapsed Time\tADC Value")
        for [elapsed_time, adc_value] in self.get_data(n_count):
            print("{:.6f}".format(elapsed_time) + "\t" + str(adc_value))

    def _get_adc_value(self):
        # MCP3008
        #ret = self._spi.xfer2([1, (8 + self.get_channel()) << 4, 0])
        #return ((ret[1]&3) << 8) + ret[2]
        # MCP3002
        #r = self._spi.xfer2([1,(2+self.get_channel()) << 6,0])
        #return ((r[1]&31) << 6) + (r[2]>>2)
        # MCP3202
        r = self._spi.xfer2([1,(2+self.get_channel()) << 6,0])
        return ((r[1] & 0b00001111) << 8) + r[2]
