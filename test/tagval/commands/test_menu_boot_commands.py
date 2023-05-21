from tcmenu.domain.menu_items import BooleanMenuItem, ScrollChoiceMenuItem, Rgb32MenuItem
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.menu_state import MenuState
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.tagval.commands.command_factory import CommandFactory
from tcmenu.tagval.protocol.message_field import MessageField
from test.domain.domain_fixtures import DomainFixtures


def test_new_menu_state_with_no_previous_state():
    item = DomainFixtures.an_analog_item("Volume", 10)
    command = CommandFactory.new_analog_boot_command(parent_id=0, item=item, current_value=100)

    menu_state = command.new_menu_state()
    assert menu_state.item == item
    assert menu_state.value == 100
    assert menu_state.changed is False
    assert menu_state.active is False


def test_new_menu_state_with_old_state_matching_current_one():
    item = DomainFixtures.an_analog_item("Volume", 10)
    old_state = MenuItemHelper.state_for_menu_item(item, 100, changed=False, active=True)
    command = CommandFactory.new_analog_boot_command(parent_id=0, item=item, current_value=100)
    menu_state = command.new_menu_state(old_state=old_state)

    assert menu_state.item == item
    assert menu_state.value == 100
    assert menu_state.changed is False
    assert menu_state.active is True


def test_new_menu_state_with_state_changed():
    item = DomainFixtures.an_analog_item("Volume", 10)
    old_state = MenuItemHelper.state_for_menu_item(item, 100, changed=False, active=False)
    command = CommandFactory.new_analog_boot_command(parent_id=0, item=item, current_value=200)
    menu_state = command.new_menu_state(old_state=old_state)

    assert menu_state.item == item
    assert menu_state.value == 200
    assert menu_state.changed is True
    assert menu_state.active is False


def test_new_menu_state_for_submenu_cannot_be_changed():
    item = DomainFixtures.a_sub_menu("SubMenu", 10)
    old_state = MenuItemHelper.state_for_menu_item(item, True, changed=True, active=True)
    command = CommandFactory.new_sub_menu_boot_command(parent_id=0, item=item)
    menu_state = command.new_menu_state(old_state=old_state)

    assert menu_state.item == item
    assert menu_state.value is False
    assert menu_state.changed is False
    assert menu_state.active is True


def test_new_action_boot_command():
    item = DomainFixtures.an_action_menu("Switch fan", 1)
    command = CommandFactory.new_menu_action_boot_command(parent_id=5, item=item)

    assert command.menu_item == item
    assert command.current_value is False
    assert command.sub_menu_id == 5
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BC"


def test_new_analog_boot_command():
    item = DomainFixtures.an_analog_item("Volume", 10)
    command = CommandFactory.new_analog_boot_command(parent_id=0, item=item, current_value=100)

    assert command.menu_item == item
    assert command.current_value == 100
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BA"


def test_new_enum_boot_command():
    item = DomainFixtures.an_enum_item("Time format", 10, ("12-hour", "24-hour"))
    command = CommandFactory.new_menu_enum_boot_command(parent_id=0, item=item, current_value=1)

    assert command.menu_item == item
    assert command.current_value == 1
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BE"


def test_new_boolean_boot_command():
    item = DomainFixtures.a_boolean_menu("Show time", 10, BooleanMenuItem.BooleanNaming.YES_NO)
    command = CommandFactory.new_menu_boolean_boot_command(parent_id=0, item=item, current_value=True)

    assert command.menu_item == item
    assert command.current_value is True
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BB"


def test_new_float_boot_command():
    item = DomainFixtures.a_float_menu("Humidity", 10)
    command = CommandFactory.new_menu_float_boot_command(parent_id=0, item=item, current_value=11.0)

    assert command.menu_item == item
    assert command.current_value == 11.0
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BF"


def test_new_scroll_choice_boot_command():
    item = ScrollChoiceMenuItem()
    command = CommandFactory.new_menu_scroll_choice_boot_command(
        parent_id=0, item=item, current_value=CurrentScrollPosition(0, "")
    )

    assert command.menu_item == item
    assert isinstance(command.current_value, CurrentScrollPosition)
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BZ"


def test_new_rgb32_boot_command():
    item = Rgb32MenuItem()
    command = CommandFactory.new_menu_rgb32_boot_command(parent_id=0, item=item, current_value=PortableColor(0, 0, 0))

    assert command.menu_item == item
    assert isinstance(command.current_value, PortableColor)
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BK"


def test_new_large_num_boot_command():
    item = DomainFixtures.a_large_number("large_num", 210, 5, False)
    command = CommandFactory.new_menu_large_item_boot_command(parent_id=0, item=item, current_value=1000)

    assert command.menu_item == item
    assert command.current_value == 1000
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BN"


def test_new_text_boot_command():
    item = DomainFixtures.a_text_menu("Main menu", 10)
    command = CommandFactory.new_menu_text_boot_command(parent_id=0, item=item, current_value="Main menu")

    assert command.menu_item == item
    assert command.current_value == "Main menu"
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BT"


def test_new_runtime_list_boot_command():
    item = DomainFixtures.a_runtime_list_menu(name="2002", item_id=20002, rows=3)
    command = CommandFactory.new_runtime_list_boot_command(parent_id=0, item=item, current_value=("Item1", "Item2"))

    assert command.menu_item == item
    assert command.current_value == ("Item1", "Item2")
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BL"


def test_new_sub_menu_boot_command():
    item = DomainFixtures.a_sub_menu(name="2002", item_id=20002)
    command = CommandFactory.new_sub_menu_boot_command(parent_id=0, item=item)

    assert command.menu_item == item
    assert command.current_value is False
    assert command.sub_menu_id == 0
    assert isinstance(command.command_type(), MessageField) is True
    assert command.command_type().id == "BM"
