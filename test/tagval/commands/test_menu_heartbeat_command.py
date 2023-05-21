from tcmenu.tagval.commands.command_factory import CommandFactory
from tcmenu.tagval.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.tagval.protocol.message_field import MessageField


def test_menu_heartbeat_command():
    command = CommandFactory.new_heartbeat_command(frequency=100, mode=MenuHeartbeatCommand.HeartbeatMode.START)
    assert command.heartbeat_interval == 100
    assert command.mode == MenuHeartbeatCommand.HeartbeatMode.START
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "HB"
