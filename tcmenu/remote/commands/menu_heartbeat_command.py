from dataclasses import dataclass
from enum import Enum, auto

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class MenuHeartbeatCommand(MenuCommand):
    # noinspection PyArgumentList
    class HeartbeatMode(Enum):
        START = auto()
        NORMAL = auto()
        END = auto()

    heartbeat_interval: int

    mode: HeartbeatMode

    @property
    def command_type(self) -> MessageField:
        return MenuCommandType.HEARTBEAT.message_field

    def __repr__(self):
        return "MenuHeartbeatCommand{}"
