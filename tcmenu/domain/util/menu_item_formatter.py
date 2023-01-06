from typing import Any

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
        pass

    @staticmethod
    def format_editable_text_to_wire() -> str:
        pass

    @staticmethod
    def format_large_num_to_wire() -> str:
        pass

    @staticmethod
    def format_scroll_item_to_wire() -> str:
        pass

    @staticmethod
    def format_bool_to_wire() -> str:
        pass

    @staticmethod
    def format_enum_to_wire() -> str:
        pass

    @staticmethod
    def format_analog_to_wire() -> str:
        pass

    @staticmethod
    def get_actual_decimal_divisor(divisor: int) -> int:
        pass

    @staticmethod
    def format_for_display(item: MenuItem, data: Any) -> str:
        pass

    @staticmethod
    def format_scroll_item_for_display(item: ScrollChoiceMenuItem, data: CurrentScrollPosition) -> str:
        pass

    @staticmethod
    def format_rgb_item_for_display(item: Rgb32MenuItem, data: PortableColor) -> str:
        pass

    @staticmethod
    def format_text_for_display(item: Rgb32MenuItem, data: PortableColor) -> str:
        pass

    @staticmethod
    def format_large_num_for_display(item: EditableLargeNumberMenuItem, data: int) -> str:
        pass

    @staticmethod
    def format_enum_for_display(item: EnumMenuItem, data: int) -> str:
        pass

    @staticmethod
    def format_bool_for_display(item: BooleanMenuItem, data: bool) -> str:
        pass

    @staticmethod
    def format_analog_for_display(item: AnalogMenuItem, data: int) -> str:
        pass

    @staticmethod
    def format_float_for_display(item: FloatMenuItem, data: float) -> str:
        pass

    @staticmethod
    def calculate_required_digits(divisor: int) -> int:
        pass
