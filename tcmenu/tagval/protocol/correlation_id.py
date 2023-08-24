import time
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class CorrelationId:
    """
    A correlation ID that allows events sent from the client or server to be linked via
    this ID. Calling the constructor with no parameters creates a new correlation. These
    are only unique for a time frame of hours to days. They should not be used for any
    purpose requiring persistence that could extend beyond that.
    """

    COUNTER_MODULO: ClassVar[int] = 1000000
    counter: ClassVar[int] = 0
    correlation: int

    @staticmethod
    def from_string(correlation_as_text: str) -> "CorrelationId":
        """
        Creates a correlation ID with the specified value, for existing correlation IDs.
        :param correlation_as_text: the ID to be represented.
        """
        return CorrelationId(correlation=int(correlation_as_text, 16))

    @staticmethod
    def new_correlation() -> "CorrelationId":
        """
        Creates a new correlation ID that is relatively unique.
        """
        CorrelationId.counter += 1
        time_part: int = int(time.time() * 1000)
        counter_modulo = CorrelationId.counter % CorrelationId.COUNTER_MODULO

        return CorrelationId(correlation=time_part + counter_modulo)

    def __str__(self) -> str:
        """
        Gets the value of the ID as a hex string
        :return: the correlation ID as a hex string.
        """
        return f"{self.correlation:08x}"

    def __repr__(self) -> str:
        """
        Get the value of the ID as a hex string.
        """
        return f"Correlation(ID={self.__str__()})"


CorrelationId.EMPTY_CORRELATION = CorrelationId.from_string("0")
