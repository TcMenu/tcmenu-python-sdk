from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import (
    AnalogMenuItem,
    MenuItem,
    EnumMenuItem,
    EditableTextMenuItem,
    SubMenuItem,
    FloatMenuItem,
    RuntimeListMenuItem,
    BooleanMenuItem,
    ActionMenuItem,
    Rgb32MenuItem,
    CustomBuilderMenuItem,
    ScrollChoiceMenuItem,
)
from test.domain.domain_fixtures import DomainFixtures


def test_analog_menu_item():
    item: AnalogMenuItem = AnalogMenuItem(
        name="Test Menu",
        variable_name="TestMenu",
        id=10,
        eeprom_address=100,
        function_name="someFn",
        divisor=2,
        offset=-20,
        unit_name="dB",
        read_only=True,
        local_only=True,
        step=2,
        max_value=10000,
    )

    assert_base_menu_fields(item=item, name="Test Menu", item_id=10, eeprom=100)
    assert item.divisor == 2
    assert item.step == 2
    assert item.offset == -20
    assert item.unit_name == "dB"
    assert item.max_value == 10000
    assert item.function_name == "someFn"
    assert item.variable_name == "TestMenu"
    assert item.read_only
    assert item.local_only
    assert item.visible
    assert not item.has_children()


def test_enum_menu_item():
    item: EnumMenuItem = EnumMenuItem(
        name="Enum Menu",
        id=20,
        eeprom_address=102,
        enum_entries=["Enum1"],
        function_name="someFn",
        variable_name="Menu123",
        visible=False,
    )

    assert_base_menu_fields(item=item, name="Enum Menu", item_id=20, eeprom=102)
    assert "Enum1" in item.enum_entries
    assert not item.has_children()
    assert not item.read_only
    assert not item.local_only
    assert not item.visible
    assert item.function_name == "someFn"
    assert item.variable_name == "Menu123"


def test_text_menu_item():
    item: EditableTextMenuItem = EditableTextMenuItem(
        name="Test",
        text_length=10,
        eeprom_address=-1,
        id=1,
        read_only=False,
        local_only=False,
        visible=False,
        item_type=EditItemType.IP_ADDRESS,
        function_name="abc",
    )

    assert_base_menu_fields(item=item, name="Test", item_id=1, eeprom=-1)
    assert item.text_length == 10
    assert not item.has_children()
    assert not item.read_only
    assert not item.local_only
    assert not item.visible
    assert item.item_type == EditItemType.IP_ADDRESS


def test_sub_menu_item():
    item: SubMenuItem = SubMenuItem(
        name="SomeName", id=30, eeprom_address=104, function_name="shouldntBeUsed", local_only=True
    )

    assert_base_menu_fields(item=item, name="SomeName", item_id=30, eeprom=104)
    assert item.has_children()
    assert item.function_name is None
    assert item.local_only
    assert item.visible


def test_float_menu_item():
    item: FloatMenuItem = FloatMenuItem(name="Flt", id=33, eeprom_address=-1, num_decimal_places=3)

    assert_base_menu_fields(item=item, name="Flt", item_id=33, eeprom=-1)
    assert item.num_decimal_places == 3


def test_list_menu_item():
    item: RuntimeListMenuItem = RuntimeListMenuItem(
        name="runList", id=2909, eeprom_address=-1, function_name="runListFn"
    )

    assert_base_menu_fields(item=item, name="runList", item_id=2909, eeprom=-1)
    assert item.function_name == "runListFn"
    assert item.initial_rows == 0


def test_boolean_menu_item():
    item: BooleanMenuItem = DomainFixtures.a_boolean_menu(
        name="Bool1", item_id=22, naming=BooleanMenuItem.BooleanNaming.TRUE_FALSE
    )

    assert_base_menu_fields(item=item, name="Bool1", item_id=22, eeprom=102)
    assert not item.has_children()
    assert item.naming == BooleanMenuItem.BooleanNaming.TRUE_FALSE


def test_action_menu_item():
    item: ActionMenuItem = DomainFixtures.an_action_menu(name="Act1", item_id=448)

    assert_base_menu_fields(item=item, name="Act1", item_id=448, eeprom=20)
    assert not item.has_children()


def test_rgb32_menu_item():
    item: Rgb32MenuItem = Rgb32MenuItem(
        name="rgb",
        id=102,
        eeprom_address=-1,
        function_name="test",
        local_only=True,
        read_only=True,
        include_alpha_channel=True,
    )

    assert_base_menu_fields(item=item, name="rgb", item_id=102, eeprom=-1)
    assert item.local_only
    assert item.read_only
    assert item.include_alpha_channel


def test_custom_builder_menu_item():
    item: CustomBuilderMenuItem = CustomBuilderMenuItem(
        name="Test12",
        id=123,
        menu_type=CustomBuilderMenuItem.CustomMenuType.REMOTE_IOT_MONITOR,
        function_name="myFunc",
        local_only=True,
        read_only=False,
        visible=False,
        eeprom_address=-1,
    )

    assert_base_menu_fields(item=item, name="Test12", item_id=123, eeprom=-1)
    assert item.local_only
    assert not item.read_only
    assert not item.visible
    assert item.menu_type == CustomBuilderMenuItem.CustomMenuType.REMOTE_IOT_MONITOR


def test_scroll_choice_menu_item():
    item: ScrollChoiceMenuItem = ScrollChoiceMenuItem(
        name="scroll",
        id=123,
        function_name="onScroll",
        eeprom_address=202,
        read_only=True,
        item_width=10,
        num_entries=20,
        choice_mode=ScrollChoiceMenuItem.ScrollChoiceMode.ARRAY_IN_RAM,
        variable_name="hello",
        eeprom_offset=80,
    )

    assert_base_menu_fields(item=item, name="scroll", item_id=123, eeprom=202)
    assert not item.local_only
    assert item.read_only
    assert item.visible
    assert item.function_name == "onScroll"
    assert item.variable_name == "hello"
    assert item.item_width == 10
    assert item.num_entries == 20
    assert item.eeprom_offset == 80


def assert_base_menu_fields(item: MenuItem, name: str, item_id: int, eeprom: int):
    assert name == item.name
    assert item_id == item.id
    assert eeprom == item.eeprom_address
