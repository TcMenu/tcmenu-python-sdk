from dataclasses import dataclass
from uuid import UUID

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class MenuPairingCommand(MenuCommand):
    name: str

    uuid: UUID

    @property
    def command_type(self) -> MessageField:
        return MenuCommandType.PAIRING_REQUEST.message_field

    def __repr__(self):
        return f"MenuPairingCommand{{" f" name={self.name}," f" uuid={self.uuid}" f" }}"
