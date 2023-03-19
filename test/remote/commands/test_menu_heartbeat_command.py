from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_heartbeat_command():
    command = CommandFactory.new_heartbeat_command(frequency=100, mode=MenuHeartbeatCommand.HeartbeatMode.START)
    assert command.heartbeat_interval == 100
    assert command.mode == MenuHeartbeatCommand.HeartbeatMode.START
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "HB"
