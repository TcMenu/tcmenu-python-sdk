import uuid

from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_pairing_command():
    phone_name = "Android Phone"
    phone_uuid = uuid.uuid4()

    command = CommandFactory.new_pairing_command(name=phone_name, uuid=phone_uuid)
    assert command.name == phone_name
    assert command.uuid == phone_uuid
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "PR"
