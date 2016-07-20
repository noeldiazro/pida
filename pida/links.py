# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar enlaces de datos."""
from abc import ABCMeta, abstractmethod
from spidev import SpiDev

class DataLink:
    """Clase base abstracta para la definición de enlaces de datos.

    :param max_speed: máxima velocidad en herzios del enlace de datos.
    """
    __metaclass__ = ABCMeta

    def __init__(self, max_speed):
        self._max_speed = max_speed

    @property
    def max_speed(self):
        """Velocidad máxima en herzios del enlace de datos.

        Es una propiedad de sólo lectura.
        """
        return self._max_speed

    @abstractmethod
    def open(self):
        """Abre el enlace de datos. Este método debe invocarse antes de
        realizar la primera transferencia por el enlace.

        .. warning:: Es un método abstracto que debe ser implementado por todas las clases que hereden de ésta.
        """
        pass

    @abstractmethod
    def close(self):
        """Cierra el enlace de datos. Debe invocarse este método cuando no
        vayan a realizarse más transferencias de datos a través del
        enlace.

        .. warning:: Es un método abstracto que debe ser implementado por todas las clases que hereden de ésta.
        """
        pass

    @abstractmethod
    def transfer(self, data):
        """Transfiere datos entre el equipo y un dispositivo conectado
        al mismo a través del enlace de datos. 

        :param data: lista con los datos a enviar. Cada elemento de la lista es un byte.
        :return: lista con la respuesta recibida desde el dispositivo. Cada elemento de la lista es un byte.

        .. warning:: Es un método abstracto que debe ser implementado por todas las clases que hereden de ésta.
        """
        pass


class SPIDataLink(DataLink):
    """Clase que gestiona un enlace Serial Peripheral Interface (SPI).

    :param max_speed: máxima velocidad en herzios del enlace de datos.
    :param bus: Identificador del bus SPI que se usa para el enlace de datos.
    :param device: Línea de selección de chip SPI activa en el enlace de datos.

    Ejemplo de uso para pedir una medida del primer canal analógico de un
    conversor ADC MCP3202 conectado a la línea de selección de chip 0 de Raspberry Pi:

    >>> from pida.links import SPIDataLink
    >>> link = SPIDataLink(1000000, 0, 0)
    >>> link.open()
    >>> request = [1, 2 << 6, 0]
    >>> response = link.transfer(request)
    >>> link.close()
    """
    def __init__(self, max_speed, bus, device):
        DataLink.__init__(self, max_speed)
        self._bus = bus
        self._device = device
        self._spi = SpiDev()
        
    @property
    def bus(self):
        """Identificador del bus SPI que se usa para el enlace de datos.

        .. note:: Raspberry Pi ofrece a través de su puerto GPIO
                  un único bus SPI cuyo identificador es 0.

        Es una propiedad de sólo lectura.
        """
        return self._bus

    @property
    def device(self):
        """Línea de selección de chip SPI activa en el enlace de datos.

        .. note:: El bus SPI 0 de Raspberry Pi puede, a través del puerto GPIO,
                  activar dos líneas de selección de chip SPI: 0 y 1.

        Es una propiedad de sólo lectura.
        """
        return self._device

    def open(self):
        self._spi.open(self._bus, self._device)
        self._spi.max_speed_hz = self.max_speed

    def close(self):
        self._spi.close()

    def transfer(self, data):
        return self._spi.xfer2(data)
