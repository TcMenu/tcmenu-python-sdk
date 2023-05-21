from enum import Enum
from tcmenu.tagval.protocol.message_field import MessageField


class MenuCommandType(Enum):
    """
    Here all the inbuilt types of messages that can be sent to and from the server are listed out.
    """

    JOIN = MessageField("N", "J")
    PAIRING_REQUEST = MessageField("P", "R")
    HEARTBEAT = MessageField("H", "B")
    BOOTSTRAP = MessageField("B", "S")
    ANALOG_BOOT_ITEM = MessageField("B", "A")
    ACTION_BOOT_ITEM = MessageField("B", "C")
    SUBMENU_BOOT_ITEM = MessageField("B", "M")
    ENUM_BOOT_ITEM = MessageField("B", "E")
    BOOLEAN_BOOT_ITEM = MessageField("B", "B")
    TEXT_BOOT_ITEM = MessageField("B", "T")
    RUNTIME_LIST_BOOT = MessageField("B", "L")
    BOOT_SCROLL_CHOICE = MessageField("B", "Z")
    BOOT_RGB_COLOR = MessageField("B", "K")
    LARGE_NUM_BOOT_ITEM = MessageField("B", "N")
    FLOAT_BOOT_ITEM = MessageField("B", "F")
    REMOTE_BOOT_ITEM = MessageField("B", "R")
    ACKNOWLEDGEMENT = MessageField("A", "K")
    CHANGE_INT_FIELD = MessageField("V", "C")
    DIALOG_UPDATE = MessageField("D", "M")

    @property
    def message_field(self):
        return self._value_
