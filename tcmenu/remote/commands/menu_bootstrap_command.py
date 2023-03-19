from dataclasses import dataclass
from enum import Enum, auto

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


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
        return f"MenuBootstrapCommand{{" f" bootType={self.boot_type}" f" }}"
