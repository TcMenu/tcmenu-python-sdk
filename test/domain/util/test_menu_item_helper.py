from typing import Any, Optional
from unittest import TestCase

from tcmenu.domain.menu_items import (
    BooleanMenuItem,
    Rgb32MenuItem,
    ScrollChoiceMenuItem,
    RuntimeListMenuItem,
    AnalogMenuItem,
    EnumMenuItem,
    SubMenuItem,
    FloatMenuItem,
    ActionMenuItem,
    EditableTextMenuItem,
    MenuItem,
)
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.menu_state import MenuState
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.tagval.commands.menu_boot_commands import (
    MenuAnalogBootCommand,
    MenuEnumBootCommand,
    MenuBooleanBootCommand,
    MenuFloatBootCommand,
    MenuScrollChoiceBootCommand,
    MenuRgb32BootCommand,
    MenuLargeNumBootCommand,
    MenuTextBootCommand,
    MenuRuntimeListBootCommand,
    MenuSubBootCommand,
    MenuActionBootCommand,
)
from test.domain.domain_fixtures import DomainFixtures

analog_item = DomainFixtures.an_analog_item(name="123", item_id=4)
enum_item = DomainFixtures.an_enum_item(name="111", item_id=3)
sub_item = DomainFixtures.a_sub_menu(name="321", item_id=3)
bool_item = DomainFixtures.a_boolean_menu(name="321", item_id=33, naming=BooleanMenuItem.BooleanNaming.TRUE_FALSE)
list_item = DomainFixtures.a_runtime_list_menu(name="2002", item_id=20002, rows=3)
text_item = DomainFixtures.a_text_menu(name="2222", item_id=33)
ip_item = DomainFixtures.an_ip_address_menu(name="127.0.0.1", item_id=99)
float_item = DomainFixtures.a_float_menu(name="fkgo", item_id=223)
action_item = DomainFixtures.an_action_menu(name="act", item_id=333)
large_num = DomainFixtures.a_large_number(name="lgeNum", item_id=293, dp=4, negative=True)
rgb_item = Rgb32MenuItem(id=10, name="rgb", include_alpha_channel=True)
scroll_item = ScrollChoiceMenuItem(
    id=15,
    name="scroll",
    item_width=10,
    num_entries=20,
    eeprom_offset=10,
    choice_mode=ScrollChoiceMenuItem.ScrollChoiceMode.ARRAY_IN_RAM,
)

tree = MenuTree()
tree.add_menu_item(analog_item, MenuTree.ROOT)
tree.add_menu_item(enum_item, MenuTree.ROOT)
tree.add_menu_item(sub_item, MenuTree.ROOT)
tree.add_menu_item(bool_item, sub_item)
tree.add_menu_item(list_item, sub_item)
tree.add_menu_item(text_item, sub_item)
tree.add_menu_item(ip_item, sub_item)
tree.add_menu_item(float_item, sub_item)
tree.add_menu_item(action_item, sub_item)
tree.add_menu_item(large_num, sub_item)
tree.add_menu_item(rgb_item, sub_item)
tree.add_menu_item(scroll_item, sub_item)


def test_sub_menu_helper():
    assert sub_item == MenuItemHelper.as_sub_menu(sub_item)


def test_is_runtime_item():
    assert MenuItemHelper.is_runtime_structure_needed(text_item)
    assert MenuItemHelper.is_runtime_structure_needed(ip_item)
    assert not MenuItemHelper.is_runtime_structure_needed(float_item)
    assert not MenuItemHelper.is_runtime_structure_needed(bool_item)
    assert MenuItemHelper.is_runtime_structure_needed(sub_item)
    assert MenuItemHelper.is_runtime_structure_needed(rgb_item)
    assert MenuItemHelper.is_runtime_structure_needed(scroll_item)


