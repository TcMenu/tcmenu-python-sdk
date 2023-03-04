import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Union
from uuid import UUID

from tcmenu.domain.menu_items import MenuItem
from tcmenu.domain.state.menu_state import MenuState
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.remote.commands.ack_status import AckStatus
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


class MenuCommand(ABC):
    """
    Classes extending from MenuCommand can be sent and received on a connector. They are protocol
    neutral in order to make replacing the protocol as easy as possible.
    """

    @property
    @abstractmethod
    def command_type(self) -> MessageField:
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

    def __repr__(self):
        return f"BootItemMenuCommand[{self.command_type}] {{" \
               f" menu_item={self.menu_item}," \
               f" current_value={self.current_value}," \
               f" sub_menu_id={self.sub_menu_id}" \
               f" }}"

    def new_menu_state(self, old_state: Optional[MenuState] = None) -> MenuState:
        changed = (old_state and old_state.value != self.current_value)
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


@dataclass(frozen=True)
class MenuAcknowledgementCommand(MenuCommand):
    correlation_id: CorrelationId

    ack_status: AckStatus

    def command_type(self) -> MessageField:
        return MenuCommandType.ACKNOWLEDGEMENT.message_field

    def __repr__(self):
        return f"MenuAcknowledgementCommand{{" \
               f" correlation_id={self.correlation_id}," \
               f" ack_status={self.ack_status}" \
               f" }}"


@dataclass(frozen=True)
class MenuBootstrapCommand(MenuCommand):
    # noinspection PyArgumentList
    class BootType(Enum):
        START = auto()
        END = auto()

    boot_type: BootType

    def command_type(self) -> MessageField:
        return MenuCommandType.BOOTSTRAP.message_field

    def __repr__(self):
        return f"MenuBootstrapCommand{{" \
               f" bootType={self.boot_type}" \
               f" }}"


@dataclass(frozen=True)
class MenuChangeCommand(MenuCommand):
    class ChangeType(Enum):
        DELTA = 0
        ABSOLUTE = 1
        ABSOLUTE_LIST = 2
        LIST_STATE_CHANGE = 3

    menu_item_id: int

    correlation_id: CorrelationId

    value: Union[str, tuple[str]]

    change_type: ChangeType

    @property
    def change_type(self):
        return MenuChangeCommand.ChangeType.ABSOLUTE_LIST\
            if type(self.value) == tuple else self.change_type

    def command_type(self) -> MessageField:
        return MenuCommandType.CHANGE_INT_FIELD.message_field

    def __repr__(self):
        return f"MenuChangeCommand{{" \
               f" menu_item_id={self.menu_item_id}," \
               f" correlation={self.correlation_id}," \
               f" change_type={self.change_type},"\
               f" value={self.value}" \
               f" }}"


@dataclass(frozen=True)
class MenuDialogCommand(MenuCommand):
    dialog_mode: DialogMode

    header: str

    buffer: str

    button1: MenuButtonType

    button2: MenuButtonType

    correlation_id: CorrelationId

    def command_type(self) -> MessageField:
        return MenuCommandType.DIALOG_UPDATE.message_field

    def __repr__(self):
        return f"MenuDialogCommand{{" \
               f" dialog_mode={self.dialog_mode}," \
               f" header={self.header},"\
               f" buffer={self.buffer}," \
               f" button1={self.button1}," \
               f" button2={self.button2}," \
               f" correlation={self.correlation_id}" \
               f" }}"


@dataclass(frozen=True)
class MenuHeartbeatCommand(MenuCommand):
    # noinspection PyArgumentList
    class HeartbeatMode(Enum):
        START = auto()
        NORMAL = auto()
        END = auto()

    heartbeat_interval: int

    mode: HeartbeatMode

    def command_type(self) -> MessageField:
        return MenuCommandType.HEARTBEAT.message_field

    def __repr__(self):
        return "MenuHeartbeatCommand{}"


@dataclass(frozen=True)
class MenuJoinCommand(MenuCommand):
    my_name: str

    api_version: int

    platform: ApiPlatform

    app_uuid: UUID = uuid.uuid4()

    def command_type(self) -> MessageField:
        return MenuCommandType.JOIN.message_field

    def __repr__(self):
        return f"MenuJoinCommand{{" \
               f" my_name={self.my_name}," \
               f" api_ver={self.api_version},"\
               f" platform={self.platform}," \
               f" uuid={self.app_uuid}" \
               f" }}"


@dataclass(frozen=True)
class MenuPairingCommand(MenuCommand):
    name: str

    uuid: UUID

    def command_type(self) -> MessageField:
        return MenuCommandType.PAIRING_REQUEST.message_field

    def __repr__(self):
        return f"MenuPairingCommand{{" \
               f" name={self.name}," \
               f" uuid={self.uuid}" \
               f" }}"
