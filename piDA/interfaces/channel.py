class Channel():
    '''This class representes a channel of an interface'''

    def __init__(self, identifier, adc, adc_channel):
        self._identifier = identifier
        self._adc = adc
        self._adc_channel = adc_channel

    @property
    def identifier(self):
        return self._identifier

    def open(self):
        self._adc.open()

    def close(self):
        self._adc.close()

    def read(self):
        return self._adc.read(self._adc_channel)
