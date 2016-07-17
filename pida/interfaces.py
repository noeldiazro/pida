""":mod:`piDA.interfaces` --- Data Acquisition interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from abc import ABCMeta
from pida.converters import MCP3002, MCP3202, MCP4802
from pida.links import SPIDataLink

class Channel:
    """Class to define a channel of a data acquisition interface.

    :param converter: data converter associated with the channel
    :type converter: :class:`piDA.converters.Converter`
    :param converter_channel: data converter channel associated with
       the channel
    :type converter_channel: :class:`Integer`

    """
    __metaclass__ = ABCMeta

    def __init__(self, converter, converter_channel):
        self._converter = converter
        self._converter_channel = converter_channel

    @property
    def converter(self):
        """.

        *Read-only* property.

        """
        return self._converter

    @property
    def converter_channel(self):
        """.

        *Read-only* property.

        """
        return self._converter_channel

    def open(self):
        """."""
        self._converter.open()

    def close(self):
        """."""
        self._converter.close()

class InputChannel(Channel):
    """Class that manages an input channel of an interface.

    :param converter: data converter associated with the channel
    :type converter: :class:`piDA.converters.Converter`
    :param converter_channel: data converter channel associated with
       the channel
    :type converter_channel: :class:`Integer`
    """
    def __init__(self, converter, converter_channel):
        Channel.__init__(self, converter, converter_channel)

    def read(self):
        """."""
        return self._converter.read(self._converter_channel)

class OutputChannel(Channel):
    """Class that manages an output channel of an interface.

    :param converter: data converter associated with the channel
    :type converter: :class:`piDA.converters.Converter`
    :param converter_channel: data converter channel associated with
       the channel
    :type converter_channel: :class:`Integer`

    """
    def __init__(self, converter, converter_channel):
        Channel.__init__(self, converter, converter_channel)

    def write(self, value):
        """."""
        return self._converter.write(value, self._converter_channel)

class Interface:
    """Abstract base class for classes that manage data acquisition interfaces operation.

    :param channel_list:
    :type channel_list:
    """
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, channel_list):
        self._identifier = identifier
        self._description  = description
        self._channel_list = channel_list

    @property
    def identifier(self):
        """."""
        return self._identifier

    @property
    def description(self):
        """."""
        return self._description

    @property
    def channel_list(self):
        """."""
        return self._channel_list

    # TO DO: remove this method, duplicates 'channel_list' property
    def get_channel_list(self):
        """."""
        return self._channel_list

    def get_channel_by_id(self, channel_identifier):
        """."""
        return self._channel_list[channel_identifier]

class PidaInterface(Interface):
    """Definition of interface 'piDA Interface 1'."""
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
    """Definition of interface 'piDA Interface 0'."""
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
    """Definition of interface 'Gertboard'."""
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
