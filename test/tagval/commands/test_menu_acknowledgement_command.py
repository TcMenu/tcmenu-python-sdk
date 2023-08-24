from tcmenu.tagval.commands.ack_status import AckStatus
from tcmenu.tagval.commands.command_factory import CommandFactory
from tcmenu.tagval.protocol.correlation_id import CorrelationId
from tcmenu.tagval.protocol.message_field import MessageField


def test_menu_acknowledgement_command():
    command = CommandFactory.new_acknowledgement_command(
        correlation_id=CorrelationId.new_correlation(), status=AckStatus.SUCCESS
    )
    assert command.ack_status == AckStatus.SUCCESS
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "AK"
