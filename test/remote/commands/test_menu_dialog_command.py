from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


def test_menu_dialog_command():
    header = "Info"
    message = "This is a informational message."
    command = CommandFactory.new_dialog_command(
        mode=DialogMode.SHOW,
        header=header,
        message=message,
        button1=MenuButtonType.OK,
        button2=MenuButtonType.NONE,
        correlation_id=CorrelationId.new_correlation(),
    )

    assert command.dialog_mode == DialogMode.SHOW
    assert command.header == header
    assert command.buffer == message
    assert command.button1 == MenuButtonType.OK
    assert command.button2 == MenuButtonType.NONE
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "DM"
