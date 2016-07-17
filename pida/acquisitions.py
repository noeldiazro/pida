""":mod:`piDA.acquisitions` --- Data Acquisitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from abc import ABCMeta, abstractmethod
from threading import Thread, Lock
from clock import time, sleep

class Acquisition(Thread):
    """Abstract base class for classes that represent a data acquisition.

    :param channel: the channel of an interface to acquire data from
    :type channel: :class:`piDA.interfaces.Channel`
    :param max_count: maximum number of data samples to take
    :type max_count: :class:`Integer`
    :param identifier: identifier of the data acquisition
    :type identifier: :class:`Integer`
    :param description: description of the data acquisition
    :type description: :class:`String`

    """
    __metaclass__ = ABCMeta

    def __init__(self, channel=None, max_count=0):
        Thread.__init__(self)
        self._channel = None
        self._max_count = 0
        self.channel = channel
        self.max_count = max_count
        self._data = []
        self._status = 'waiting'
        self._elapsed_time = 0.0
        self._running = True
        self._start_time = 0.0
        # Lock to access start_time
        self.start_time_lock = Lock()
        """."""

        self.start_time_lock.acquire()
        self.daemon = True

    # Channel
    @property
    def channel(self):
        """."""
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @channel.deleter
    def channel(self):
        raise AttributeError("Can't delete attribute")

    # Max count
    @property
    def max_count(self):
        """."""
        return self._max_count

    @max_count.setter
    def max_count(self, max_count):
        if max_count < 0:
            raise ValueError("Positive number expected")
        self._max_count = int(max_count)

    @max_count.deleter
    def max_count(self):
        raise AttributeError("Can't delete attribute")

    # Data
    def get_data(self, n_count=0):
        """."""
        return self._data[-n_count:]

    def print_data(self, n_count=0):
        """."""
        print "Elapsed Time\tValue"
        for [elapsed_time, adc_value] in self.get_data(n_count):
            print "{:.6f}".format(elapsed_time) + "\t" + str(adc_value)

    # Status
    @property
    def status(self):
        """."""
        return self._status

    # Elapsed Time
    @property
    def elapsed_time(self):
        """."""
        return self._elapsed_time

    # Start Time
    @property
    def start_time(self):
        """."""
        return self._start_time

    @abstractmethod
    def run(self):
        """."""
        pass

    def stop(self):
        """."""
        self._running = False

class SynchronousAcquisition(Acquisition):
    """This class represents a synchrounous data acquisition.

    :param channel: the channel of an interface to acquire data from
    :type channel: :class:`piDA.interfaces.Channel`
    :param max_count: maximum number of data samples to take
    :type max_count: :class:`Integer`
    :param sampling_rate: sampling rate of the acquisition
    :param identifier: identifier of the data acquisition
    :type identifier: :class:`Integer`
    :param description: description of the data acquisition
    :type description: :class:`String`

    """

    def __init__(self, channel=None, max_count=0, sampling_rate=0):
        Acquisition.__init__(self, channel, max_count)
        self._sampling_rate = 0.0
        self._sampling_period = 0.0
        self.sampling_rate = sampling_rate

    # Sampling rate
    @property
    def sampling_rate(self):
        """."""
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sampling_rate):
        if sampling_rate > 0:
            self._sampling_rate = 1.0 * sampling_rate
            self._sampling_period = 1.0 / sampling_rate
        elif sampling_rate == 0:
            self._sampling_rate = 0.0
            self._sampling_period = 0.0
        else:
            raise TypeError("Positive number expected")

    @sampling_rate.deleter
    def sampling_rate(self):
        raise AttributeError("Can't delete attribute")

    def run(self):
        """."""
        # Open channel
        self.channel.open()
        self._status = 'running'

        self._start_time = time()
        self.start_time_lock.release()

        request = self._start_time
        i = 0
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
