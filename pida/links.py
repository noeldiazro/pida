""":mod:`piDA.links` --- Data Links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from abc import ABCMeta, abstractmethod
from pida import PidaObject
from spidev import SpiDev

class DataLink(PidaObject):
    """Abstract base class for data link definitions.

    :param max_speed: maximum speed (hertzs) of the data link
    :type description: :class:`Number`
    :param identifier: identifier of the data link
    :type identifier: :class:`Integer`
    :param description: description of the data link
    :type description: :class:`String`

    """
    __metaclass__ = ABCMeta

    def __init__(self, max_speed, identifier=0, description=""):
        PidaObject.__init__(self, identifier, description)
        self.max_speed = max_speed
        """Maximum speed in hertzs of the data link."""

    @abstractmethod
    def open(self):
        """Open data link. This method must be called before making
        the first transference through the link.

        .. warning:: Abstract method.

        """
        pass

    @abstractmethod
    def close(self):
        """Close data link. Call this method after all transferences
        have been performed.

        .. warning:: Abstract method.

        """
        pass

    @abstractmethod
    def transfer(self, data):
        """Send given data through the data link to a device. Return
        data that device sends back in response.

        :param data: data (bytes) to send.
        :type data: :class:`List`

        .. warning:: Abstract method.
        """
        pass


class SPIDataLink(DataLink):
    """Class for Serial Peripheral Interface (SPI) management.

    :param max_speed: maximum speed (hertzs) of the data link
    :type description: :class:`Number`
    :param bus: SPI bus identifier used by the data link
    :type bus: :class:`Integer`
    :param device: SPI chip select line used by the data link
    :type device: :class:`Integer`
    :param identifier: identifier of the data link
    :type identifier: :class:`Integer`
    :param description: description of the data link
    :type description: :class:`String`

    """
    def __init__(self, max_speed, bus, device, identifier=0, description=""):
        DataLink.__init__(self, max_speed, identifier, description)
        self._bus = bus
        self._device = device
        self._spi = SpiDev()

    @property
    def bus(self):
        """SPI bus identifier used by the data link.

        .. note:: Raspberry Pi has a single SPI bus that can be
           accessed through the GPIO port. Its identifier is 0.

        """
        return self._bus

    @property
    def device(self):
        """SPI chip select line used by the data link.

        .. note:: Raspberry Pi's SPI bus 0 can enable two chip select
           lines. Their identifiers are 0 and 1.

        """
        return self._device

    def open(self):
        """Open data link. This method must be called before making
        the first transference through the link."""
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = self.max_speed

    def close(self):
        """Close data link. Call this method after all transferences
        have been performed."""
        self._spi.close()

    def transfer(self, data):
        """Send given data through the data link to a device. Return
        data that device sends back in response.

        :param data: data (bytes) to send.
        :type data: :class:`List`

        """
        return self._spi.xfer2(data)
