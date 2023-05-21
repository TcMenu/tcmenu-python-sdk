from dataclasses import dataclass

from tcmenu.tagval.commands.dialog_mode import DialogMode
from tcmenu.tagval.commands.menu_button_type import MenuButtonType
from tcmenu.tagval.commands.menu_command import MenuCommand
from tcmenu.tagval.commands.menu_command_type import MenuCommandType
from tcmenu.tagval.protocol.correlation_id import CorrelationId
from tcmenu.tagval.protocol.message_field import MessageField


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
        return (
            f"MenuDialogCommand{{"
            f" dialog_mode={self.dialog_mode},"
            f" header={self.header},"
            f" buffer={self.buffer},"
            f" button1={self.button1},"
            f" button2={self.button2},"
            f" correlation={self.correlation_id}"
            f" }}"
        )
