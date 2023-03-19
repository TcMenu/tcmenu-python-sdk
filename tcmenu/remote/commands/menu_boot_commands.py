from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional

from tcmenu.domain.menu_items import MenuItem
from tcmenu.domain.state.menu_state import MenuState
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class BootItemMenuCommand(MenuCommand, ABC):
    menu_item: MenuItem

    current_value: Any

    sub_menu_id: int

    def __repr__(self):
        return (
            f"BootItemMenuCommand[{self.command_type}] {{"
            f" menu_item={self.menu_item},"
            f" current_value={self.current_value},"
            f" sub_menu_id={self.sub_menu_id}"
            f" }}"
        )

    def new_menu_state(self, old_state: Optional[MenuState] = None) -> MenuState:
        changed = old_state and old_state.value != self.current_value
        return MenuItemHelper.state_for_menu_item(self.menu_item, self.current_value, changed, old_state.active)


@dataclass(frozen=True)
class MenuActionBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.ACTION_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuAnalogBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.ANALOG_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuEnumBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.ENUM_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuBooleanBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.BOOLEAN_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuFloatBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.FLOAT_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuScrollChoiceBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.BOOT_SCROLL_CHOICE.message_field


@dataclass(frozen=True)
class MenuRgb32BootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.BOOT_RGB_COLOR.message_field


@dataclass(frozen=True)
class MenuLargeNumBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.LARGE_NUM_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuTextBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.TEXT_BOOT_ITEM.message_field


@dataclass(frozen=True)
class MenuRuntimeListBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.RUNTIME_LIST_BOOT.message_field


@dataclass(frozen=True)
class MenuSubBootCommand(BootItemMenuCommand):
    def command_type(self) -> MessageField:
        return MenuCommandType.SUBMENU_BOOT_ITEM.message_field

    def new_menu_state(self, old_state: Optional[MenuState] = None) -> MenuState:
        # SubBootCommand can't be changed.
        return MenuItemHelper.state_for_menu_item(self.menu_item, self.current_value, False, old_state.active)
