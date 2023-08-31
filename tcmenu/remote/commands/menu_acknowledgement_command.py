from dataclasses import dataclass

from tcmenu.remote.commands.ack_status import AckStatus
from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


@dataclass(frozen=True)
class MenuAcknowledgementCommand(MenuCommand):
    correlation_id: CorrelationId

    ack_status: AckStatus

    @property
    def command_type(self) -> MessageField:
        return MenuCommandType.ACKNOWLEDGEMENT.message_field

    def __repr__(self):
        return (
            f"MenuAcknowledgementCommand{{"
            f" correlation_id={self.correlation_id},"
            f" ack_status={self.ack_status}"
            f" }}"
        )
