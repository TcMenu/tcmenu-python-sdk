from tcmenu.domain.menu_items import AnalogMenuItem
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.util.menu_item_formatter import MenuItemFormatter
from test.domain.domain_fixtures import DomainFixtures


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
