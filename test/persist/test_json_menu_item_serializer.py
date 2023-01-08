import json

from tcmenu.domain.menu_items import BooleanMenuItem, SubMenuItem
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.persist.json_menu_item_serializer import JsonMenuItemSerializer, PersistedMenuEncoder
from tcmenu.persist.persisted_menu import PersistedMenu
from test.domain.domain_fixtures import DomainFixtures

EXPECTED_JSON: str = (
    "[\n"
    "  {\n"
    + '    "parentId": 0,\n'
    + '    "type": "boolItem",\n'
    + '    "item": {\n'
    + '      "naming": "TRUE_FALSE",\n'
    + '      "name": "abc",\n'
    + '      "id": 1,\n'
    + '      "eepromAddress": 102,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 0,\n'
    + '    "type": "floatItem",\n'
    + '    "item": {\n'
    + '      "numDecimalPlaces": 3,\n'
    + '      "name": "def",\n'
    + '      "id": 2,\n'
    + '      "eepromAddress": 105,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 0,\n'
    + '    "type": "subMenu",\n'
    + '    "item": {\n'
    + '      "secured": false,\n'
    + '      "name": "ghi",\n'
    + '      "id": 3,\n'
    + '      "eepromAddress": 102,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "enumItem",\n'
    + '    "defaultValue": "1",\n'
    + '    "item": {\n'
    + '      "enumEntries": [\n'
    + '        "Item1",\n'
    + '        "Item2"\n'
    + "      ],\n"
    + '      "name": "xyz",\n'
    + '      "id": 4,\n'
    + '      "eepromAddress": 101,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "analogItem",\n'
    + '    "defaultValue": "100",\n'
    + '    "item": {\n'
    + '      "maxValue": 255,\n'
    + '      "offset": 102,\n'
    + '      "divisor": 2,\n'
    + '      "unitName": "dB",\n'
    + '      "step": 1,\n'
    + '      "name": "fhs",\n'
    + '      "id": 5,\n'
    + '      "eepromAddress": 104,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "actionMenu",\n'
    + '    "item": {\n'
    + '      "name": "oewue",\n'
    + '      "id": 6,\n'
    + '      "eepromAddress": 20,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "largeNumItem",\n'
    + '    "item": {\n'
    + '      "digitsAllowed": 12,\n'
    + '      "decimalPlaces": 8,\n'
    + '      "negativeAllowed": true,\n'
    + '      "name": "lge",\n'
    + '      "id": 7,\n'
    + '      "eepromAddress": 64,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "textItem",\n'
    + '    "item": {\n'
    + '      "textLength": 20,\n'
    + '      "itemType": "IP_ADDRESS",\n'
    + '      "name": "ip",\n'
    + '      "id": 8,\n'
    + '      "eepromAddress": 110,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "textItem",\n'
    + '    "item": {\n'
    + '      "textLength": 10,\n'
    + '      "itemType": "PLAIN_TEXT",\n'
    + '      "name": "txt",\n'
    + '      "id": 9,\n'
    + '      "eepromAddress": 101,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  }\n"
    + "]"
)

EXPECTED_COPY_TEXT: str = (
    "tcMenuCopy:[\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "enumItem",\n'
    + '    "defaultValue": "1",\n'
    + '    "item": {\n'
    + '      "enumEntries": [\n'
    + '        "Item1",\n'
    + '        "Item2"\n'
    + "      ],\n"
    + '      "name": "xyz",\n'
    + '      "id": 4,\n'
    + '      "eepromAddress": 101,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "analogItem",\n'
    + '    "defaultValue": "100",\n'
    + '    "item": {\n'
    + '      "maxValue": 255,\n'
    + '      "offset": 102,\n'
    + '      "divisor": 2,\n'
    + '      "unitName": "dB",\n'
    + '      "step": 1,\n'
    + '      "name": "fhs",\n'
    + '      "id": 5,\n'
    + '      "eepromAddress": 104,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "actionMenu",\n'
    + '    "item": {\n'
    + '      "name": "oewue",\n'
    + '      "id": 6,\n'
    + '      "eepromAddress": 20,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "largeNumItem",\n'
    + '    "item": {\n'
    + '      "digitsAllowed": 12,\n'
    + '      "decimalPlaces": 8,\n'
    + '      "negativeAllowed": true,\n'
    + '      "name": "lge",\n'
    + '      "id": 7,\n'
    + '      "eepromAddress": 64,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "textItem",\n'
    + '    "item": {\n'
    + '      "textLength": 20,\n'
    + '      "itemType": "IP_ADDRESS",\n'
    + '      "name": "ip",\n'
    + '      "id": 8,\n'
    + '      "eepromAddress": 110,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  },\n"
    + "  {\n"
    + '    "parentId": 3,\n'
    + '    "type": "textItem",\n'
    + '    "item": {\n'
    + '      "textLength": 10,\n'
    + '      "itemType": "PLAIN_TEXT",\n'
    + '      "name": "txt",\n'
    + '      "id": 9,\n'
    + '      "eepromAddress": 101,\n'
    + '      "readOnly": false,\n'
    + '      "localOnly": false,\n'
    + '      "visible": true\n'
    + "    }\n"
    + "  }\n"
    + "]"
)


