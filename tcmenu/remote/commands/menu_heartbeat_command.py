from dataclasses import dataclass
from enum import Enum, auto

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class MenuHeartbeatCommand(MenuCommand):
    # noinspection PyArgumentList
    class HeartbeatMode(Enum):
        NORMAL = 0
        START = 1
        END = 2

    heartbeat_interval: int

    mode: HeartbeatMode

    @property
    def command_type(self) -> MessageField:
        return MenuCommandType.HEARTBEAT.message_field

    @staticmethod
    def from_id(heartbeat_id: int):
        return (
            MenuHeartbeatCommand.HeartbeatMode(heartbeat_id)
            if heartbeat_id in (item.value for item in MenuHeartbeatCommand.HeartbeatMode)
            else MenuHeartbeatCommand.HeartbeatMode.NORMAL
        )

    def __repr__(self):
        return "MenuHeartbeatCommand{}"
