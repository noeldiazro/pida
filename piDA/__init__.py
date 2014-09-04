""":mod:`piDA` --- piDA
~~~~~~~~~~~~~~~~~~~~~~~

"""
from abc import ABCMeta

class piDAObject(object):
    """Abstract base class for all objects in :mod:`piDA` library."""
    __metaclass__ = ABCMeta

    def __init__(self, identifier="", description=""):
        self._identifier = identifier
        self._description = description

    @property
    def identifier(self):
        """Identifier of the :mod:`piDA` object.

        *Read-only* property."""
        return self._identifier

    @property
    def description(self):
        """Description of the :mod:`piDA` object.

        *Read-only* property."""
        return self._description
