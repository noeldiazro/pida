from clock import time, sleep
from threading import Thread, Lock
from numbers import Number
from interfaces import Channel

class Acquisition(Thread):
    '''This class represents an acquisition object'''

    def __init__(self, sampling_rate=0, channel=None, max_count=0):
        Thread.__init__(self)
        self.sampling_rate = sampling_rate
        self.channel = channel
        self.max_count = max_count
        self._data = []
        self._status = 'waiting'
        self._elapsed_time = 0.0
        self._running = True
        self._start_time = 0.0
        # Lock to access start_time
        self.start_time_lock = Lock()
        self.start_time_lock.acquire()
        self.LOCK = Lock()  #For critical section locking
        
        self.daemon = True

    # Sampling rate
    def get_sampling_rate(self):
        return self._sampling_rate

    def set_sampling_rate(self, sampling_rate):
        if not isinstance(sampling_rate, Number):
            raise TypeError("Number expected")

        if sampling_rate > 0:
            self._sampling_rate = 1.0 * sampling_rate
            self._sampling_period = 1.0 / sampling_rate
        elif sampling_rate == 0:
            self._sampling_rate = 0.0
            self._sampling_period = 0.0
        else:
            raise TypeError("Positive number expected")

    def del_sampling_rate(self):
        raise AttributeError("Can't delete attribute")

    sampling_rate = property(get_sampling_rate, set_sampling_rate, del_sampling_rate)

    # Channel
    def get_channel(self):
        return self._channel
    
    def set_channel(self, channel):
        
        if not isinstance(channel, Channel):
            raise TypeError("Channel expected")
        self._channel = channel

    def del_channel(self):
        raise AttributeError("Can't delete attribute")

    channel = property(get_channel, set_channel, del_channel)

    # Max count
    def get_max_count(self):
        return self._max_count

    def set_max_count(self, max_count):
        if not isinstance(max_count, Number):
            raise TypeError("Number expected")
        if max_count >= 0:
            self._max_count = int(max_count)
        else:
            raise TypeError("Positive number expected")
    
    def del_max_count(self):
        raise AttributeError("Can't delete attribute")

    max_count = property(get_max_count, set_max_count, del_max_count)

    # Data
    def get_data(self, n_count=0):
        return self._data[-n_count:]
    
    data = property(get_data)

    def print_data(self, n_count=0):
        print("Elapsed Time\tValue")
        for [elapsed_time, adc_value] in self.get_data(n_count):
            print("{:.6f}".format(elapsed_time) + "\t" + str(adc_value))

    # Status
    def get_status(self):
        return self._status
    
    status = property(get_status)

    # Elapsed Time
    def get_elapsed_time(self):
        return self._elapsed_time

    elapsed_time = property(get_elapsed_time)

    # Start Time
    @property
    def start_time(self):
        return self._start_time

#    def start(self):
    def run(self):
        # Open channel
        self.channel.open() 
        self._status = 'running'

        self._start_time = time()
        self.start_time_lock.release()

        request = self._start_time
        i=0
        while self._running and (self._max_count == 0 or i < self._max_count):
            # Calculate iteration end time
            request += self._sampling_period

            # Add new data poing
            self._elapsed_time = time() - self._start_time
            value = self.channel.read()
            self._data.append([self._elapsed_time, value])
            
            # Sleep till iteration end time
            sleep(request)            
            i = i + 1

        self._elapsed_time = time() - self._start_time
        self.channel.close()
        self._status = 'stopped'

    def stop(self):
        self._running = False
