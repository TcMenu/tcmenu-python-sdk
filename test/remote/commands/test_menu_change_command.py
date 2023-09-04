from tcmenu.domain.menu_items import ActionMenuItem
from tcmenu.domain.state.list_response import ListResponse
from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.menu_change_command import MenuChangeCommand
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField


def test_new_delta_menu_change_command():
    command = CommandFactory.new_delta_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=5, value=10
    )
    assert command.change_type == MenuChangeCommand.ChangeType.DELTA
    assert command.menu_item_id == 5
    assert command.value == "10"
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"

    command = CommandFactory.new_delta_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=ActionMenuItem(id=8), value=11
    )
    assert command.change_type == MenuChangeCommand.ChangeType.DELTA
    assert command.menu_item_id == 8
    assert command.value == "11"
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"


def test_new_absolute_menu_change_command():
    command = CommandFactory.new_absolute_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=15, value=110
    )
    assert command.change_type == MenuChangeCommand.ChangeType.ABSOLUTE
    assert command.menu_item_id == 15
    assert command.value == "110"
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"

    command = CommandFactory.new_absolute_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=ActionMenuItem(id=80), value=-5
    )
    assert command.change_type == MenuChangeCommand.ChangeType.ABSOLUTE
    assert command.menu_item_id == 80
    assert command.value == "-5"
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"


def test_new_list_response_menu_change_command():
    command = CommandFactory.new_list_response_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=22, value=ListResponse.from_string("220:1")
    )
    assert command.change_type == MenuChangeCommand.ChangeType.LIST_STATE_CHANGE
    assert command.menu_item_id == 22
    assert isinstance(command.value, str)
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"

    command = CommandFactory.new_list_response_menu_change_command(
        correlation_id=CorrelationId.new_correlation(),
        item=ActionMenuItem(id=85),
        value=ListResponse.from_string("230:1"),
    )
    assert command.change_type == MenuChangeCommand.ChangeType.LIST_STATE_CHANGE
    assert command.menu_item_id == 85
    assert isinstance(command.value, str)
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"


def test_new_absolute_list_menu_change_command():
    command = CommandFactory.new_absolute_list_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=22, values=("3", "5", "7", "10")
    )
    assert command.change_type == MenuChangeCommand.ChangeType.ABSOLUTE_LIST
    assert command.menu_item_id == 22
    assert isinstance(command.value, tuple)
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"

    command = CommandFactory.new_absolute_list_menu_change_command(
        correlation_id=CorrelationId.new_correlation(), item=ActionMenuItem(id=55), values=("3", "5", "7", "10")
    )
    assert command.change_type == MenuChangeCommand.ChangeType.ABSOLUTE_LIST
    assert command.menu_item_id == 55
    assert isinstance(command.value, tuple)
    assert isinstance(command.command_type, MessageField) is True
    assert command.command_type.id == "VC"


def test_change_type_from_id():
    assert MenuChangeCommand.ChangeType.from_id(0) == MenuChangeCommand.ChangeType.DELTA
    assert MenuChangeCommand.ChangeType.from_id(1) == MenuChangeCommand.ChangeType.ABSOLUTE
    assert MenuChangeCommand.ChangeType.from_id(2) == MenuChangeCommand.ChangeType.ABSOLUTE_LIST
    assert MenuChangeCommand.ChangeType.from_id(3) == MenuChangeCommand.ChangeType.LIST_STATE_CHANGE
    assert MenuChangeCommand.ChangeType.from_id(4) == MenuChangeCommand.ChangeType.DELTA
    assert MenuChangeCommand.ChangeType.from_id(1000) == MenuChangeCommand.ChangeType.DELTA
