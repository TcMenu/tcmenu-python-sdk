from dataclasses import dataclass
from enum import Enum
from typing import Any

from tcmenu.domain.menu_items import MenuItem


@dataclass
class MenuState:
    class StateStorageType(Enum):
        """
        Represents the storage type for the state.
        """

        INTEGER = 0
        BOOLEAN = 1
        FLOAT = 2
        STRING = 3
        STRING_LIST = 4
        SCROLL_POSITION = 5
        PORTABLE_COLOR = 6
        BIG_DECIMAL = 7

    """Changed status."""
    changed: bool

    """Active status."""
    active: bool

    """Menu item associated with this state."""
    item: MenuItem

    """Current value."""
    value: Any

    """
    The storage type for this state, e.g., if it is a MenuState specialized for Integer,
    then the state type will be INTEGER.
    """
    storage_type: StateStorageType


@dataclass
class BigDecimalMenuState(MenuState):
    """
    Used to store the decimal state of large number menu item in the menu tree.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.BIG_DECIMAL


@dataclass
class BooleanMenuState(MenuState):
    """
    An implementation of menu state for booleans. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.BOOLEAN


@dataclass
class CurrentScrollPositionMenuState(MenuState):
    """
    An implementation of menu state for scroll positions. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.SCROLL_POSITION


@dataclass
class FloatMenuState(MenuState):
    """
    An implementation of menu state for float values. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.FLOAT


@dataclass
class IntegerMenuState(MenuState):
    """
    An implementation of menu state for integer values. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.INTEGER


@dataclass
class PortableColorMenuState(MenuState):
    """
    An implementation of menu state for portable colors. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.PORTABLE_COLOR


@dataclass
class StringListMenuState(MenuState):
    """
    An implementation of menu state for lists of strings. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.STRING_LIST


@dataclass
class StringMenuState(MenuState):
    """
    An implementation of menu state for strings. This stores the current value in the MenuTree for an item.
    Generally it's best to work with state via tcmenu.domain.util.MenuItemHelper.
    """

    storage_type: MenuState.StateStorageType = MenuState.StateStorageType.STRING
