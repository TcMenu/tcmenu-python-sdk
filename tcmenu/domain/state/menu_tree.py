from enum import Enum, auto
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

    # noinspection PyArgumentList
    class MoveType(Enum):
        MOVE_UP = auto()
        MOVE_DOWN = auto()

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
        :param item: the item to be added.
        :param parent: the submenu where this should appear.
        """
        if parent not in self._sub_menu_items:
            self._sub_menu_items[parent] = []
        self._sub_menu_items[parent].append(item)

        if item.has_children():
            self._sub_menu_items[item] = []

    def add_or_update_item(self, item: MenuItem, parent_id: int):
        """
        This will either add or update an existing item, depending on the ID is already present.
        :param item: the item to either add or update.
        :param parent_id: the parent where it should be placed / already exists.
        """
        sub_menu = self.get_sub_menu_by_id(parent_id)
        if sub_menu is not None:
            if next(filter(lambda menu: menu.id == item.id, self.get_menu_items(sub_menu)), None):
                self.replace_menu_by_id(sub_menu=MenuItemHelper.as_sub_menu(sub_menu), to_replace=item)
            else:
                self.add_menu_item(parent=MenuItemHelper.as_sub_menu(sub_menu), item=item)

    def get_sub_menu_by_id(self, parent_id: int) -> Optional[SubMenuItem]:
        """
        Gets a submenu by its ID. Returns an optional that will be empty when not present
        :param parent_id: the parent to obtain.
        :return: an optional that will be populated when present with the sub menu.
        """
        return next(filter(lambda sub_menu: sub_menu.id == parent_id, self.get_all_sub_menus()), None)

    def get_menu_by_id(self, menu_id: int) -> Optional[MenuItem]:
        """
        Gets the menu item with the specified ID, finding the submenu if needed. If you don't know
        the sub menu set it to null, and it will be determined.
        :param menu_id: the id of the object to find.
        :return: the menu at the given id
        """
        state = self._menu_states.get(menu_id)
        if state is not None:
            return state.item

        # Shortcut to find the submenu by ID if possible before going through everything.
        maybe_sub_menu = next(filter(lambda menu: menu.id == menu_id, self.get_all_sub_menus()), None)
        if maybe_sub_menu is not None:
            return maybe_sub_menu

        return next(filter(lambda menu: menu.id == menu_id, self.get_all_menu_items()), None)

    def replace_menu_by_id(self, to_replace: MenuItem, sub_menu: SubMenuItem = None):
        """
        Replace the menu item that has a given parent with the one provided. This is an infrequent
        operation and therefore not optimized. If you don't specify a parent, we will look it up.
        :param to_replace: the menu item to replace by ID.
        :param sub_menu: the parent.
        """
        if sub_menu is None:
            sub_menu = self.find_parent(to_replace)

        idx = None
        for i, item in enumerate(self._sub_menu_items[sub_menu]):
            if item.id == to_replace.id:
                idx = i
                break

        if idx is not None:
            # We found the original, so we now change that index to the new entry
            old_item: MenuItem = self._sub_menu_items[sub_menu][idx].id
            self._sub_menu_items[sub_menu][idx] = to_replace

            # Now we update the "state" which also acts like a cache of menu items for lookup
            old_state = self._menu_states.get(to_replace.id)
            if old_state is not None:
                self._menu_states[to_replace.id] = MenuItemHelper.modify_existing_state_for_menu_item(
                    old_state, to_replace, old_state.value
                )

            # Lastly if the item was a submenu, we need change the top level submenu list as well.
            if to_replace.has_children():
                items = self._sub_menu_items.pop(old_item)
                self._sub_menu_items[to_replace] = items

    def move_item(self, parent: SubMenuItem, new_item: MenuItem, move_type: MoveType):
        """
        Moves the item either up or down in the list for that submenu.
        :param parent: the parent id.
        :param new_item: the item to move.
        :param move_type: the direction of the move.
        """
        items: [MenuItem] = self._sub_menu_items[parent]

        try:
            idx = items.index(new_item)
        except ValueError:
            return

        items.pop(idx)

        if move_type == MenuTree.MoveType.MOVE_UP:
            idx -= 1
        else:
            idx += 1

        if idx < 0:
            idx = 0

        if idx > len(items):
            items.append(new_item)
        else:
            items.insert(idx, new_item)

    def find_parent(self, to_find: MenuItem) -> Optional[SubMenuItem]:
        """
        Finds the submenu that the provided object belongs to.
        :param to_find: the object to find sub menu for.
        :return: the submenu.
        """
        parent = None
        for menu_item, sub_menu_items in self._sub_menu_items.items():
            for item in sub_menu_items:
                if item.id == to_find.id:
                    parent = MenuItemHelper.as_sub_menu(menu_item)

        return parent

    def remove_menu_item(self, item: MenuItem, parent: Optional[SubMenuItem] = None):
        """
        Remove the menu item for the provided menu item in the provided sub menu.
        :param item: the item to remove (Search By ID).
        :param parent: the submenu to search.
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
        return set(self._sub_menu_items.keys())

    def get_menu_items(self, item: MenuItem) -> Optional[tuple[MenuItem]]:
        """
        Get a tuple of all menu items for a given submenu.
        :param item: the submenu to use.
        :return: a tuple of submenu items.
        """
        items = self._sub_menu_items.get(item)

        if items is None or len(items) == 0:
            return None

        return tuple(items)

    def get_all_menu_items(self) -> set[MenuItem]:
        """
        Gets every menu item held in this menu tree, will be unique.
        :return: every menu item in the tree.
        """
        to_return = set()
        subs: set[MenuItem] = self.get_all_sub_menus()
        for sub in subs:
            to_return.add(sub)
            items = self.get_menu_items(sub)
            if items is not None:
                to_return.update(self.get_menu_items(sub))

        return to_return

    def get_all_menu_items_from(self, item: SubMenuItem) -> tuple[MenuItem]:
        """
        Gets every menu item held in this menu tree from a given starting point, the starting point is a sub menu,
        from that submenu, this method will recurse through the rest of the menu structure and provide a complete list.
        The menu item provided itself will be the first item in the list, the rest will be in exact order as added.
        Use this method over get_all_menu_items() when the order is important, just call with `MenuTree.ROOT` to get all
        items in the tree.
        :param item: the starting point for traversal.
        :return: every menu item in the tree from the given starting point.
        """
        to_return: list[MenuItem] = []
        sub_items: list[MenuItem] = self._sub_menu_items[item]
        to_return.append(item)

        for item in sub_items:
            if item.has_children():
                to_return.extend(self.get_all_menu_items_from(MenuItemHelper.as_sub_menu(item)))
            else:
                to_return.append(item)

        return tuple(to_return)

    def change_item(self, item: MenuItem, menu_state: MenuState):
        """
        Change the value that's associated with a menu item. if you are changing
        a value, just send a command to the device, it will automatically update
        the tree.

        :param item: the item to change.
        :param menu_state: the new state.
        """

        # Add/update state only for items in the menu tree.
        # Note: Out of tree item with the same ID as an item inside tree
        # is considered to be the same item.
        if item.id not in set(map(lambda tree_item: tree_item.id, self.get_all_menu_items())):
            return

        self._menu_states[item.id] = menu_state

    def get_menu_state(self, item: MenuItem) -> Optional[MenuState]:
        """
        Gets the menu state that's associated with a given menu item. This is the
        current value for the menu item.
        :param item: the item which the state belongs to.
        :return: the state for the given menu item.
        """
        return self._menu_states.get(item.id)

    def initialize_state_for_each_item(self):
        """
        Initialize the state of each menu item to the default value, should be used during initialization of a local
        menu application. Will only take effect when there is no state already stored.
        """
        items: set[MenuItem] = self.get_all_menu_items()
        for item in items:
            if self.get_menu_state(item) is None:
                self.change_item(item, MenuItemHelper.state_for_menu_item(item, None, False, False))
