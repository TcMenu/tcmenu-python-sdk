from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from tcmenu.domain.edit_item_type import EditItemType


@dataclass(frozen=True)
class MenuItem:
    """
    The base class for all menu items, has the most basic operations
    available on it that are needed by pretty much all menu items.
    """

    """name of the menu item"""
    name: str = ""

    """variable name that should be used during generation"""
    variable_name: Optional[str] = None

    """ID for the menu item"""
    id: int = -1

    """eeprom storage address for this item; -1 indicates no storage"""
    eeprom_address: int = -1

    """function name for this item"""
    function_name: Optional[str] = None

    """read only status of this menu item"""
    read_only: bool = False

    """if this menu item is only for local viewing and not to be sent remotely"""
    local_only: bool = False

    """this flag indicates if the item should be visible on the UI"""
    visible: bool = True

    def has_children(self) -> bool:
        """
        This method indicates if this item can contain child items.
        :return: true, if the item can contain child items
        """
        return False


@dataclass(frozen=True)
class ActionMenuItem(MenuItem):
    """
    ActionMenuItem represents a menu item that is a one shot action, in that when triggered it
    just runs the callback on the embedded side.
    """

    pass


@dataclass(frozen=True)
class AnalogMenuItem(MenuItem):
    """
    Represents an analog (numeric) menu item, it is always a zero based integer when retrieved from storage, but it can
    have an offset and divisor, so therefore is able to represent decimal values. The offset can also be negative. Step
    allows the rate of change to be greater than 1 unit, but must be an exact divisor of the maximum value.
    Rather than directly constructing an item of this type, you can use the AnalogMenuItemBuilder.
    """

    """The maximum value (0 based integer) that this item can represent"""
    max_value: int = -1

    """The offset from 0 that is used when displaying the item, can be negative"""
    offset: int = -1

    """The divisor used when displaying the item, for example value 50 with a divisor of 10 is 5.0"""
    divisor: int = -1

    """
    The unit name to appear directly after the value, for example a temperature item may be "oC"
    where as a volume control could be "dB"
    :return: the name of the unit (if any)
    """
    unit_name: str = ""

    """
    The step is the amount by which each increment should increase the value,
    it must be exactly divisible by the maximum value. Default is 1 and
    the value can never be lower than 1.
    """
    step: int = 1


@dataclass(frozen=True)
class BooleanMenuItem(MenuItem):
    """
    A menu item that can only hold boolean values (true or false). The naming can be changed such that the boolean can
    be represented with different text.
    """

    # noinspection PyArgumentList
    class BooleanNaming(Enum):
        TRUE_FALSE = 0
        ON_OFF = 1
        YES_NO = 2
        CHECKBOX = 3

        @staticmethod
        def from_id(item_id: int):
            return (
                BooleanMenuItem.BooleanNaming(item_id)
                if item_id in (item.value for item in BooleanMenuItem.BooleanNaming)
                else BooleanMenuItem.BooleanNaming.TRUE_FALSE
            )

    """the naming for this boolean, that describes how to render the true/false choice."""
    naming: BooleanNaming = BooleanNaming.ON_OFF


@dataclass(frozen=True)
class CustomBuilderMenuItem(MenuItem):
    """
    This is a custom menu item that can be created by the designer, but does not directly represent a different item
    in the API. For example, the Remote management menu item and the authentication menu item. They are just regular
    lists when sent remotely.

    IMPORTANT: This menu type is a design time only type, it must never be sent to a tagval.
    """

    # noinspection PyArgumentList
    class CustomMenuType(Enum):
        AUTHENTICATION = auto()
        REMOTE_IOT_MONITOR = auto()

    """the naming for this boolean, that describes how to render the true/false choice."""
    menu_type: CustomMenuType = CustomMenuType.AUTHENTICATION


@dataclass(frozen=True)
class EditableLargeNumberMenuItem(MenuItem):
    """
    A menu item that corresponds to the large number type on the device. These numeric values are generally
    large enough that they should be stored as big decimals. They have a maximum number of digits and a
    fixed number of decimal places. They can be positive or negative, although you can prevent negative values
    by setting negativeAllowed to false.
    """

    digits_allowed: int = 0
    decimal_places: int = 0
    negative_allowed: bool = False


@dataclass(frozen=True)
class EditableTextMenuItem(MenuItem):
    """
    An implementation of menu item that can store text strings. Currently, they are always stored in RAM on the Arduino
    so choose the size carefully.
    """

    """The maximum length allowable."""
    text_length: int = 0

    """The type of values that can be represented by this control."""
    item_type: EditItemType = EditItemType.PLAIN_TEXT


@dataclass(frozen=True)
class EnumMenuItem(MenuItem):
    """
    A menu item implementation that represents one of a known set of choices, the choices are stored as an integer
    value, but each choice has a string representation as well.
    """

    enum_entries: tuple[str, ...] = tuple()


@dataclass(frozen=True)
class FloatMenuItem(MenuItem):
    """
    FloatMenuItem represents a menu item that uses a floating point value. It is not editable on the device
    because it does not really represent absolute values, but is sometimes useful for conveying status.
    """

    num_decimal_places: int = 0


@dataclass(frozen=True)
class Rgb32MenuItem(MenuItem):
    """
    A menu item that represents a color in the RGB domain with optional Alpha channel. It is represented using a
    PortableColor
    :see: tcmenu.domain.state.portable_color
    """

    include_alpha_channel: bool = False


@dataclass(frozen=True)
class RuntimeListMenuItem(MenuItem):
    initial_rows: int = 0


@dataclass(frozen=True)
class ScrollChoiceMenuItem(MenuItem):
    """
    Represents a more configurable and more extensible version of enum that should be used when the number of choices is
    larger, the choices are in eeprom, or you need more control at runtime of the choices.
    """

    # noinspection PyArgumentList
    class ScrollChoiceMode(Enum):
        ARRAY_IN_EEPROM = auto()
        ARRAY_IN_RAM = auto()
        CUSTOM_RENDERFN = auto()

    item_width: int = 0
    eeprom_offset: int = 0
    num_entries: int = 0
    choice_mode: ScrollChoiceMode = ScrollChoiceMode.ARRAY_IN_EEPROM
    variable: Optional[str] = None


@dataclass(frozen=True)
class SubMenuItem(MenuItem):
    """
    SubMenuItem represents a menu item that has children. To get the child items call the MenuTree
    methods that interact with items.
    """

    secured: bool = False

    @property
    def function_name(self) -> Optional[str]:
        return None

    @function_name.setter
    def function_name(self, value):
        pass

    def has_children(self) -> bool:
        """
        :return: True; submenu's always have children.
        """
        return True