def test_serializer():
    items: tuple[PersistedMenu] = get_persisted_menus()
    output_json: str = JsonMenuItemSerializer.to_json(items)

    compare_json_data(output_json, EXPECTED_JSON)

    decoded_items: tuple[PersistedMenu] = JsonMenuItemSerializer.from_json(output_json)
    for idx, item in enumerate(decoded_items):
        assert item.parent_id == items[idx].parent_id
        assert item.type == items[idx].type
        assert item.item == items[idx].item


def test_copy_operations():
    items: tuple[PersistedMenu] = get_persisted_menus()
    tree: MenuTree = MenuTree()

    for item in items:
        tree.add_menu_item(item.item, parent=MenuItemHelper.as_sub_menu(tree.get_menu_by_id(item.parent_id)))

        if item.default_value is not None:
            MenuItemHelper.set_menu_state(item.item, item.default_value, tree)

    output_data = JsonMenuItemSerializer.items_to_copy_text(tree.get_menu_by_id(3), tree)
    assert output_data.startswith(PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX)

    compare_json_data(
        output_data[len(PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX) :],
        EXPECTED_COPY_TEXT[len(PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX) :],
    )

    copied_data: tuple[PersistedMenu] = JsonMenuItemSerializer.copy_text_to_items(output_data)

    assert copied_data[0].parent_id == 3
    assert copied_data[0].item == tree.get_menu_by_id(4)
    assert copied_data[1].item == tree.get_menu_by_id(5)
    assert copied_data[2].item == tree.get_menu_by_id(6)
    assert copied_data[3].item == tree.get_menu_by_id(7)
    assert copied_data[4].item == tree.get_menu_by_id(8)
    assert copied_data[5].item == tree.get_menu_by_id(9)
    assert MenuItemHelper.get_value_for(tree.get_menu_by_id(4), tree, 0) == 1
    assert copied_data[0].default_value == "1"
    assert MenuItemHelper.get_value_for(tree.get_menu_by_id(5), tree, 0) == 100
    assert copied_data[1].default_value == "100"


def get_persisted_menus() -> tuple[PersistedMenu]:
    items: list[PersistedMenu] = [
        PersistedMenu(
            item=DomainFixtures.a_boolean_menu("abc", 1, BooleanMenuItem.BooleanNaming.TRUE_FALSE),
            parent_id=MenuTree.ROOT.id,
        ),
        PersistedMenu(item=DomainFixtures.a_float_menu("def", 2), parent_id=MenuTree.ROOT.id),
    ]
    sub_menu_item: SubMenuItem = DomainFixtures.a_sub_menu("ghi", 3)
    items.append(PersistedMenu(item=sub_menu_item, parent_id=MenuTree.ROOT.id))
    enum_item = PersistedMenu(item=DomainFixtures.an_enum_item("xyz", 4), parent_id=sub_menu_item.id, default_value="1")
    items.append(enum_item)
    analog_item: PersistedMenu = PersistedMenu(
        item=DomainFixtures.an_analog_item("fhs", 5), parent_id=sub_menu_item.id, default_value="100"
    )
    items.append(analog_item)
    items.append(PersistedMenu(item=DomainFixtures.an_action_menu("oewue", 6), parent_id=sub_menu_item.id))
    items.append(PersistedMenu(item=DomainFixtures.a_large_number("lge", 7, 8, True), parent_id=sub_menu_item.id))
    items.append(PersistedMenu(item=DomainFixtures.an_ip_address_menu("ip", 8), parent_id=sub_menu_item.id))
    items.append(PersistedMenu(item=DomainFixtures.a_text_menu("txt", 9), parent_id=sub_menu_item.id))

    return tuple(items)


def compare_json_data(source: str, expected: str):
    source_decoded = json.loads(source)
    expected_decoded = json.loads(expected)

    assert type(source_decoded) == type(expected_decoded) == list
    assert len(source_decoded) == len(expected_decoded)

    for idx, item in enumerate(source_decoded):
        assert item == expected_decoded[idx]
