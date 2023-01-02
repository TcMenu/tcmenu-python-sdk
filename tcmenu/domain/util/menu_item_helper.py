import dataclasses
from typing import Optional, Any

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    MenuItem,
    SubMenuItem,
    RuntimeListMenuItem,
    EditableTextMenuItem,
    EditableLargeNumberMenuItem,
    ScrollChoiceMenuItem,
    Rgb32MenuItem,
    AnalogMenuItem,
    BooleanMenuItem,
    EnumMenuItem,
    FloatMenuItem,
    ActionMenuItem,
)
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.menu_state import (
    MenuState,
    BooleanMenuState,
    IntegerMenuState,
    FloatMenuState,
    StringMenuState,
    BigDecimalMenuState,
    StringListMenuState,
    CurrentScrollPositionMenuState,
    PortableColorMenuState,
)
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.remote.commands.menu_command import (
    BootItemMenuCommand,
    MenuAnalogBootCommand,
    MenuEnumBootCommand,
    MenuFloatBootCommand,
    MenuBooleanBootCommand,
    MenuSubBootCommand,
    MenuActionBootCommand,
    MenuLargeNumBootCommand,
    MenuTextBootCommand,
    MenuRgb32BootCommand,
    MenuRuntimeListBootCommand,
    MenuScrollChoiceBootCommand,
)


