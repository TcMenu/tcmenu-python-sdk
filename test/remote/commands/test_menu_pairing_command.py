import uuid

from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_pairing_command():
    phone_name = "Android Phone"
    phone_uuid = uuid.uuid4()

    command = CommandFactory.new_pairing_command(name=phone_name, uuid=phone_uuid)
    assert command.name == phone_name
    assert command.uuid == phone_uuid
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "PR"
