from enum import Enum
from typing import Optional

from tcmenu.domain.menu_items import SubMenuItem, MenuItem
from tcmenu.domain.state.menu_state import MenuState
from tcmenu.domain.util.menu_item_helper import MenuItemHelper


class MenuTree:
    """
    Menu tree holds all the menu items for a specific remote connection or local session. It holds a hierarchy of
    items, where items of type submenu can hold other items. As menu items are immutable, the state for each item is
    held separately, and can be accessed from here for each item. There are many helper methods on `MenuItemHelper`
    that make working with menu items easier.
    :see: MenuItemHelper
    """

    """
    Some operations support moving items up or down in the tree, when they do they use this enumeration to
    describe the direction of the move.
    """

    class MoveType(Enum):
        MOVE_UP = 0
        MOVE_DOWN = 1

    """This is the root menu item, the top level item on the display basically."""
    ROOT = SubMenuItem(
        name="Root", variable_name=None, id=0, eeprom_address=-1, read_only=False, local_only=True, visible=False
    )

    """The maximum expected items in a typical menu."""
    _EXPECTED_MAX_VALUES: int = 256

    def __init__(self):
        """
        This dictionary holds the state for each item, it's the only semi immutable part of the library, even though
        the actual state objects are immutable, and are replaced on change.
        """
        self._menu_states: dict[int, MenuState] = {}

        """
        Submenus are organized as a sub menu containing a list of items.
        """
        self._sub_menu_items: dict[MenuItem, [MenuItem]] = {}

        """Create a basic tree that is initially empty."""
        self._sub_menu_items[MenuTree.ROOT] = []

    def add_menu_item(self, item: MenuItem, parent: SubMenuItem = ROOT):
        """
        Add a new menu item to a sub menu, for the top level menu use ROOT.
        :param: item the item to be added.
        :param: parent the submenu where this should appear.
        """
        if parent not in self._sub_menu_items:
            self._sub_menu_items[parent] = []
        self._sub_menu_items[parent].append(item)

        if item.has_children():
            self._sub_menu_items[item] = []

    def add_or_update_item(self, item: MenuItem, parent_id: int):
        """
        This will either add or update an existing item, depending on the ID is already present.
        :param: item the item to either add or update.
        :param: parent_id the parent where it should be placed / already exists.
        """
        pass

    def get_sub_menu_by_id(self, parent_id: int) -> Optional[SubMenuItem]:
        """
        Gets a submenu by its ID. Returns an optional that will be empty when not present
        :param: parent_id the parent to obtain.
        :return: an optional that will be populated when present with the sub menu.
        """
        pass

    def get_menu_by_id(self, menu_id: int) -> Optional[MenuItem]:
        """
        Gets the menu item with the specified ID, finding the submenu if needed. If you don't know
        the sub menu set it to null, and it will be determined.
        :param: menu_id the id of the object to find.
        :return: the menu at the given id
        """
        pass

    def replace_menu_by_id(self, to_replace: MenuItem, sub_menu: Optional[SubMenuItem] = None):
        """
        Replace the menu item that has a given parent with the one provided. This is an infrequent
        operation and therefore not optimized. If you don't specify a parent, we will look it up.
        :param: to_replace the menu item to replace by ID.
        :param: sub_menu the parent.
        """
        pass

    def move_item(self, parent: SubMenuItem, new_item: MenuItem, move_type: MoveType):
        """
        Moves the item either up or down in the list for that submenu.
        :param: parent the parent id.
        :param: new_item the item to move.
        :param: move_type the direction of the move.
        """
        pass

    def find_parent(self, to_find: MenuItem) -> Optional[SubMenuItem]:
        """
        Finds the submenu that the provided object belongs to.
        :param: to_find the object to find sub menu for.
        :return: the submenu.
        """
        parent = None
        for (menu_item, sub_menu_items) in self._sub_menu_items.items():
            for item in sub_menu_items:
                if item.id == to_find.id:
                    parent = MenuItemHelper.as_sub_menu(menu_item)

        return parent

    def remove_menu_item(self, item: MenuItem, parent: Optional[SubMenuItem]):
        """
        Remove the menu item for the provided menu item in the provided sub menu.
        :param: item the item to remove (Search By ID).
        :param: parent the submenu to search.
        """
        if parent is None:
            parent = self.find_parent(item)

        sub_menu_children: [MenuItem] = self._sub_menu_items.get(parent)

        for child in sub_menu_children:
            if child.id == item.id:
                sub_menu_children.remove(child)
                break

        if item.has_children():
            self._sub_menu_items.pop(item)

        self._menu_states.pop(item.id, None)

    def get_all_sub_menus(self) -> set[MenuItem]:
        """
        Returns all the submenus that are currently stored.
        :return: all available sub menus.
        """
        pass

    def get_menu_items(self, item: MenuItem) -> Optional[list[MenuItem]]:
        """
        Get a list of all menu items for a given submenu.
        :param: item the submenu to use.
        :return: a list of submenu items.
        """
        return self._sub_menu_items.get(item)

    def get_all_menu_items(self) -> set[MenuItem]:
        """
        Gets every menu item held in this menu tree, will be unique.
        :return: every menu item in the tree.
        """
        pass

    def get_all_menu_items_from(self, item: SubMenuItem) -> list[MenuItem]:
        """
        Gets every menu item held in this menu tree from a given starting point, the starting point is a sub menu,
        from that submenu, this method will recurse through the rest of the menu structure and provide a complete list.
        The menu item provided itself will be the first item in the list, the rest will be in exact order as added.
        Use this method over get_all_menu_items() when the order is important, just call with `MenuTree.ROOT` to get all
        items in the tree.
        :param: item the starting point for traversal.
        :return: every menu item in the tree from the given starting point.
        """
        pass

    def change_item(self, item: MenuItem, menu_state: MenuState):
        """
        Change the value that's associated with a menu item. if you are changing
        a value, just send a command to the device, it will automatically update
        the tree.

        :param: item the item to change.
        :param: menu_state the new state.
        """
        self._menu_states[item.id] = menu_state

    def get_menu_state(self, item: MenuItem) -> Optional[MenuState]:
        """
        Gets the menu state that's associated with a given menu item. This is the
        current value for the menu item.
        :param: item the item which the state belongs to.
        :return: the state for the given menu item.
        """
        return self._menu_states.get(item.id)

    def recurse_tree_iterating_on_items(self, root: SubMenuItem, consumer):
        """
        Recurse the whole menu tree calling the consumer for each item in turn. This will always be in order so that
        a child item never comes before its parent.
        :param: root the starting point, normally ROOT.
        :param: consumer the consumer that will be called for each item, providing the item and the parent.
        """
        pass

    def initialize_state_for_each_item(self):
        """
        Initialize the state of each menu item to the default value, should be used during initialization of a local
        menu application. Will only take effect when there is no state already stored.
        """
        pass
