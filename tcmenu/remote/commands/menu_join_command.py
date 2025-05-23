import uuid
from dataclasses import dataclass

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class MenuJoinCommand(MenuCommand):
    my_name: str

    api_version: int

    platform: ApiPlatform

    app_uuid: uuid.UUID = uuid.uuid4()

    serial_number: str = "999999999"

    @property
    def command_type(self) -> MessageField:
        return MenuCommandType.JOIN.message_field

    def __repr__(self):
        return (
            f"MenuJoinCommand{{"
            f" my_name={self.my_name},"
            f" api_ver={self.api_version},"
            f" platform={self.platform},"
            f" uuid={self.app_uuid}"
            f" (S/N={self.serial_number})"
            f" }}"
        )
