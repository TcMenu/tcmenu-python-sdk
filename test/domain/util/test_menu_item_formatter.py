import pytest

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import AnalogMenuItem, Rgb32MenuItem
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.util.menu_item_formatter import MenuItemFormatter
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from test.domain.domain_fixtures import DomainFixtures


def test_format_for_wire():
    tree: MenuTree = DomainFixtures.full_esp_amplifier_test_tree()

    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(1), "-39.5dB") == "-39.5dB"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(2), "3") == "3-3"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(2), "abc") == "0-abc"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(3), "ON") == "1"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(3), "yes") == "1"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(3), "false") == "0"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(4), "asdf") == "0"

    with pytest.raises(ValueError):
        MenuItemFormatter.format_to_wire(tree.get_menu_by_id(5), "")

    with pytest.raises(ValueError):
        MenuItemFormatter.format_to_wire(tree.get_menu_by_id(24), "")

    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(22), "text") == "text"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(22), "text_longer_than_defined_length") == ""
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.IP_ADDRESS),
            "192.168.1.10",
        )
        == "192.168.1.10"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.IP_ADDRESS),
            "192x168x1x10",
        )
        == "0.0.0.0"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.TIME_12H), "12:34:56"
        )
        == "12:34:56"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.TIME_24H),
            "12:34:56.123",
        )
        == "12:34:56.123"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.TIME_24_HUNDREDS),
            "12:34 56",
        )
        == "12:00:00"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.GREGORIAN_DATE),
            "01/08/2023",
        )
        == "01/08/2023"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.GREGORIAN_DATE),
            "01/08 2023",
        )
        == "01/01/2000"
    )
    assert (
        MenuItemFormatter.format_to_wire(
            MenuItemHelper.create_from_existing(tree.get_menu_by_id(22), item_type=EditItemType.TIME_24H_HHMM),
            "12:34:56.123",
        )
        == ""
    )

    assert MenuItemFormatter.format_to_wire(Rgb32MenuItem(name="RGB"), "#ababab") == "#ABABABFF"
    assert MenuItemFormatter.format_to_wire(Rgb32MenuItem(name="RGB"), "test") == "#000000FF"
    assert MenuItemFormatter.format_to_wire(DomainFixtures.a_large_number("large_num", 210, 5, False), "1000") == "1000"
    assert MenuItemFormatter.format_to_wire(DomainFixtures.a_large_number("large_num", 210, 5, False), "a1000") == "0"
    assert MenuItemFormatter.format_to_wire(tree.get_menu_by_id(14), "abc") == "abc"


def test_format_for_display():
    tree: MenuTree = DomainFixtures.full_esp_amplifier_test_tree()

    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(1), 101) == "-39.5dB"
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(2), CurrentScrollPosition(1, "hello")) == "hello"
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(3), True) == "True"
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(4), False) == "Off"
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(5), False) == ""
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(24), False) == ""
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(22), "text") == "text"
    assert MenuItemFormatter.format_for_display(tree.get_menu_by_id(14), 1) == "Warm Valves"


def test_integer_percentage_case():
    item: AnalogMenuItem = AnalogMenuItem(
        divisor=1, offset=0, max_value=100, unit_name="%", name="hello", eeprom_address=-1
    )

    assert MenuItemFormatter.format_for_display(item, 0) == "0%"
    assert MenuItemFormatter.format_for_display(item, 100) == "100%"
