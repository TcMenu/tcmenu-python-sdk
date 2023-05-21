from tcmenu.tagval.commands.command_factory import CommandFactory
from tcmenu.tagval.commands.menu_bootstrap_command import MenuBootstrapCommand
from tcmenu.tagval.protocol.message_field import MessageField


def test_menu_bootstrap_command():
    command = CommandFactory.new_bootstrap_command(boot_type=MenuBootstrapCommand.BootType.START)
    assert command.boot_type == MenuBootstrapCommand.BootType.START
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BS"
