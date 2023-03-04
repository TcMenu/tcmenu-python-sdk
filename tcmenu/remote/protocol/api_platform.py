from collections import namedtuple
from enum import Enum


class ApiPlatform(Enum):
    """
    Provides a list of the supported platforms as an enumeration. Used during joining
    to indicate the platform of the connectee.
    """
    Platform = namedtuple('ApiPlatform', ['key', 'description'])

    ARDUINO = Platform(0, "Arduino 8-bit")
    ARDUINO32 = Platform(2, "Arduino 32-bit")
    JAVA_API = Platform(1, "Java API")
    DNET_API = Platform(3, ".NET API")
    JAVASCRIPT_CLIENT = Platform(4, "JS API")
    PYTHON_API = Platform(5, "Python API")

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}>"

    @property
    def key(self) -> str:
        """ Platform key. """
        return self._value_.key

    @property
    def description(self) -> str:
        """ Platform description. """
        return self._value_.description
