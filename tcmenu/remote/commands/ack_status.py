from collections import namedtuple
from enum import Enum


class AckStatus(Enum):
    """
    An enumeration that represents all the possible status / error return codes from the tagval.
    """

    Status = namedtuple("AckStatus", ["description", "status_code"])

    """ This is a warning that the value was out of range. """
    VALUE_RANGE_WARNING = Status("Value out of range", -1)

    """ The operation was successful. """
    SUCCESS = Status("OK", 0)

    """ The requested ID was not found. """
    ID_NOT_FOUND = Status("ID not found", 1)

    """ The credentials provided were incorrect. """
    INVALID_CREDENTIALS = Status("Invalid Credentials", 2)

    """ There was an error that is not categorised. """
    UNKNOWN_ERROR = Status("Unknown Error", 10000)

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}>"

    @property
    def description(self) -> str:
        """Description of the status."""
        return self._value_.description

    @property
    def status_code(self) -> int:
        """Integer wire code for the status."""
        return self._value_.status_code

    def is_error(self) -> bool:
        """:return: True if the status code is an error, otherwise False."""
        return self._value_.status_code > 0

    @classmethod
    def from_status_code(cls, status_code: int):
        """Retrieve status based on numeric code."""
        for status in cls:
            if status.status_code == status_code:
                return status
        return AckStatus.UNKNOWN_ERROR
