from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CurrentScrollPosition:
    """
    Represents a scroll position as used by ScrollChoiceMenuItems, it holds the position and the current string value.
    """

    position: int
    value: str

    @staticmethod
    def from_text(text: str) -> CurrentScrollPosition:
        """
        Create from a textual representation in the form, position-value, EG 1-Pizza
        :param: text the text form of the object to parse
        """
        position = None
        value = None

        try:
            split_point = text.index("-")
            value = text[split_point + 1 :]
            position = int(text[:split_point])
        except ValueError:
            if position is None:
                position = 0

            if value is None:
                value = "Unknown"

        return CurrentScrollPosition(position, value)

    def __str__(self) -> str:
        return f"{self.position}-{self.value}"