def test_create_from_existing():
    new_analog = MenuItemHelper.create_from_existing_with_id(analog_item, new_id=11)
    new_enum = MenuItemHelper.create_from_existing_with_id(enum_item, new_id=94)
    new_sub = MenuItemHelper.create_from_existing_with_id(sub_item, new_id=97)
    new_bool = MenuItemHelper.create_from_existing_with_id(bool_item, new_id=99)
    new_float = MenuItemHelper.create_from_existing_with_id(float_item, new_id=3333)
    new_text = MenuItemHelper.create_from_existing_with_id(text_item, new_id=1111)
    new_action = MenuItemHelper.create_from_existing_with_id(action_item, new_id=9999)
    new_list = MenuItemHelper.create_from_existing_with_id(list_item, new_id=20093)
    new_rgb = MenuItemHelper.create_from_existing_with_id(rgb_item, new_id=20095)
    new_scroll = MenuItemHelper.create_from_existing_with_id(scroll_item, new_id=20096)

    assert isinstance(new_list, RuntimeListMenuItem)
    assert new_list.id == 20093

    assert isinstance(new_analog, AnalogMenuItem)
    assert new_analog.id == 11

    assert isinstance(new_enum, EnumMenuItem)
    assert new_enum.id == 94

    assert isinstance(new_sub, SubMenuItem)
    assert new_sub.id == 97

    assert isinstance(new_bool, BooleanMenuItem)
    assert new_bool.id == 99

    assert isinstance(new_float, FloatMenuItem)
    assert new_float.id == 3333

    assert isinstance(new_action, ActionMenuItem)
    assert new_action.id == 9999

    assert isinstance(new_text, EditableTextMenuItem)
    assert new_text.id == 1111

    assert isinstance(new_scroll, ScrollChoiceMenuItem)
    assert new_scroll.id == 20096

    assert isinstance(new_rgb, Rgb32MenuItem)
    assert new_rgb.id == 20095


def test_eeprom_size_for_item():
    assert MenuItemHelper.eeprom_size_for_item(list_item) == 0
    assert MenuItemHelper.eeprom_size_for_item(analog_item) == 2
    assert MenuItemHelper.eeprom_size_for_item(enum_item) == 2
    assert MenuItemHelper.eeprom_size_for_item(sub_item) == 0
    assert MenuItemHelper.eeprom_size_for_item(bool_item) == 1
    assert MenuItemHelper.eeprom_size_for_item(text_item) == 10
    assert MenuItemHelper.eeprom_size_for_item(ip_item) == 4
    assert MenuItemHelper.eeprom_size_for_item(float_item) == 0
    assert MenuItemHelper.eeprom_size_for_item(action_item) == 0
    assert MenuItemHelper.eeprom_size_for_item(rgb_item) == 4
    assert MenuItemHelper.eeprom_size_for_item(scroll_item) == 2


def test_create_state_function():
    check_state(analog_item, MenuState.StateStorageType.INTEGER, 10, True, False)
    check_state(analog_item, MenuState.StateStorageType.INTEGER, 102.2, True, True, 102)
    check_state(analog_item, MenuState.StateStorageType.INTEGER, "1033", False, True, 255)  # above maximum
    check_state(analog_item, MenuState.StateStorageType.INTEGER, -200, False, True, 0)  # below min
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, "true", False, True, True)
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, "0", False, False, False)
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, "1", False, False, True)
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, 1, False, True, True)
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, 0, True, False, False)
    check_state(bool_item, MenuState.StateStorageType.BOOLEAN, "Y", False, False, True)
    check_state(float_item, MenuState.StateStorageType.FLOAT, "100.4", False, True, 100.4)
    check_state(float_item, MenuState.StateStorageType.FLOAT, 10034.3, False, False, 10034.3)
    check_state(enum_item, MenuState.StateStorageType.INTEGER, 4, False, True, 1)  # exceeds max
    check_state(enum_item, MenuState.StateStorageType.INTEGER, "1", True, False, 1)
    check_state(enum_item, MenuState.StateStorageType.INTEGER, "-221", True, False, 0)  # below min
    check_state(text_item, MenuState.StateStorageType.STRING, "12345", True, True)
    check_state(large_num, MenuState.StateStorageType.BIG_DECIMAL, "12345.432", True, True, 12345.432)
    check_state(large_num, MenuState.StateStorageType.BIG_DECIMAL, 12345.432, True, False)
    check_state(list_item, MenuState.StateStorageType.STRING_LIST, [1, 2], True, False, ["1", "2"])
    check_state(list_item, MenuState.StateStorageType.STRING_LIST, ["3", "4"], True, False)
    check_state(scroll_item, MenuState.StateStorageType.SCROLL_POSITION, 1, True, False, CurrentScrollPosition(1, ""))
    check_state(
        scroll_item,
        MenuState.StateStorageType.SCROLL_POSITION,
        "1-My Sel",
        True,
        False,
        CurrentScrollPosition(1, "My Sel"),
    )
    check_state(
        scroll_item, MenuState.StateStorageType.SCROLL_POSITION, CurrentScrollPosition(1, "Sel 123"), True, False
    )
    check_state(
        scroll_item,
        MenuState.StateStorageType.SCROLL_POSITION,
        "99-My Sel",
        True,
        False,
        CurrentScrollPosition(0, "No entries"),
    )
    check_state(
        rgb_item, MenuState.StateStorageType.PORTABLE_COLOR, "#ff00aa", True, False, PortableColor.from_html("#ff00aa")
    )
    check_state(rgb_item, MenuState.StateStorageType.PORTABLE_COLOR, PortableColor.from_html("#000000"), True, False)
    check_state(sub_item, MenuState.StateStorageType.BOOLEAN, False, True, False)
    check_state(MenuItem(), MenuState.StateStorageType.BOOLEAN, False, True, False)
    check_state(None, MenuState.StateStorageType.BOOLEAN, False, False, False)
    check_state(text_item, MenuState.StateStorageType.STRING, None, True, True, "")


