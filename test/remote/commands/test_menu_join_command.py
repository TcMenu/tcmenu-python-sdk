import uuid

from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_join_command_random_uuid():
    command = CommandFactory.new_join_command(name="Android Phone")
    assert isinstance(command.app_uuid, uuid.UUID)
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "NJ"

    assert command.my_name == "Android Phone"
    assert type(command.api_version) == int
    assert command.platform == ApiPlatform.PYTHON_API


def test_menu_join_command_fixed_uuid():
    phone_uuid = uuid.uuid4()
    command = CommandFactory.new_join_command(name="Android Phone", uuid=phone_uuid)
    assert isinstance(command.app_uuid, uuid.UUID)
    assert command.app_uuid == phone_uuid
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "NJ"

    assert command.my_name == "Android Phone"
    assert type(command.api_version) == int
    assert command.platform == ApiPlatform.PYTHON_API
