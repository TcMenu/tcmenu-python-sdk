from dataclasses import dataclass
from enum import Enum
from typing import Union

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


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
        return MenuChangeCommand.ChangeType.ABSOLUTE_LIST if type(self.value) == tuple else self.change_type

    def command_type(self) -> MessageField:
        return MenuCommandType.CHANGE_INT_FIELD.message_field

    def __repr__(self):
        return (
            f"MenuChangeCommand{{"
            f" menu_item_id={self.menu_item_id},"
            f" correlation={self.correlation_id},"
            f" change_type={self.change_type},"
            f" value={self.value}"
            f" }}"
        )
