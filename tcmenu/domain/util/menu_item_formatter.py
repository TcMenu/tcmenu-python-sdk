from typing import Any, Optional
import re

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    MenuItem,
    ScrollChoiceMenuItem,
    Rgb32MenuItem,
    EditableTextMenuItem,
    EditableLargeNumberMenuItem,
    EnumMenuItem,
    BooleanMenuItem,
    AnalogMenuItem,
    FloatMenuItem,
)
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.portable_color import PortableColor


class MenuItemFormatter:
    @staticmethod
    def format_to_wire(item: MenuItem, text: str) -> str:
        if isinstance(item, AnalogMenuItem):
            return MenuItemFormatter._format_analog_to_wire(text)
        elif isinstance(item, EnumMenuItem):
            return MenuItemFormatter._format_enum_to_wire(text)
        elif isinstance(item, BooleanMenuItem):
            return MenuItemFormatter._format_bool_to_wire(text)
        elif isinstance(item, EditableLargeNumberMenuItem):
            return MenuItemFormatter._format_large_num_to_wire(text)
        elif isinstance(item, Rgb32MenuItem):
            return MenuItemFormatter._format_rgb_item_to_wire(text)
        elif isinstance(item, ScrollChoiceMenuItem):
            return MenuItemFormatter._format_scroll_item_to_wire(text)
        elif isinstance(item, EditableTextMenuItem):
            return MenuItemFormatter._format_editable_text_to_wire(item, text)
        else:
            raise ValueError(f"Item {item.name} is not editable.")

    @staticmethod
    def _format_editable_text_to_wire(item: EditableTextMenuItem, text: str) -> str:
        if item.item_type == EditItemType.PLAIN_TEXT and len(text) < item.text_length:
            return text
        elif item.item_type == EditItemType.IP_ADDRESS:
            return "0.0.0.0" if not re.match("\\d+\\.\\d+\\.\\d+\\.\\d+", text) else text
        elif (
            item.item_type == EditItemType.TIME_24H
            or item.item_type == EditItemType.TIME_24_HUNDREDS
            or item.item_type == EditItemType.TIME_12H
        ):
            # Time is always sent back to the server in 24-hour format. It is always possible
            # (but optional) to provide hundreds/sec.
            return "12:00:00" if not re.match("\\d+:\\d+:\\d+(.\\d*)*", text) else text
        elif item.item_type == EditItemType.GREGORIAN_DATE:
            return "01/01/2000" if not re.match("\\d+/\\d+/\\d+", text) else text
        else:
            return ""

    @staticmethod
    def _format_large_num_to_wire(text: str) -> str:
        try:
            val = int(text)
        except ValueError:
            val = 0

        return str(val)

    @staticmethod
    def _format_rgb_item_to_wire(text: str) -> str:
        return str(PortableColor.from_html(text))

    @staticmethod
    def _format_scroll_item_to_wire(text: str) -> str:
        try:
            val = int(text)
        except ValueError:
            val = 0

        return str(CurrentScrollPosition(val, text))

    @staticmethod
    def _format_bool_to_wire(text: str) -> str:
        text = text.upper()

        if text == "ON" or text == "YES" or text == "TRUE":
            return "1"
        else:
            return "0"

    @staticmethod
    def _format_enum_to_wire(text: str) -> str:
        return text

    @staticmethod
    def _format_analog_to_wire(text: str) -> str:
        return text

    @staticmethod
    def _get_actual_decimal_divisor(divisor: int) -> int:
        if divisor < 2:
            return 1
        elif divisor > 1000:
            return 10000
        elif divisor > 100:
            return 1000
        elif divisor > 10:
            return 100
        else:
            return 10

    @staticmethod
    def format_for_display(item: Optional[MenuItem] = None, data: Optional[Any] = None) -> str:
        if item is None or data is None:
            return ""
        elif isinstance(item, FloatMenuItem):
            return MenuItemFormatter._format_float_for_display(item, data)
        elif isinstance(item, AnalogMenuItem):
            return MenuItemFormatter._format_analog_for_display(item, data)
        elif isinstance(item, BooleanMenuItem):
            return MenuItemFormatter._format_bool_for_display(item, data)
        elif isinstance(item, EnumMenuItem):
            return MenuItemFormatter._format_enum_for_display(item, data)
        elif isinstance(item, EditableLargeNumberMenuItem):
            return MenuItemFormatter._format_large_num_for_display(data)
        elif isinstance(item, EditableTextMenuItem):
            return MenuItemFormatter._format_text_for_display(data)
        elif isinstance(item, Rgb32MenuItem):
            return MenuItemFormatter._format_rgb_item_for_display(data)
        elif isinstance(item, ScrollChoiceMenuItem):
            return MenuItemFormatter._format_scroll_item_for_display(data)
        else:
            return ""

    @staticmethod
    def _format_scroll_item_for_display(data: CurrentScrollPosition) -> str:
        return data.value

    @staticmethod
    def _format_rgb_item_for_display(data: PortableColor) -> str:
        return str(data)

    @staticmethod
    def _format_text_for_display(data: str) -> str:
        return data

    @staticmethod
    def _format_large_num_for_display(data: int) -> str:
        return str(data)

    @staticmethod
    def _format_enum_for_display(item: EnumMenuItem, data: int) -> str:
        if len(item.enum_entries) > data:
            return item.enum_entries[data]

        return ""

    @staticmethod
    def _format_bool_for_display(item: BooleanMenuItem, data: bool) -> str:
        if item.naming == BooleanMenuItem.BooleanNaming.ON_OFF:
            return "On" if data else "Off"
        elif item.naming == BooleanMenuItem.BooleanNaming.YES_NO:
            return "Yes" if data else "No"
        elif item.naming == BooleanMenuItem.BooleanNaming.TRUE_FALSE:
            return "True" if data else "False"

    @staticmethod
    def _format_analog_for_display(item: AnalogMenuItem, data: int) -> str:
        calc_val: int = data + item.offset
        divisor: int = item.divisor

        if divisor < 2:
            return f"{calc_val}{item.unit_name}"
        else:
            whole: int = int(calc_val / divisor)
            fract_max: int = MenuItemFormatter._get_actual_decimal_divisor(item.divisor)
            fraction: int = int(abs(calc_val % divisor) * (fract_max / divisor))

            return f"{whole}.{fraction:0{MenuItemFormatter._calculate_required_digits(divisor)}}{item.unit_name}"

    @staticmethod
    def _format_float_for_display(item: FloatMenuItem, data: float) -> str:
        return f"{data:.{item.num_decimal_places}f}"

    @staticmethod
    def _calculate_required_digits(divisor: int) -> int:
        if divisor <= 10:
            return 1
        elif divisor <= 100:
            return 2
        elif divisor <= 1000:
            return 3
        else:
            return 4
