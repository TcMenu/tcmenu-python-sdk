from typing import Optional

from tcmenu.domain.menu_items import (
    MenuItem,
    AnalogMenuItem,
    BooleanMenuItem,
    EnumMenuItem,
    SubMenuItem,
    ActionMenuItem,
    RuntimeListMenuItem,
    CustomBuilderMenuItem,
    ScrollChoiceMenuItem,
    Rgb32MenuItem,
    EditableLargeNumberMenuItem,
    EditableTextMenuItem,
    FloatMenuItem,
)
from tcmenu.domain.state.menu_tree import MenuTree


class PersistedMenu:
    """
    Represents a persisted menu item, it has additional information needed to reconstitute the item at the right point
    in the tree, namely the parent_id, and also the type of menu item. This class is used by the JsonMenuItemSerializer
    to store menu items.
    :see: JsonMenuItemSerializer
    """

    class ItemTypes:
        ANALOG_PERSIST_TYPE: str = "analogItem"
        ENUM_PERSIST_TYPE: str = "enumItem"
        SUB_PERSIST_TYPE: str = "subMenu"
        ACTION_PERSIST_TYPE: str = "actionMenu"
        RUNTIME_LIST_PERSIST_TYPE: str = "runtimeList"
        CUSTOM_ITEM_PERSIST_TYPE: str = "customBuildItem"
        BOOLEAN_PERSIST_TYPE: str = "boolItem"
        TEXT_PERSIST_TYPE: str = "textItem"
        FLOAT_PERSIST_TYPE: str = "floatItem"
        RUNTIME_LARGE_NUM_PERSIST_TYPE: str = "largeNumItem"
        SCROLL_CHOICE_PERSIST_TYPE: str = "scrollItem"
        RGB32_COLOR_PERSIST_TYPE: str = "rgbItem"
        TCMENU_COPY_PREFIX: str = "tcMenuCopy:"

    def __init__(
        self,
        item: MenuItem,
        parent_id: Optional[int] = None,
        item_type: Optional[str] = None,
        default_value: Optional[str] = None,
    ):
        if parent_id is None:
            self.parent_id = MenuTree.ROOT.id
        else:
            self.parent_id: int = parent_id

        self.item: MenuItem = item

        if default_value is not None:
            self.default_value: str = str(default_value)
        else:
            self.default_value = None

        if item_type is not None:
            self.type = item_type
        else:
            if isinstance(item, AnalogMenuItem):
                self.type = PersistedMenu.ItemTypes.ANALOG_PERSIST_TYPE
            elif isinstance(item, BooleanMenuItem):
                self.type = PersistedMenu.ItemTypes.BOOLEAN_PERSIST_TYPE
            elif isinstance(item, EnumMenuItem):
                self.type = PersistedMenu.ItemTypes.ENUM_PERSIST_TYPE
            elif isinstance(item, SubMenuItem):
                self.type = PersistedMenu.ItemTypes.SUB_PERSIST_TYPE
            elif isinstance(item, ActionMenuItem):
                self.type = PersistedMenu.ItemTypes.ACTION_PERSIST_TYPE
            elif isinstance(item, RuntimeListMenuItem):
                self.type = PersistedMenu.ItemTypes.RUNTIME_LIST_PERSIST_TYPE
            elif isinstance(item, CustomBuilderMenuItem):
                self.type = PersistedMenu.ItemTypes.CUSTOM_ITEM_PERSIST_TYPE
            elif isinstance(item, ScrollChoiceMenuItem):
                self.type = PersistedMenu.ItemTypes.SCROLL_CHOICE_PERSIST_TYPE
            elif isinstance(item, Rgb32MenuItem):
                self.type = PersistedMenu.ItemTypes.RGB32_COLOR_PERSIST_TYPE
            elif isinstance(item, EditableLargeNumberMenuItem):
                self.type = PersistedMenu.ItemTypes.RUNTIME_LARGE_NUM_PERSIST_TYPE
            elif isinstance(item, EditableTextMenuItem):
                self.type = PersistedMenu.ItemTypes.TEXT_PERSIST_TYPE
            elif isinstance(item, FloatMenuItem):
                self.type = PersistedMenu.ItemTypes.FLOAT_PERSIST_TYPE
