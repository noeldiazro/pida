# -*- coding: utf-8 -*-
"""Este módulo incluye clases para gestionar interfaces de adquisición de
datos.
"""
from abc import ABCMeta
from pida.converters import MCP3002, MCP3202, MCP4802
from pida.links import SPIDataLink
from pida.acquisitions import SynchronousAcquisition

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

    def acquire(self, max_count=0, sampling_rate=0):
        """Comienza una adquisición de datos a través del canal y devuelve el
        objeto para controlar dicha adquisición.
        
        :param max_count: número máximo de muestras a tomar en la adquisición.
            El valor por defecto (0) indica que no hay límite.
        :param sampling_rate: frecuencia de muestreo en hertzios. El valor
            por defecto (0) provoca que las muestras se tomen a la máxima
            tasa posible.

        Ejemplo de adquisición síncrona a través del canal de entrada 0
        de la interfaz de adquisición de datos PidaInterface, con un número
        ilimitado de muestras y una frecuencia de muestreo de 1Hz:

        >>> from pida.interfaces import InterfaceBuilder
        >>> interface = InterfaceBuilder().build("PidaInterface")
        >>> channel0 = interface.get_channel_by_id(0)
        >>> acquisition = channel0.acquire(0, 1)
        >>> acquisition.start()
        >>> acquisition.print_data(5)
        Elapsed Time    Value
        12.000181       1.46389160156
        13.000177       1.46389160156
        14.000171       1.46469726562
        15.000166       1.46389160156
        16.000172       1.46469726562
        >>> acquisition.print_data(5)
        Elapsed Time    Value
        24.000167       3.29919433594
        25.000172       3.29919433594
        26.000168       3.29919433594
        27.000174       3.29919433594
        28.000168       3.29919433594
        >>> acquisition.status
        'running'
        >>> acquisition.stop()
        >>> acquisition.status
        'stopped'
        """
        acquisition = SynchronousAcquisition(self, max_count, sampling_rate)
        acquisition.start()
        return acquisition
        
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
    """Clase que gestiona una interfaz de adquisición de datos.

    :param identifier: identificador de la interfaz.
    :param description: descripción de la interfaz.
    :param channel_list: lista de canales de la interfaz. Cada elemento de la lista es un objeto :class:`Channel`.
    """
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

class InterfaceBuilder:
    """Clase para definir las interfaces de adquisición de datos.
    """

    def build(self, interface_id):
        """Devuelve un objeto para controlar la interfaz de adquisición de datos
        con el identificador que se pasa como argumento.

        :param interface_id: identificador de la interfaz de adquisición de datos.

        Eleva una excepción :exc:`ValueError` si no se reconoce el identificador.
        En la actualidad se pueden utilizar los siguientes identificadores:

        - "PidaInterface"
        - "PidaInterface0"
        - "Gertboard"

        Ejemplo de uso para generar distintas interfaces:

        >>> from pida.interfaces import InterfaceBuilder
        >>> builder = InterfaceBuilder()
        >>> pidaInterface = builder.build("PidaInterface")
        >>> pidaInterface0 = builder.build("PidaInterface0")
        >>> gertboard = builder.build("Gertboard")
        >>> builder.build("Spam")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "pida/interfaces.py", line 143, in build
            raise ValueError("Unknown interface")
        ValueError: Unknown interface
        """
        if interface_id == "PidaInterface":
            return self._build_pida_interface()
        elif interface_id == "PidaInterface0":
            return self._build_pida_interface_0()
        elif interface_id == "Gertboard":
            return self._build_gertboard()
        else:
            raise ValueError("Unknown interface")
        
    def _build_pida_interface(self):
        identifier = "PidaInterface"
        description = ""

        link0 = SPIDataLink(0, 0)
        link0.max_speed_hz = 100000
        adc0 = MCP3202(3.3, link0)
        
        link1 = SPIDataLink(0, 1)
        link1.max_speed_hz = 100000
        adc1 = MCP3202(3.3, link1)

        channel_list = [
            InputChannel(adc0, 1),
            InputChannel(adc0, 0),
            InputChannel(adc1, 1),
            InputChannel(adc1, 0)
        ]
        return Interface(identifier, description, channel_list)

    def _build_pida_interface_0(self):
        identifier = "PidaInterface0"
        description = ""

        link0 = SPIDataLink(0, 0)
        link0.max_speed_hz = 1000000
        adc0 = MCP3202(3.3, link0)

        channel_list = [
            InputChannel(adc0, 0),
            InputChannel(adc0, 1)
            ]
        return Interface(identifier, description, channel_list)

    def _build_gertboard(self):
        identifier = "Gertboard"
        description = ""

        link0 = SPIDataLink(0, 0)
        link0.max_speed_hz = 1000000        
        adc0 = MCP3002(3.3, link0)

        link1 = SPIDataLink(0, 1)
        link1.max_speed_hz = 1000000        
        dac0 = MCP4802(2.048, link1)

        channel_list = [
            InputChannel(adc0, 0),
            InputChannel(adc0, 1),
            OutputChannel(dac0, 0),
            OutputChannel(dac0, 1)
            ]
        return Interface(identifier, description, channel_list)
