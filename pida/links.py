# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar enlaces de datos."""
from abc import ABCMeta, abstractmethod
from spidev import SpiDev

class DataLink(object):
    """Clase base abstracta para la definición de enlaces de datos.
    """
    __metaclass__ = ABCMeta

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

class FullDuplexDataLink(DataLink):
    """Clase base abstracta que define la interfaz de enlaces de detos full-duplex.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def transfer(self, data):
        """Transfiere datos entre el equipo y un dispositivo conectado
        al mismo a través del enlace de datos. 

        :param data: lista con los datos a enviar. Cada elemento de la lista es un byte.
        :return: lista con la respuesta recibida desde el dispositivo. Cada elemento de la lista es un byte.

        .. warning:: Es un método abstracto que debe ser implementado por todas las clases que hereden de ésta.
        """
        pass


class SPIDataLinkConfiguration(object):
    def __init__(self, mode, max_speed_hz):
        self._mode = mode
        self._max_speed_hz = max_speed_hz

    @property
    def mode(self):
        return self._mode

    @property
    def max_speed_hz(self):
        return self._max_speed_hz

    
class SPIDataLink(FullDuplexDataLink):
    """Clase que gestiona un enlace Serial Peripheral Interface (SPI).

    :param bus: Identificador del bus SPI que se usa para el enlace de datos.
    :param device: Línea de selección de chip SPI activa en el enlace de datos.
    :param configuration: Configuración del enlace de datos

    Ejemplo de uso:

    >>> from pida.links import SPIDataLinkConfiguration, SPIDataLink
    >>> configuration = SPIDataLinkConfiguration(mode=0, max_speed_hz=32000000)
    >>> with SPIDataLink(0, 0, configuration) as link:
            request = [0x00, 0x01, 0xFF]
            response = link.transfer(request)
    >>> response
    [0, 1, 255]
    """
    def __init__(self, bus, device, configuration):
        self._bus = bus
        self._device = device
        self._configuration = configuration
        self._spi = SpiDev()

    def _apply_configuration(self):
        self._spi.mode = self._configuration.mode
        self._spi.max_speed_hz = self._configuration.max_speed_hz

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
        self._apply_configuration()

    def close(self):
        self._spi.close()

    def transfer(self, data):
        return self._spi.xfer2(data)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def max_speed_hz(self):
        return self._configuration.max_speed_hz

    @property
    def mode(self):
        return self._configuration.mode
