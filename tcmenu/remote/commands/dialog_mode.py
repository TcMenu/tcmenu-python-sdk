from enum import Enum, auto


# noinspection PyArgumentList
class DialogMode(Enum):
    """
    The modes that a dialog can be in, and the transmission type for action too.
    """

    """ The dialog is to be shown. """
    SHOW = auto()

    """ The dialog is to be hidden. """
    HIDE = auto()

    """ Perform the following action on the dialog. """
    ACTION = auto()

    @staticmethod
    def from_string(mode: str) -> "DialogMode":
        if mode == "S":
            return DialogMode.SHOW
        elif mode == "H":
            return DialogMode.HIDE
        else:
            return DialogMode.ACTION