class MenuItemHelper:
    """
    A helper class for dealing with MenuItem objects. This class provides helpers for visiting
    menu items and returning a result. It also provides other helpers for dealing with items.
    """

    @staticmethod
    def as_sub_menu(item: MenuItem) -> Optional[SubMenuItem]:
        """
        Returns the menu item as a sub menu or None
        :param: item the possible sub menu
        :return: the sub menu, or None.
        """
        if isinstance(item, SubMenuItem):
            return item
        return None

    @staticmethod
    def is_runtime_structure_needed(item: MenuItem) -> bool:
        """
        Check if the item is based on a runtime item
        :param: item the item to check
        :return: true if runtime based, otherwise false.
        """
        if isinstance(item, RuntimeListMenuItem):
            return True
        elif isinstance(item, EditableTextMenuItem):
            return True
        elif isinstance(item, EditableLargeNumberMenuItem):
            return True
        elif isinstance(item, ScrollChoiceMenuItem):
            return True
        elif isinstance(item, Rgb32MenuItem):
            return True
        elif isinstance(item, SubMenuItem):
            # needed for the back menu item
            return True
        elif isinstance(item, MenuItem):
            return False
        else:
            return False

    @staticmethod
    def create_from_existing_with_id(selected: MenuItem, new_id: int) -> MenuItem:
        """
        Creates a copy of the menu item chosen, with the ID changed to new_id
        :param: selected the item to copy
        :param: new_id the ID for the copy
        :return: the newly created item
        """
        return dataclasses.replace(selected, id=new_id)

    @staticmethod
    def eeprom_size_for_item(item: Optional[MenuItem]):
        """
        Gets the size of the eeprom storage for a given element type
        :param: item the item to determine eeprom size for
        :return: the eeprom storage needed.
        """
        if item is None:
            return 0
        elif isinstance(item, AnalogMenuItem):
            return 2
        elif isinstance(item, BooleanMenuItem):
            return 1
        elif isinstance(item, EnumMenuItem):
            return 2
        elif isinstance(item, EditableLargeNumberMenuItem):
            return 8
        elif isinstance(item, Rgb32MenuItem):
            return 4
        elif isinstance(item, ScrollChoiceMenuItem):
            return 2
        elif isinstance(item, EditableTextMenuItem):
            if item.item_type == EditItemType.IP_ADDRESS:
                return 4
            elif item.item_type == EditItemType.PLAIN_TEXT:
                return item.text_length
            else:
                # all date and time types are 4 bytes long
                return 4
        elif isinstance(item, MenuItem):
            return 0
        else:
            return 0

    @staticmethod
    def modify_existing_state_for_menu_item(
        existing_state: Optional[MenuState], item: MenuItem, value: Any, changed: Optional[bool] = None
    ) -> MenuState:
        """
        Modify an existing state with a new value.
        :param: existing_state the existing state object
        :param: item the item
        :param: value the changed value
        :param: changed optional new change status. If not specified, existing state will be kept
        :return: a new state object based on the parameters
        """
        active = False

        if existing_state is not None:
            active = existing_state.active
            if changed is None:
                changed = existing_state.changed

        if changed is None:
            changed = False

        return MenuItemHelper.state_for_menu_item(item, value, changed, active)

    @staticmethod
    def state_for_menu_item(item: Optional[MenuItem], value: Any, changed: bool, active: bool) -> MenuState:
        """
        Create a menu state for a given item with a value update. We try pretty hard
        to convert whatever comes in for the value into a new state.

        :param: item the item to create the state for
        :param: value the value
        :param: changed the changed status
        :param: active the active status
        :return: the new menu state
        """
        if item is None:
            return BooleanMenuState(item=MenuItem(), changed=False, active=False, value=False)

        if value is None:
            value = MenuItemHelper.get_default_for(item)

        if isinstance(item, AnalogMenuItem):
            res = int(value)
            if res < 0:
                res = 0
            if res > item.max_value:
                res = item.max_value
            return IntegerMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, BooleanMenuItem):
            if type(value) == str:
                res = value.lower() in ("true", "1", "y")
            else:
                res = bool(value)
            return BooleanMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, EnumMenuItem):
            res = int(value)
            if res < 0:
                res = 0
            if res > len(item.enum_entries):
                res = len(item.enum_entries) - 1
            return IntegerMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, SubMenuItem):
            return BooleanMenuState(item=MenuItem(), changed=changed, active=active, value=False)
        elif isinstance(item, EditableTextMenuItem):
            return StringMenuState(item=item, changed=changed, active=active, value=str(value))
        elif isinstance(item, ActionMenuItem):
            pass
        elif isinstance(item, FloatMenuItem):
            res = float(value)
            return FloatMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, RuntimeListMenuItem):
            res = [str(x) for x in value]
            return StringListMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, EditableLargeNumberMenuItem):
            res = float(value)
            return BigDecimalMenuState(item=item, changed=changed, active=active, value=res)
        elif isinstance(item, ScrollChoiceMenuItem):
            pos: CurrentScrollPosition

            if type(value) == int:
                pos = CurrentScrollPosition(position=value, value="")
            elif isinstance(value, CurrentScrollPosition):
                pos = value
            else:
                pos = CurrentScrollPosition.from_text(str(value))

            if 0 <= pos.position < item.num_entries:
                return CurrentScrollPositionMenuState(item=item, changed=changed, active=active, value=pos)
            else:
                return CurrentScrollPositionMenuState(
                    item=item, changed=changed, active=active, value=CurrentScrollPosition(0, "No entries")
                )
        elif isinstance(item, Rgb32MenuItem):
            color: PortableColor

            if type(value) == str:
                color = PortableColor.from_html(value)
            elif isinstance(value, PortableColor):
                color = value
            else:
                raise ValueError("Invalid value for Rgb32MenuItem.")
            return PortableColorMenuState(item=item, changed=changed, active=active, value=color)
        elif isinstance(item, MenuItem):
            return BooleanMenuState(item=MenuItem(), changed=changed, active=active, value=False)

    @staticmethod
    def apply_incremental_value_change(item: MenuItem, delta: int, tree: "MenuTree") -> Optional[MenuState]:
        """
        Try and apply an incremental delta value update to a menu tree. This works for integer, enum and scroll items.
        It loads the existing value and tries to apply the delta offset, if the min/max would not be exceeded.

        :param: item the item to change
        :param: delta the delta amount
        :param: tree the tree the item belongs to
        :return: a new item if the operation was possible, otherwise empty
        """
        state = tree.get_menu_state(item)
        if state is None:
            state = MenuItemHelper.state_for_menu_item(item, 0, False, False)

        if state.storage_type == MenuState.StateStorageType.INTEGER:
            val = state.value + delta

            if (
                val < 0
                or (isinstance(item, AnalogMenuItem) and val > item.max_value)
                or (isinstance(item, EnumMenuItem) and val > len(item.enum_entries))
            ):
                return None

            menu_state = MenuItemHelper.modify_existing_state_for_menu_item(state, item, state.value + delta)
            tree.change_item(item, menu_state)
            return menu_state
        elif state.storage_type == MenuState.StateStorageType.SCROLL_POSITION:
            val = state.value.position + delta

            if val <= 0 or (isinstance(item, ScrollChoiceMenuItem) and val >= item.num_entries):
                return None

            current_scroll_position = CurrentScrollPosition(state.value.position + delta, "")
            menu_state = MenuItemHelper.modify_existing_state_for_menu_item(state, item, current_scroll_position)
            tree.change_item(item, menu_state)
            return menu_state

        return None

    @staticmethod
    def set_menu_state(item: MenuItem, value: Any, tree: "MenuTree"):
        """
        Set the state in the tree for an item with a new value, setting it changed if it genuinely has.
        :param: item the item
        :param: value the replacement value
        :param: tree the tree to change
        """
        old_state = tree.get_menu_state(item)

        if old_state is not None:
            tree.change_item(
                item,
                MenuItemHelper.state_for_menu_item(
                    item, value, changed=value != old_state.value, active=old_state.active
                ),
            )
        else:
            tree.change_item(item, MenuItemHelper.state_for_menu_item(item, value, changed=False, active=False))

    @staticmethod
    def get_value_for(item: MenuItem, tree: "MenuTree", default: Optional[Any] = None):
        """
        Gets the value from the tree or the default provided
        :param: item the item
        :param: tree the tree to lookup in
        :param: def the default item (get_default_for can get the default automatically)
        :return: the item looked up, or the default.
        """
        if default is None:
            default = MenuItemHelper.get_default_for(item)

        if tree.get_menu_state(item) is not None:
            return tree.get_menu_state(item).value

        tree.change_item(
            item=item,
            menu_state=MenuItemHelper.state_for_menu_item(item=item, value=default, changed=False, active=False),
        )
        return default

    @staticmethod
    def get_default_for(item: MenuItem) -> Any:
        """
        Gets the default item value for a menu item, such that the value could be used in call to set state.
        :param: item the item
        :return: the default value
        """
        if isinstance(item, AnalogMenuItem) or isinstance(item, EnumMenuItem):
            return 0
        elif isinstance(item, FloatMenuItem):
            return float(0)
        elif isinstance(item, BooleanMenuItem) or isinstance(item, SubMenuItem):
            return False
        elif isinstance(item, EditableLargeNumberMenuItem):
            return 0
        elif isinstance(item, EditableTextMenuItem):
            return ""
        elif isinstance(item, Rgb32MenuItem):
            return PortableColor(red=0, green=0, blue=0)
        elif isinstance(item, RuntimeListMenuItem):
            return []
        elif isinstance(item, ScrollChoiceMenuItem):
            return CurrentScrollPosition(position=0, value="")
        else:
            return False

    @staticmethod
    def get_boot_msg_for_item(item: MenuItem, parent: SubMenuItem, tree: "MenuTree") -> Optional[BootItemMenuCommand]:
        """
        Can be used during boot sequences to get a suitable boot item for a menu item
        :param: item the item
        :param: parent the parent
        :param: tree the tree it belongs to
        :return: either a boot item or empty
        """
        if isinstance(item, AnalogMenuItem):
            return MenuAnalogBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, 0)
            )
        elif isinstance(item, EnumMenuItem):
            return MenuEnumBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, 0)
            )
        elif isinstance(item, FloatMenuItem):
            return MenuFloatBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, 0.0)
            )
        elif isinstance(item, BooleanMenuItem):
            return MenuBooleanBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, False)
            )
        elif isinstance(item, SubMenuItem):
            return MenuSubBootCommand(sub_menu_id=parent.id, menu_item=item, current_value=False)
        elif isinstance(item, ActionMenuItem):
            return MenuActionBootCommand(sub_menu_id=parent.id, menu_item=item, current_value=False)
        elif isinstance(item, EditableLargeNumberMenuItem):
            return MenuLargeNumBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, 0)
            )
        elif isinstance(item, EditableTextMenuItem):
            return MenuTextBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, "")
            )
        elif isinstance(item, Rgb32MenuItem):
            return MenuRgb32BootCommand(
                sub_menu_id=parent.id,
                menu_item=item,
                current_value=MenuItemHelper.get_value_for(item, tree, PortableColor(0, 0, 0)),
            )
        elif isinstance(item, RuntimeListMenuItem):
            return MenuRuntimeListBootCommand(
                sub_menu_id=parent.id, menu_item=item, current_value=MenuItemHelper.get_value_for(item, tree, [])
            )
        elif isinstance(item, ScrollChoiceMenuItem):
            return MenuScrollChoiceBootCommand(
                sub_menu_id=parent.id,
                menu_item=item,
                current_value=MenuItemHelper.get_value_for(item, tree, CurrentScrollPosition(0, "")),
            )
        else:
            return None
