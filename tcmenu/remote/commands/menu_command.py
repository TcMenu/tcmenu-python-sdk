from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from tcmenu.domain.menu_items import MenuItem
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


class MenuCommand(ABC):
    """
    Classes extending from MenuCommand can be sent and received on a connector. They are protocol
    neutral in order to make replacing the protocol as easy as possible.
    """

    @abstractmethod
    def get_command_type(self) -> MessageField:
        """
        The type of message received.
        :return: the command type
        """
        pass


@dataclass(frozen=True)
class BootItemMenuCommand(MenuCommand, ABC):
    menu_item: MenuItem

    current_value: Any

    sub_menu_id: int


@dataclass(frozen=True)
class MenuActionBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.ACTION_BOOT_ITEM


@dataclass(frozen=True)
class MenuAnalogBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.ANALOG_BOOT_ITEM


@dataclass(frozen=True)
class MenuEnumBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.ENUM_BOOT_ITEM


@dataclass(frozen=True)
class MenuBooleanBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.BOOLEAN_BOOT_ITEM


@dataclass(frozen=True)
class MenuFloatBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.FLOAT_BOOT_ITEM


@dataclass(frozen=True)
class MenuScrollChoiceBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.BOOT_SCROLL_CHOICE


@dataclass(frozen=True)
class MenuRgb32BootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.BOOT_RGB_COLOR


@dataclass(frozen=True)
class MenuLargeNumBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.LARGE_NUM_BOOT_ITEM


@dataclass(frozen=True)
class MenuTextBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.TEXT_BOOT_ITEM


@dataclass(frozen=True)
class MenuRuntimeListBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.RUNTIME_LIST_BOOT


@dataclass(frozen=True)
class MenuSubBootCommand(BootItemMenuCommand):
    def get_command_type(self) -> MessageField:
        return MenuCommandType.SUBMENU_BOOT_ITEM
