""":mod:`piDA.converters` --- Data Converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from abc import ABCMeta, abstractmethod, abstractproperty
from piDA import piDAObject

class Converter(piDAObject):
    """Abstract base class for classes that manage data converters.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
    __metaclass__ = ABCMeta

    def __init__(self, vref, data_link, identifier=0, description=""):
        piDAObject.__init__(self, identifier, description)
        self._vref = vref * 1.0
        self._data_link = data_link
        
    def open(self):
        """Open communication with the converter. Call this method
        before reading/writing from/to the converter.

        """
        self._data_link.open()

    def close(self):
        """Close communication with the converter. Call this method
        after all readings/writings have been performed.

        """
        self._data_link.close()

    @property
    def vref(self):
        """Reference voltage of the converter. It is the analog
        voltage that corresponds to the highest level of the
        converter.

        *Read-only* property.

        """
        return self._vref

    @abstractproperty
    def bits(self):
        """Bit resolution of the data converter.

        *Read-only* property.

        .. warning:: Abstract property.

        """
        pass

    @property
    def levels(self):
        """Level resolution of the data converter.

        *Read-only* property.

        """
        return 2 ** self.bits

    @abstractproperty
    def channels(self):
        """Number of channels of the data converter.

        *Read-only* property.

        .. warning:: Abstract property.

        """
        pass

    @property
    def data_link(self):
        """Data link used to communicate with the data converter.

        """
        return self._data_link

    @data_link.setter
    def data_link(self, value):
        self._data_link = value


class ADC(Converter):
    """Abstract base class for classes that manage Analog/Digital converter operation.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
    __metaclass__ = ABCMeta

    def __init__(self, vref, data_link, identifier=0, description=""):
        Converter.__init__(self, vref, data_link, identifier, description)
        self._factor = self._vref / self.levels

    @abstractmethod
    def read_code(self, channel):
        """Read given channel of the ADC and return code value.

        :param channel: channel of the converter to read from.
        :type channel: :class:`Integer`

        .. warning:: Abstract method.

        """
        pass

    def read(self, channel):
        """Read given channel of the ADC and return voltage value.

        :param channel: channel of the converter to read from.
        :type channel: :class:`Integer`

        """
        return self.read_code(channel) * self._factor

class DAC(Converter):
    """Abstract base class for classes that manage Digital/Analog converter operation.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
    __metaclass__ = ABCMeta

    def __init__(self, vref, data_link, identifier=0, description=""):
        Converter.__init__(self, vref, data_link, identifier, description)
        self._factor = self.levels / self._vref  

    @abstractmethod
    def write_code(self, value, channel):
        """Write given code value on given channel of the DAC.

        :param value: code value to write.
        :type value: :class:`Integer`
        :param channel: channel of the converter to read from.
        :type channel: :class:`Integer`

        .. warning:: Abstract method.

        """
        pass

    def write(self, value, channel):
        """Write given voltage value on given channel of the DAC.

        :param value: voltage value to write.
        :type value: :class:`Number`
        :param channel: channel of the converter to write to.
        :type channel: :class:`Integer`

        """
        return self.write_code(int(value * self._factor), channel)

class MCP3002(ADC):
    """Class that manages Microchip's MCP3002 Analog-to-Digital converter.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`    
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
    def __init__(self, vref, data_link=None, identifier=0, description=""):
        ADC.__init__(self, vref, data_link, identifier, description)

    @property
    def bits(self):
        """Bit resolution of the data converter.

        *Read-only* property.

        """
        return 10

    @property
    def channels(self):
        """Number of channels of the data converter.

        *Read-only* property.

        """
        return 2

    def read_code(self, channel):
        """Read given channel of the ADC and return code value.

        :param channel: channel of the converter to read from.
        :type channel: :class:`Integer`

        """
        r = self._data_link.transfer([1,(2+channel) << 6,0])
        return ((r[1] & 0b00011111) << 6) + (r[2]>>2)

class MCP3202(ADC):
    """Class that manages Microchip's MCP3202 Analog-to-Digital converter.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`    
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
    def __init__(self, vref, data_link=None, identifier=0, description=""):
        ADC.__init__(self, vref, data_link, identifier, description)

    @property
    def bits(self):
        """Bit resolution of the data converter.

        *Read-only* property.

        """
        return 12

    @property
    def channels(self):
        """Number of channels of the data converter.

        *Read-only* property.

        """
        return 2

    def read_code(self, channel):
        """Read given channel of the ADC and return code value.

        :param channel: channel of the converter to read from.
        :type channel: :class:`Integer`

        """
        r = self._data_link.transfer([1,(2+channel) << 6,0])
        return ((r[1] & 0b00001111) << 8) + r[2]

class MCP4802(DAC):
    """Class that manages Microchip's MCP4802 Digital-to-Analog converter.

    :param vref: reference voltage of the converter
    :type vref: :class:`Number`
    :param data_link: data link used to communicate with the converter
    :type data_link: :class:`piDA.links.DataLink`
    :param identifier: identifier of the converter
    :type identifier: :class:`Integer`
    :param description: description of the converter
    :type description: :class:`String`

    """
#    def __init__(self, vref=2.048, data_link):
    def __init__(self, vref, data_link=None, identifier=0, description=""):
        DAC.__init__(self, vref, data_link, identifier, description)

    @property
    def bits(self):
        """Bit resolution of the data converter.

        *Read-only* property.

        """
        return 8

    @property
    def channels(self):
        """Number of channels of the data converter.

        *Read-only* property.

        """
        return 2

    def write_code(self, value, channel):
        """Write given code value on given channel of the DAC.

        :param value: code value to write.
        :type value: :class:`Integer`
        :param channel: channel of the converter to write to.
        :type channel: :class:`Integer`

        """
        
        b1 = (channel << 7) + (0b011 << 4) + (value >> 4)
        b2 = (value << 4) & 0xFF
        r = self._data_link.transfer([b1, b2])
