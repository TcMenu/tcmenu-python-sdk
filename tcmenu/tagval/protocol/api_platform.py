from collections import namedtuple
from enum import Enum
from functools import lru_cache


class ApiPlatform(Enum):
    """
    Provides a list of the supported platforms as an enumeration. Used during joining
    to indicate the platform of the connecting device.
    """

    Platform = namedtuple("ApiPlatform", ["key", "description"])

    ARDUINO = Platform(0, "Arduino 8-bit")
    JAVA_API = Platform(1, "Java API")
    ARDUINO32 = Platform(2, "Arduino 32-bit")
    DOTNET_API = Platform(3, ".NET API")
    JAVASCRIPT_API = Platform(4, "JS API")
    PYTHON_API = Platform(5, "Python API")

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}>"

    @property
    def key(self) -> str:
        """Platform key."""
        return self._value_.key

    @property
    def description(self) -> str:
        """Platform description."""
        return self._value_.description

    @staticmethod
    @lru_cache(maxsize=6)
    def _from_key_cached(key: int):
        for platform in ApiPlatform:
            if platform.key == key:
                return platform
        raise ValueError(f"No ApiPlatform member found with key {key}")

    @classmethod
    def from_key(cls, key: int) -> "ApiPlatform":
        """Returns the enum member matching the given key."""
        return cls._from_key_cached(key)