def test_get_boot_message_for_item():
    tree._menu_states = {}
    check_get_boot_item_menu_command(action_item, False, MenuActionBootCommand)
    check_get_boot_item_menu_command(analog_item, 10, MenuAnalogBootCommand)
    check_get_boot_item_menu_command(enum_item, 1, MenuEnumBootCommand)
    check_get_boot_item_menu_command(bool_item, True, MenuBooleanBootCommand)
    check_get_boot_item_menu_command(float_item, 133.23, MenuFloatBootCommand)
    check_get_boot_item_menu_command(scroll_item, CurrentScrollPosition.from_text("11"), MenuScrollChoiceBootCommand)
    check_get_boot_item_menu_command(rgb_item, PortableColor.from_html("#aabbcc"), MenuRgb32BootCommand)
    check_get_boot_item_menu_command(large_num, 10, MenuLargeNumBootCommand)
    check_get_boot_item_menu_command(text_item, "text", MenuTextBootCommand)
    check_get_boot_item_menu_command(list_item, ["hello"], MenuRuntimeListBootCommand)
    check_get_boot_item_menu_command(sub_item, False, MenuSubBootCommand)


def test_setting_delta_state_enum():
    tree._menu_states = {}
    MenuItemHelper.set_menu_state(enum_item, 1, tree)
    assert MenuItemHelper.get_value_for(enum_item, tree, -1)
    MenuItemHelper.apply_incremental_value_change(enum_item, -1, tree)
    assert MenuItemHelper.get_value_for(enum_item, tree, -1) == 0
    # Can't go past 0.
    MenuItemHelper.apply_incremental_value_change(enum_item, -1, tree)
    assert MenuItemHelper.get_value_for(enum_item, tree, -1) == 0


def test_setting_delta_state_position():
    tree._menu_states = {}
    MenuItemHelper.set_menu_state(scroll_item, 1, tree)
    assert MenuItemHelper.get_value_for(scroll_item, tree, CurrentScrollPosition.from_text("0-")).position == 1
    MenuItemHelper.apply_incremental_value_change(scroll_item, 1, tree)
    assert MenuItemHelper.get_value_for(scroll_item, tree, CurrentScrollPosition.from_text("0-")).position == 2


def test_get_value_for():
    tree._menu_states = {}
    assert MenuItemHelper.get_value_for(analog_item, tree, -1) == -1
    MenuItemHelper.set_menu_state(analog_item, 22, tree)
    assert MenuItemHelper.get_value_for(analog_item, tree, -1) == 22


def test_get_default_from():
    assert MenuItemHelper.get_default_for(analog_item) == 0
    assert MenuItemHelper.get_default_for(float_item) == float(0)
    assert not MenuItemHelper.get_default_for(bool_item)
    assert not MenuItemHelper.get_default_for(sub_item)
    assert MenuItemHelper.get_default_for(large_num) == 0
    assert MenuItemHelper.get_default_for(text_item) == ""
    assert MenuItemHelper.get_default_for(rgb_item) == PortableColor(red=0, green=0, blue=0)
    assert MenuItemHelper.get_default_for(list_item) == []
    assert MenuItemHelper.get_default_for(scroll_item) == CurrentScrollPosition(position=0, value="")
    assert not MenuItemHelper.get_default_for(MenuItem())


def check_get_boot_item_menu_command(item: MenuItem, value: Any, cmd_class: Any):
    MenuItemHelper.set_menu_state(item, value, tree)
    boot_cmd = MenuItemHelper.get_boot_msg_for_item(item, MenuTree.ROOT, tree)
    assert isinstance(boot_cmd, cmd_class)
    assert boot_cmd.current_value == value


def check_state(
    item: Optional[MenuItem],
    storage_type: MenuState.StateStorageType,
    value: Any,
    changed: bool,
    active: bool,
    actual: Optional[Any] = None,
):
    if actual is None:
        actual = value

    state = MenuItemHelper.state_for_menu_item(item, value, changed, active)
    assert state.storage_type == storage_type
    assert state.changed == changed
    assert state.active == active

    if type(active) == float:
        TestCase().assertAlmostEqual(float(state.value), float(actual), delta=0.00001)
    else:
        assert state.value == actual
