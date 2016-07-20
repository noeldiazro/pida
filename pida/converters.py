# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar convertidores de datos
analógico/digitales y digital/analógicos.
"""
from abc import ABCMeta, abstractmethod

class Converter:
    """Clase base abstracta para la definición de convertidores de datos.

    :param channels: número de canales del conversor.
    :param bits: resolución en bits del conversor.
    :param vref: tensión de referencia del conversor.
    :param data_link: enlace de datos para la comunicación con el conversor.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channels, bits, vref, data_link):
        self._channels = channels
        self._bits = bits
        self._vref = vref * 1.0
        self._data_link = data_link

    def open(self):
        """Abre la comunicación con el conversor. Debe invocarse este
        método antes de realizar cualquier lectura/escritura del
        conversor.
        """
        self._data_link.open()

    def close(self):
        """Cierra la comunicación con el conversor. Debe invocarse este
        método tras haber realizado todas las lecturas/escrituras
        requeridas del conversor.
        """
        self._data_link.close()

    @property
    def vref(self):
        """Tensión de referencia del conversor. Es la tensión en voltios
        que se corresponde con el nivel más alto del conversor.

        Es una propiedad de sólo lectura.
        """
        return self._vref

    @property
    def bits(self):
        """Resolución en número de bits del conversor de datos.

        Es una propiedad de sólo lectura.
        """
        return self._bits

    @property
    def levels(self):
        """Resolución en número de niveles del conversor de datos.

        Es una propiedad de sólo lectura.
        """
        return 2 ** self.bits

    @property
    def channels(self):
        """Número de canales del conversor de datos.

        Es una propiedad de sólo lectura.
        """
        return self._channels

    @property
    def data_link(self):
        """Enlace de datos que se usa en la comunicación con el conversor.
        """
        return self._data_link

    @data_link.setter
    def data_link(self, value):
        self._data_link = value


class ADC(Converter):
    """Clase base abstracta para controlar convertidores de datos
    analógico/digitales.

    :param channels: número de canales del conversor.
    :param bits: resolución en bits del conversor.
    :param vref: tensión de referencia del conversor.
    :param data_link: enlace de datos para la comunicación con el conversor.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channels, bits, vref, data_link):
        Converter.__init__(self, channels, bits, vref, data_link)

    @abstractmethod
    def read_code(self, channel):
        """Realiza una lectura de un canal del conversor analógico/digital
        y devuelve el código de su valor.

        :param channel: Canal del conversor que quiere leerse.

        .. warning:: Es un método abstracto. Debe ser implementado por
           cada heredero que defina un modelo concreto de conversor
           analógico/digital.
        """
        pass

    def read(self, channel):
        """Realiza una lectura de un canal del conversor analógico/digital
        y devuelve su valor en voltios.

        :param channel: Canal del conversor que quiere leerse.
        """
        return self.read_code(channel) * self.vref / self.levels

class DAC(Converter):
    """Clase base abstracta para controlar convertidores de datos
    digital/analógicos.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channels, bits, vref, data_link):
        Converter.__init__(self, channels, bits, vref, data_link)

    @abstractmethod
    def write_code(self, value, channel):
        """Fija en un canal del conversor digital/analógico el valor
        especificado como código.

        :param value: Código del valor a escribir.
        :param channel: Canal del conversor que quiere escribirse.

        .. warning:: Es un método abstracto. Debe ser implementado por
           cada heredero que defina un modelo concreto de conversor
           digital/analógico.
        """
        pass

    def write(self, value, channel):
        """
        Fija en un canal del conversor digital/analógico el valor
        especificado en voltios.

        :param value: Valor a fijar en voltios.
        :type value: :class:`Number`
        :param channel: Canal del conversor que quiere escribirse.
        :type channel: :class:`Number`
        """
        return self.write_code(int(value * self.vref / self.levels), channel)

class MCP3002(ADC):
    """Clase para gestionar el convertidor analógico/digital Microchip
    MCP3002.

    :param vref: tensión de referencia del conversor.
    :param data_link: enlace de datos para la comunicación con el conversor.
    """
    def __init__(self, vref, data_link=None):
        ADC.__init__(self, 2, 10, vref, data_link)

    def read_code(self, channel):
        result = self._data_link.transfer([1, (2+channel) << 6, 0])
        return ((result[1] & 0b00011111) << 6) + (result[2]>>2)

class MCP3202(ADC):
    """Clase para gestionar el convertidor analógico/digital Microchip
    MCP3202.

    :param vref: tensión de referencia del conversor.
    :param data_link: enlace de datos para la comunicación con el conversor.

    Ejemplo de uso de un ADC MCP3202 conectado a la línea de selección
    de chip 0 de Raspberry Pi con una tensión de referencia de 3.3V:

    >>> from pida.links import SPIDataLink
    >>> from pida.converters import MCP3202
    >>> link = SPIDataLink(100000, 0, 0)
    >>> adc = MCP3202(3.3, link)
    >>> adc.channels
    2
    >>> adc.bits
    12
    >>> adc.levels
    4096
    >>> adc.vref
    3.3
    >>> adc.data_link
    <pida.links.SPIDataLink object at 0xb6ab3410>
    >>> adc.open()
    >>> adc.read_code(0)
    940
    >>> adc.read(0)
    0.7565185546875
    >>> adc.read_code(1)
    1815
    >>> adc.read(1)
    1.46630859375
    >>> adc.close()
    """
    def __init__(self, vref, data_link=None):
        ADC.__init__(self, 2, 12, vref, data_link)

    def read_code(self, channel):
        result = self._data_link.transfer([1, (2+channel) << 6, 0])
        return ((result[1] & 0b00001111) << 8) + result[2]

class MCP4802(DAC):
    """Clase para gestionar el convertidor digital/analógico Microchip
    MCP4802.

    :param vref: tensión de referencia del conversor.
    :param data_link: enlace de datos para la comunicación con el conversor.
    """
    def __init__(self, vref, data_link=None):
        DAC.__init__(self, 2, 8, vref, data_link)

    def write_code(self, value, channel):
        byte1 = (channel << 7) + (0b011 << 4) + (value >> 4)
        byte2 = (value << 4) & 0xFF
        self._data_link.transfer([byte1, byte2])
