from enum import Enum


# noinspection PyArgumentList
class DialogMode(Enum):
    """
    The modes that a dialog can be in, and the transmission type for action too.
    """

    """ The dialog is to be shown. """
    SHOW = "S"

    """ The dialog is to be hidden. """
    HIDE = "H"

    """ Perform the following action on the dialog. """
    ACTION = "A"

    @staticmethod
    def from_string(mode: str) -> "DialogMode":
        try:
            return DialogMode(mode)
        except ValueError:
            return DialogMode.ACTION
