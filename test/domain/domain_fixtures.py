from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    EnumMenuItem,
    SubMenuItem,
    ActionMenuItem,
    RuntimeListMenuItem,
    EditableTextMenuItem,
    EditableLargeNumberMenuItem,
    FloatMenuItem,
    BooleanMenuItem,
    AnalogMenuItem,
)
from tcmenu.domain.state.menu_tree import MenuTree


class DomainFixtures:
    @staticmethod
    def an_enum_item(name: str, item_id: int, enums: list[str] = None) -> EnumMenuItem:
        if enums is None:
            enums = ["Item1", "Item2"]
        return EnumMenuItem(name=name, id=item_id, eeprom_address=101, enum_entries=enums)

    @staticmethod
    def a_sub_menu(name: str, item_id: int) -> SubMenuItem:
        return SubMenuItem(name=name, id=item_id, eeprom_address=102)

    @staticmethod
    def an_action_menu(name: str, item_id: int) -> ActionMenuItem:
        return ActionMenuItem(name=name, id=item_id, eeprom_address=20)

    @staticmethod
    def a_runtime_list_menu(name: str, item_id: int, rows: int) -> RuntimeListMenuItem:
        return RuntimeListMenuItem(name=name, id=item_id, initial_rows=rows, eeprom_address=88)

    @staticmethod
    def a_text_menu(name: str, item_id: int) -> EditableTextMenuItem:
        return EditableTextMenuItem(name=name, id=item_id, eeprom_address=101, text_length=10)

    @staticmethod
    def an_ip_address_menu(name: str, item_id: int) -> EditableTextMenuItem:
        return EditableTextMenuItem(
            name=name, id=item_id, eeprom_address=110, item_type=EditItemType.IP_ADDRESS, text_length=20
        )

    @staticmethod
    def a_large_number(name: str, item_id: int, dp: int, negative: bool) -> EditableLargeNumberMenuItem:
        return EditableLargeNumberMenuItem(
            name=name, id=item_id, decimal_places=dp, negative_allowed=negative, eeprom_address=64, digits_allowed=12
        )

    @staticmethod
    def a_float_menu(name: str, item_id: int) -> FloatMenuItem:
        return FloatMenuItem(name=name, id=item_id, eeprom_address=105, num_decimal_places=3)

    @staticmethod
    def a_boolean_menu(name: str, item_id: int, naming: BooleanMenuItem.BooleanNaming) -> BooleanMenuItem:
        return BooleanMenuItem(name=name, id=item_id, naming=naming, eeprom_address=102)

    @staticmethod
    def an_analog_item(name: str, item_id: int) -> AnalogMenuItem:
        return AnalogMenuItem(
            name=name, id=item_id, eeprom_address=104, divisor=2, max_value=255, offset=102, unit_name="dB"
        )

    @staticmethod
    def full_esp_amplifier_test_tree() -> MenuTree:
        """
        TODO:
        public static MenuTree fullEspAmplifierTestTree() {
        var serialiser = new JsonMenuItemSerializer();
        return serialiser.newMenuTreeWithItems(COMPLETE_MENU_TREE);
        """

        return MenuTree()

    COMPLETE_MENU_TREE: str = (
        "tcMenuCopy:[\n"
        + "  {\n"
        + '    "parentId": 0,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 255,\n'
        + '      "offset": -180,\n'
        + '      "divisor": 2,\n'
        + '      "unitName": "dB",\n'
        + '      "name": "Volume",\n'
        + '      "variableName": "",\n'
        + '      "id": 1,\n'
        + '      "eepromAddress": 2,\n'
        + '      "functionName": "onVolumeChanged",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 0,\n'
        + '    "type": "scrollItem",\n'
        + '    "item": {\n'
        + '      "itemWidth": 16,\n'
        + '      "eepromOffset": 150,\n'
        + '      "numEntries": 3,\n'
        + '      "choiceMode": "ARRAY_IN_EEPROM",\n'
        + '      "name": "Channel",\n'
        + '      "variableName": "Channels",\n'
        + '      "id": 2,\n'
        + '      "eepromAddress": 4,\n'
        + '      "functionName": "onChannelChanged",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 0,\n'
        + '    "type": "boolItem",\n'
        + '    "item": {\n'
        + '      "naming": "TRUE_FALSE",\n'
        + '      "name": "Direct",\n'
        + '      "variableName": "",\n'
        + '      "id": 3,\n'
        + '      "eepromAddress": 6,\n'
        + '      "functionName": "onAudioDirect",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 0,\n'
        + '    "type": "boolItem",\n'
        + '    "item": {\n'
        + '      "naming": "ON_OFF",\n'
        + '      "name": "Mute",\n'
        + '      "variableName": "",\n'
        + '      "id": 4,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "onMuteSound",\n'
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
        + '      "name": "Settings",\n'
        + '      "variableName": "",\n'
        + '      "id": 5,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 5,\n'
        + '    "type": "subMenu",\n'
        + '    "item": {\n'
        + '      "secured": false,\n'
        + '      "name": "Channel Settings",\n'
        + '      "variableName": "",\n'
        + '      "id": 7,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 7,\n'
        + '    "type": "scrollItem",\n'
        + '    "item": {\n'
        + '      "itemWidth": 10,\n'
        + '      "eepromOffset": 0,\n'
        + '      "numEntries": 3,\n'
        + '      "choiceMode": "CUSTOM_RENDERFN",\n'
        + '      "name": "Channel Num",\n'
        + '      "variableName": "ChannelSettingsChannel",\n'
        + '      "id": 23,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 7,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 20,\n'
        + '      "offset": -10,\n'
        + '      "divisor": 2,\n'
        + '      "unitName": "dB",\n'
        + '      "name": "Level Trim",\n'
        + '      "variableName": "ChannelSettingsLevelTrim",\n'
        + '      "id": 8,\n'
        + '      "eepromAddress": 9,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 7,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 15,\n'
        + '      "itemType": "PLAIN_TEXT",\n'
        + '      "name": "Name",\n'
        + '      "variableName": "ChannelSettingsName",\n'
        + '      "id": 22,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 7,\n'
        + '    "type": "actionMenu",\n'
        + '    "item": {\n'
        + '      "name": "Update Settings",\n'
        + '      "variableName": "ChannelSettingsUpdateSettings",\n'
        + '      "id": 24,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "onChannelSetttingsUpdate",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 5,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 300,\n'
        + '      "offset": 0,\n'
        + '      "divisor": 10,\n'
        + '      "unitName": "s",\n'
        + '      "name": "Warm up time",\n'
        + '      "variableName": "SettingsWarmUpTime",\n'
        + '      "id": 11,\n'
        + '      "eepromAddress": 7,\n'
        + '      "functionName": "@warmUpChanged",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 5,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 600,\n'
        + '      "offset": 0,\n'
        + '      "divisor": 10,\n'
        + '      "unitName": "s",\n'
        + '      "name": "Valve Heating",\n'
        + '      "variableName": "SettingsValveHeating",\n'
        + '      "id": 17,\n'
        + '      "eepromAddress": 15,\n'
        + '      "functionName": "@valveHeatingChanged",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 5,\n'
        + '    "type": "actionMenu",\n'
        + '    "item": {\n'
        + '      "name": "Save settings",\n'
        + '      "variableName": "",\n'
        + '      "id": 25,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "onSaveSettings",\n'
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
        + '      "name": "Status",\n'
        + '      "variableName": "",\n'
        + '      "id": 6,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "enumItem",\n'
        + '    "item": {\n'
        + '      "enumEntries": [\n'
        + '        "Warm up",\n'
        + '        "Warm Valves",\n'
        + '        "Ready",\n'
        + '        "DC Protection",\n'
        + '        "Overloaded",\n'
        + '        "Overheated"\n'
        + "      ],\n"
        + '      "name": "Amp Status",\n'
        + '      "variableName": "",\n'
        + '      "id": 14,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": true,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 30000,\n'
        + '      "offset": -20000,\n'
        + '      "divisor": 1000,\n'
        + '      "unitName": "dB",\n'
        + '      "name": "Left VU",\n'
        + '      "variableName": "StatusLeftVU",\n'
        + '      "id": 15,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": true,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 30000,\n'
        + '      "offset": -20000,\n'
        + '      "divisor": 1000,\n'
        + '      "unitName": "dB",\n'
        + '      "name": "Right VU",\n'
        + '      "variableName": "",\n'
        + '      "id": 16,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": true,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "actionMenu",\n'
        + '    "item": {\n'
        + '      "name": "Show Dialogs",\n'
        + '      "variableName": "",\n'
        + '      "id": 20,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "onShowDialogs",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "runtimeList",\n'
        + '    "item": {\n'
        + '      "initialRows": 0,\n'
        + '      "name": "Data List",\n'
        + '      "variableName": "StatusDataList",\n'
        + '      "id": 21,\n'
        + '      "eepromAddress": -1,\n'
        + '      "functionName": "",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 6,\n'
        + '    "type": "analogItem",\n'
        + '    "item": {\n'
        + '      "maxValue": 65535,\n'
        + '      "offset": -5000,\n'
        + '      "divisor": 10,\n'
        + '      "unitName": "U",\n'
        + '      "name": "Test",\n'
        + '      "variableName": "StatusTest",\n'
        + '      "id": 28,\n'
        + '      "eepromAddress": -1,\n'
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
        + '      "name": "Connectivity",\n'
        + '      "variableName": "",\n'
        + '      "id": 12,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 5,\n'
        + '      "itemType": "IP_ADDRESS",\n'
        + '      "name": "IP address",\n'
        + '      "variableName": "",\n'
        + '      "id": 13,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": true,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 20,\n'
        + '      "itemType": "PLAIN_TEXT",\n'
        + '      "name": "SSID",\n'
        + '      "variableName": "",\n'
        + '      "id": 18,\n'
        + '      "eepromAddress": 17,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 20,\n'
        + '      "itemType": "PLAIN_TEXT",\n'
        + '      "name": "Passcode",\n'
        + '      "variableName": "",\n'
        + '      "id": 19,\n'
        + '      "eepromAddress": 37,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 20,\n'
        + '      "itemType": "TIME_24_HUNDREDS",\n'
        + '      "name": "Time 24",\n'
        + '      "variableName": "",\n'
        + '      "id": 91,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "textItem",\n'
        + '    "item": {\n'
        + '      "textLength": 20,\n'
        + '      "itemType": "GREGORIAN_DATE",\n'
        + '      "name": "Date field",\n'
        + '      "variableName": "",\n'
        + '      "id": 92,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "customBuildItem",\n'
        + '    "item": {\n'
        + '      "menuType": "REMOTE_IOT_MONITOR",\n'
        + '      "name": "IoT Monitor",\n'
        + '      "id": 26,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "customBuildItem",\n'
        + '    "item": {\n'
        + '      "menuType": "AUTHENTICATION",\n'
        + '      "name": "Authenticator",\n'
        + '      "id": 27,\n'
        + '      "eepromAddress": -1,\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  },\n"
        + "  {\n"
        + '    "parentId": 12,\n'
        + '    "type": "rgbItem",\n'
        + '    "item": {\n'
        + '      "includeAlphaChannel": false,\n'
        + '      "name": "RGB",\n'
        + '      "variableName": "",\n'
        + '      "id": 90,\n'
        + '      "eepromAddress": 16,\n'
        + '      "functionName": "onRgbChanged",\n'
        + '      "readOnly": false,\n'
        + '      "localOnly": false,\n'
        + '      "visible": true\n'
        + "    }\n"
        + "  }\n"
        + "]"
    )
