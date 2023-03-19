from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_command_type():
    command = MenuCommandType.ENUM_BOOT_ITEM
    assert isinstance(command.message_field, MessageField)
    assert command.message_field.id == "BE"
