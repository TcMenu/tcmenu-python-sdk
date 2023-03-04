from collections import namedtuple
from enum import Enum


class MenuButtonType(Enum):
    """
    The button type for a dialog. Dialogs generally have up to two buttons by default,
    each button can be one of the following types.
    """
    Button = namedtuple('MenuButtonType', ['type_value', 'button_name'])

    """ The OK button. """
    OK = Button(0, "OK")

    """ The accept button. """
    ACCEPT = Button(1, "Accept")

    """ The cancel button. """
    CANCEL = Button(2, "Cancel")

    """ The close button. """
    CLOSE = Button(3, "Close")

    """ No button. """
    NONE = Button(4, "")

    @property
    def button_name(self) -> str:
        return self._value_.button_name

    @property
    def type_value(self) -> int:
        return self._value_.type_value
