# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar interfaces de adquisición de
datos.
"""
from abc import ABCMeta
from pida.converters import MCP3002, MCP3202, MCP4802
from pida.links import SPIDataLink

class Channel:
    """Clase base abstracta para la gestión de un canal de una interfaz de adquisición de datos.

    :param converter: conversor de datos asociado al canal.
    :param converter_channel: canal del conversor de datos asociado al canal.
    """
    __metaclass__ = ABCMeta

    def __init__(self, converter, converter_channel):
        self._converter = converter
        self._converter_channel = converter_channel

    @property
    def converter(self):
        """Conversor de datos asociado al canal.

        Es una propiedad de sólo lectura.
        """
        return self._converter

    @property
    def converter_channel(self):
        """Canal del conversor de datos asociado al canal.

        Es una propiedad de sólo lectura.
        """
        return self._converter_channel

    def open(self):
        """Abre el canal. Es necesario invocar este método antes de
        realizar la primera escritura/lectura del canal.
        """
        self._converter.open()

    def close(self):
        """Cierra el canal."""
        self._converter.close()

class InputChannel(Channel):
    """Clase para la gestión de un canal de entrada de una interfaz de
    adquisición de datos.

    :param converter: conversor de datos asociado al canal.
    :param converter_channel: canal del conversor de datos asociado al canal.
    """
    def __init__(self, converter, converter_channel):
        Channel.__init__(self, converter, converter_channel)

    def read(self):
        """Lee un valor en voltios en el canal."""
        return self._converter.read(self._converter_channel)

class OutputChannel(Channel):
    """Clase para la gestión de un canal de salida de una interfaz de
    adquisición de datos.

    :param converter: conversor de datos asociado al canal.
    :param converter_channel: canal del conversor de datos asociado al canal.
    """
    def __init__(self, converter, converter_channel):
        Channel.__init__(self, converter, converter_channel)

    def write(self, value):
        """Escribe un valor en voltios en el canal."""
        return self._converter.write(value, self._converter_channel)

class Interface:
    """Clase que define una interfaz de adquisición de datos.

    :param identifier: identificador de la interfaz.
    :param description: descripción de la interfaz.
    :param channel_list: lista de canales de la interfaz. Cada elemento de la lista es un objeto :class:`Channel`.
    """
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, channel_list):
        self._identifier = identifier
        self._description  = description
        self._channel_list = channel_list

    @property
    def identifier(self):
        """Identificador de la interfaz.

        Es una propiedad de sólo lectura."""
        return self._identifier

    @property
    def description(self):
        """Descripción de la interfaz.

        Es una propiedad de sólo lectura."""
        return self._description

    @property
    def channel_list(self):
        """Lista de canales de la interfaz. Cada elemento de la lista es un
        objeto :class:`Channel`.
        
        Es una propiedad de sólo lectura.
        """
        return self._channel_list

    # TO DO: remove this method, duplicates 'channel_list' property
    def get_channel_list(self):
        """Devuelve la lista de canales de la interfaz."""
        return self._channel_list

    def get_channel_by_id(self, channel_identifier):
        """Busca en la lista de canales de la interfaz y devuelve el canal
        que se corresponde con el identificador suministrado."""
        return self._channel_list[channel_identifier]

class PidaInterface(Interface):
    """Clase para gestionar la interfaz de adquisición de datos piDAInterface."""
    def __init__(self):
        identifier = "piDA Interface 1"
        description = ""
        link0 = SPIDataLink(100000, 0, 0)
        adc0 = MCP3202(3.3, link0)
        link1 = SPIDataLink(100000, 0, 1)
        adc1 = MCP3202(3.3, link1)
        channel_list = [
            InputChannel(adc0, 1),
            InputChannel(adc0, 0),
            InputChannel(adc1, 1),
            InputChannel(adc1, 0)
            ]
        Interface.__init__(self, identifier, description, channel_list)

class PidaInterface0(Interface):
    """Clase para gestionar la interfaz de adquisición de datos piDAInterface 0."""
    def __init__(self):
        identifier = "piDA Interface 0"
        description = ""
        link0 = SPIDataLink("", "", 1000000, 0, 0)
        adc0 = MCP3202("", "", 3.3, link0)
        channel_list = [
            InputChannel(0, "", adc0, 0),
            InputChannel(1, "", adc0, 1)
            ]
        Interface.__init__(self, identifier, description, channel_list)

class Gertboard(Interface):
    """Clase para gestionar la interfaz de adquisición de datos Gertboard."""
    def __init__(self):
        identifier = "Gertboard"
        description = ""
        link0 = SPIDataLink("", "", 1000000, 0, 0)
        adc0 = MCP3002("", "", 3.3, link0)
        link1 = SPIDataLink("", "", 1000000, 0, 1)
        dac0 = MCP4802("", "", 2.048, link1)
        channel_list = [
            InputChannel(0, "", adc0, 0),
            InputChannel(1, "", adc0, 1),
            OutputChannel(2, "", dac0, 0),
            OutputChannel(3, "", dac0, 1)
            ]
        Interface.__init__(self, identifier, description, channel_list)
