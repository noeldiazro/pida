from abc import ABCMeta

class Interface:
    '''Abstract base class for classes that manage data acquisition interfaces operation'''
    __metaclass__ = ABCMeta

    def __init__(self, identifier, description, channel_list):
        self._identifier = identifier
        self._description = description
        self._channel_list = channel_list

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def channel_list(self):
        return self._channel_list

    # TO DO: remove this method, duplicates 'channel_list' property
    def get_channel_list(self):
        return self._channel_list

    def get_channel_by_id(self, channel_identifier):
        return self._channel_list[channel_identifier]
