import logging
import json
from typing import Any

import humps

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    SubMenuItem,
    MenuItem,
    ActionMenuItem,
    RuntimeListMenuItem,
    CustomBuilderMenuItem,
    EnumMenuItem,
    AnalogMenuItem,
    BooleanMenuItem,
    EditableTextMenuItem,
    EditableLargeNumberMenuItem,
    ScrollChoiceMenuItem,
    Rgb32MenuItem,
    FloatMenuItem,
)
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from tcmenu.persist.persisted_menu import PersistedMenu


class JsonMenuItemSerializer:
    """
    Creates a menu serializer instance that can convert menu structures to and from JSON format. In the simplest case
    just create a new instance of the class, and you can use it to convert between formats.

    <pre>
        json_serializer = JsonMenuItemSerializer()
        tree = json_serializer.new_menu_tree_with_items(text_copied_from_the_menu_designer)
        json = json_serializer.items_to_copy_text(MenuTree.ROOT, tree);
    </pre>
    """

    PARENT_ID: str = "parent_id"
    TYPE_ID: str = "type"
    DEF_VALUE_ID: str = "default_value"
    ITEM_ID: str = "item"

    logger = logging.getLogger("JsonMenuItemSerializer")

    @staticmethod
    def populate_list_in_order(node: SubMenuItem, menu_tree: MenuTree) -> tuple[PersistedMenu]:
        data: list[PersistedMenu] = []
        items: tuple[MenuItem] = menu_tree.get_menu_items(node)
        for item in items:
            persisted_menu = PersistedMenu(item, node.id)
            if menu_tree.get_menu_state(item) is not None:
                persisted_menu.default_value = str(
                    MenuItemHelper.get_value_for(item, menu_tree, MenuItemHelper.get_default_for(item))
                )
            data.append(persisted_menu)
            if item.has_children():
                data.extend(JsonMenuItemSerializer.populate_list_in_order(MenuItemHelper.as_sub_menu(item), menu_tree))

        return tuple(data)

    @staticmethod
    def items_to_copy_text(starting_point: MenuItem, tree: MenuTree) -> str:
        items: tuple[PersistedMenu]

        if isinstance(starting_point, SubMenuItem):
            items = JsonMenuItemSerializer.populate_list_in_order(starting_point, tree)
        else:
            menu: PersistedMenu = PersistedMenu(
                starting_point,
                tree.find_parent(starting_point).id,
                default_value=str(MenuItemHelper.get_value_for(starting_point, tree)),
            )
            items = (menu,)

        return f"{PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX}{JsonMenuItemSerializer.to_json(items)}"

    @staticmethod
    def copy_text_to_items(copy_text: str) -> tuple[PersistedMenu]:
        if not copy_text.startswith(PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX):
            return tuple()

        json_str: str = copy_text[len(PersistedMenu.ItemTypes.TCMENU_COPY_PREFIX) :]
        return JsonMenuItemSerializer.from_json(json_str)

    @staticmethod
    def new_menu_tree_with_items(tc_menu_copy: str) -> MenuTree:
        tree: MenuTree = MenuTree()
        items: tuple[PersistedMenu] = JsonMenuItemSerializer.copy_text_to_items(tc_menu_copy)

        for item in items:
            tree.add_menu_item(parent=tree.get_sub_menu_by_id(item.parent_id), item=item.item)

            if item.default_value is not None:
                MenuItemHelper.set_menu_state(item.item, item.default_value, tree)

        return tree

    @staticmethod
    def to_json(items: tuple[PersistedMenu]) -> str:
        """
        Convert PersistedMenu items to json.
        :param items: tuple containing PersistedMenu items.
        :return: JSON
        """
        return json.dumps(items, indent=4, cls=PersistedMenuEncoder)

    @staticmethod
    def from_json(json_str: str) -> tuple[PersistedMenu]:
        """
        Convert json back to PersistedMenu items.
        :param json_str: JSON string containing PersistedMenu items.
        :return: tuple containing PersistedMenu items.
        """
        data = json.loads(json_str, object_hook=lambda val: humps.decamelize(val))
        return tuple(map(JsonMenuItemSerializer.deserialize, data))

    @staticmethod
    def check_item_value_can_persist(persisted_menu: PersistedMenu) -> bool:
        """
        There are some menu types that should not have a default value, these generally don't have a value
        associated with them that can be easily saved, such as lists, action items and submenus.
        :param persisted_menu: the item to check
        :return: True if the item value can be persisted, otherwise False
        """
        item: MenuItem = persisted_menu.item
        return not (
            isinstance(item, SubMenuItem)
            or isinstance(item, ActionMenuItem)
            or isinstance(item, RuntimeListMenuItem)
            or isinstance(item, CustomBuilderMenuItem)
        )

    @staticmethod
    def deserialize(data: dict[str]) -> PersistedMenu:
        map_of_types = {
            PersistedMenu.ItemTypes.ENUM_PERSIST_TYPE: EnumMenuItem,
            PersistedMenu.ItemTypes.ANALOG_PERSIST_TYPE: AnalogMenuItem,
            PersistedMenu.ItemTypes.BOOLEAN_PERSIST_TYPE: BooleanMenuItem,
            PersistedMenu.ItemTypes.ACTION_PERSIST_TYPE: ActionMenuItem,
            PersistedMenu.ItemTypes.TEXT_PERSIST_TYPE: EditableTextMenuItem,
            PersistedMenu.ItemTypes.SUB_PERSIST_TYPE: SubMenuItem,
            PersistedMenu.ItemTypes.RUNTIME_LIST_PERSIST_TYPE: RuntimeListMenuItem,
            PersistedMenu.ItemTypes.RUNTIME_LARGE_NUM_PERSIST_TYPE: EditableLargeNumberMenuItem,
            PersistedMenu.ItemTypes.CUSTOM_ITEM_PERSIST_TYPE: CustomBuilderMenuItem,
            PersistedMenu.ItemTypes.SCROLL_CHOICE_PERSIST_TYPE: ScrollChoiceMenuItem,
            PersistedMenu.ItemTypes.RGB32_COLOR_PERSIST_TYPE: Rgb32MenuItem,
            PersistedMenu.ItemTypes.FLOAT_PERSIST_TYPE: FloatMenuItem,
        }

        # Special handling for some items
        if data["type"] == PersistedMenu.ItemTypes.BOOLEAN_PERSIST_TYPE:
            data["item"]["naming"] = BooleanMenuItem.BooleanNaming[data["item"]["naming"]]
        elif data["type"] == PersistedMenu.ItemTypes.CUSTOM_ITEM_PERSIST_TYPE:
            data["item"]["menu_type"] = CustomBuilderMenuItem.CustomMenuType[data["item"]["menu_type"]]
        elif data["type"] == PersistedMenu.ItemTypes.TEXT_PERSIST_TYPE:
            data["item"]["item_type"] = EditItemType[data["item"]["item_type"]]
        elif data["type"] == PersistedMenu.ItemTypes.ENUM_PERSIST_TYPE:
            data["item"]["enum_entries"] = tuple(data["item"]["enum_entries"])
        elif data["type"] == PersistedMenu.ItemTypes.SCROLL_CHOICE_PERSIST_TYPE:
            data["item"]["choice_mode"] = ScrollChoiceMenuItem.ScrollChoiceMode[data["item"]["choice_mode"]]

        # noinspection PyArgumentList
        item: MenuItem = map_of_types[data[JsonMenuItemSerializer.TYPE_ID]](**data[JsonMenuItemSerializer.ITEM_ID])
        default_value: str = data.get(JsonMenuItemSerializer.DEF_VALUE_ID)

        try:
            return PersistedMenu(
                item=item,
                item_type=data[JsonMenuItemSerializer.TYPE_ID],
                parent_id=data[JsonMenuItemSerializer.PARENT_ID],
                default_value=default_value,
            )
        except KeyError:
            JsonMenuItemSerializer.logger.error(f"Item of type {data['type']} was not reloaded - skipping")


class PersistedMenuEncoder(json.JSONEncoder):
    @staticmethod
    def clean_nones(value):
        """
        Recursively remove all None values from dictionaries and lists, and returns
        the result as a new dictionary or list.
        """
        if isinstance(value, list):
            return [PersistedMenuEncoder.clean_nones(x) for x in value if x is not None]
        elif isinstance(value, dict):
            return {key: PersistedMenuEncoder.clean_nones(val) for key, val in value.items() if val is not None}
        else:
            return value

    def default(self, obj: Any) -> Any:
        if isinstance(obj, PersistedMenu):
            data = {
                "parent_id": int(obj.parent_id),
                "type": str(obj.type),
                "item": obj.item.__dict__,
                "default_value": obj.default_value,
            }
            return PersistedMenuEncoder.clean_nones(humps.camelize(data))
        elif isinstance(obj, BooleanMenuItem.BooleanNaming):
            return str(obj.name)
        elif isinstance(obj, CustomBuilderMenuItem.CustomMenuType):
            return str(obj.name)
        elif isinstance(obj, EditItemType):
            return str(obj.name)
        elif isinstance(obj, ScrollChoiceMenuItem.ScrollChoiceMode):
            return str(obj.name)

        return json.JSONEncoder.default(self, obj)
