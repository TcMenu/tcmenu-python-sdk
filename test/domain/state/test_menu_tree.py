from tcmenu.domain.menu_items import AnalogMenuItem
from tcmenu.domain.state.menu_state import IntegerMenuState
from tcmenu.domain.state.menu_tree import MenuTree
from tcmenu.domain.util.menu_item_helper import MenuItemHelper
from test.domain.domain_fixtures import DomainFixtures

item1 = DomainFixtures.an_enum_item(name="Item1", item_id=1)
item2 = DomainFixtures.an_enum_item(name="Item2", item_id=2)
item3 = DomainFixtures.an_analog_item(name="Item3", item_id=3)
item_text = DomainFixtures.a_text_menu(name="ItemText", item_id=10)
sub_menu = DomainFixtures.a_sub_menu(name="Sub1", item_id=4)


def test_adding_items_then_removing():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    # if parent is not specified, it acts the same as ROOT
    menu_tree.add_menu_item(item=item2)

    assert len(menu_tree.get_menu_items(MenuTree.ROOT)) == 2

    menu_tree.remove_menu_item(parent=MenuTree.ROOT, item=item1)

    menu_items = menu_tree.get_menu_items(MenuTree.ROOT)
    assert len(menu_items) == 1
    assert menu_items[0] == item2


def test_that_removing_menu_item_removes_state():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.change_item(
        item1, MenuItemHelper.modify_existing_state_for_menu_item(menu_tree.get_menu_state(item1), item1, 1, True)
    )

    assert menu_tree.get_menu_state(item1) is not None

    menu_tree.remove_menu_item(parent=MenuTree.ROOT, item=item1)
    assert menu_tree.get_menu_state(item1) is None


def test_that_removing_works_by_id_only_as_per_docs():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    item1_same_id = MenuItemHelper.create_from_existing(
        item1, name="New Name", function_name="HelloThere", read_only=True
    )
    MenuItemHelper.set_menu_state(item1_same_id, 1, menu_tree)
    assert MenuItemHelper.get_value_for(item1_same_id, menu_tree, -1) == 1
    assert menu_tree.get_menu_by_id(item1.id) == item1_same_id

    menu_tree.remove_menu_item(parent=MenuTree.ROOT, item=item1_same_id)
    assert menu_tree.get_menu_by_id(item1.id) is None
    assert menu_tree.get_menu_by_id(item1_same_id.id) is None
    assert MenuItemHelper.get_value_for(item1_same_id, menu_tree, -1) == -1


def test_sub_menu_keys_are_created_and_removed():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    assert sub_menu in menu_tree.get_all_sub_menus()
    assert MenuTree.ROOT in menu_tree.get_all_sub_menus()

    menu_tree.add_menu_item(parent=sub_menu, item=item1)
    menu_tree.add_menu_item(parent=sub_menu, item=item2)

    assert menu_tree.get_menu_items(sub_menu) == (item1, item2)

    menu_tree.remove_menu_item(parent=sub_menu, item=item1)

    assert menu_tree.get_menu_items(sub_menu) == (item2,)

    menu_tree.remove_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    assert menu_tree.get_menu_items(sub_menu) is None


def test_manipulating_state():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.add_menu_item(parent=sub_menu, item=item3)

    menu_tree.change_item(item1, MenuItemHelper.state_for_menu_item(item1, 1, True, False))
    state = menu_tree.get_menu_state(item1)
    assert isinstance(state, IntegerMenuState)
    assert state.value == 1
    assert state.changed
    assert not state.active

    menu_tree.change_item(
        item3, MenuItemHelper.modify_existing_state_for_menu_item(menu_tree.get_menu_state(item3), item3, 1, False)
    )
    state_analog = menu_tree.get_menu_state(item3)
    assert isinstance(state_analog, IntegerMenuState)
    assert state_analog.value == 1
    assert not state_analog.changed
    assert not state_analog.active

    menu_tree.add_or_update_item(parent_id=MenuTree.ROOT.id, item=item_text)
    assert item_text in menu_tree.get_all_menu_items()

    menu_tree.change_item(
        item_text,
        MenuItemHelper.modify_existing_state_for_menu_item(menu_tree.get_menu_state(item_text), item_text, "Hello"),
    )
    assert menu_tree.get_menu_state(item_text) is not None
    assert menu_tree.get_menu_state(item_text).value == "Hello"


def test_replace_by_id():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=sub_menu, item=item1)

    item1_change = DomainFixtures.an_enum_item("Changed item1", 1)
    menu_tree.replace_menu_by_id(item1_change)

    assert len(menu_tree.get_menu_items(sub_menu)) == 1
    assert item1_change in menu_tree.get_menu_items(sub_menu)


def test_remove_where_parent_not_specified():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=sub_menu, item=item1)
    menu_tree.add_menu_item(parent=sub_menu, item=item2)

    assert menu_tree.get_menu_items(sub_menu) == (item1, item2)
    menu_tree.remove_menu_item(item2)
    assert menu_tree.get_menu_items(sub_menu) == (item1,)


def test_moving_items_around():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item2)

    menu_tree.move_item(parent=MenuTree.ROOT, new_item=item2, move_type=MenuTree.MoveType.MOVE_UP)
    assert menu_tree.get_menu_items(MenuTree.ROOT) == (item3, item2, item1)

    menu_tree.move_item(parent=MenuTree.ROOT, new_item=item3, move_type=MenuTree.MoveType.MOVE_DOWN)
    assert menu_tree.get_menu_items(MenuTree.ROOT) == (item2, item3, item1)

    menu_tree.move_item(parent=MenuTree.ROOT, new_item=item1, move_type=MenuTree.MoveType.MOVE_DOWN)
    assert menu_tree.get_menu_items(MenuTree.ROOT) == (item2, item3, item1)

    menu_tree.move_item(parent=MenuTree.ROOT, new_item=item2, move_type=MenuTree.MoveType.MOVE_UP)
    assert menu_tree.get_menu_items(MenuTree.ROOT) == (item2, item3, item1)

    menu_tree.move_item(parent=MenuTree.ROOT, new_item=item1, move_type=MenuTree.MoveType.MOVE_UP)
    assert menu_tree.get_menu_items(MenuTree.ROOT) == (item2, item1, item3)


def test_get_items_from_point():
    sub_sub_item = DomainFixtures.a_sub_menu("extra", 400)
    analog_sub_sub_item = DomainFixtures.an_analog_item("analogExtra", 401)
    enum_sub_sub_item = DomainFixtures.an_enum_item("enumExtra", 402)
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=sub_menu, item=item3)
    menu_tree.add_menu_item(parent=sub_menu, item=sub_sub_item)
    menu_tree.add_menu_item(parent=sub_menu, item=item2)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.add_menu_item(parent=sub_sub_item, item=analog_sub_sub_item)
    menu_tree.add_menu_item(parent=sub_sub_item, item=enum_sub_sub_item)

    assert menu_tree.get_all_menu_items_from(sub_menu) == (
        sub_menu,
        item3,
        sub_sub_item,
        analog_sub_sub_item,
        enum_sub_sub_item,
        item2,
    )


def test_get_all_items():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=sub_menu, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item2)

    assert menu_tree.get_all_menu_items() == {MenuTree.ROOT, sub_menu, item1, item2, item3}


def test_add_or_update_method():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)

    item1_replacement = DomainFixtures.an_analog_item("Replaced", 1)
    menu_tree.add_or_update_item(parent_id=MenuTree.ROOT.id, item=item1_replacement)

    item = menu_tree.get_menu_by_id(1)
    assert item.name == "Replaced"
    assert item.id == 1
    assert isinstance(item, AnalogMenuItem)

    menu_tree.add_or_update_item(parent_id=MenuTree.ROOT.id, item=item2)

    assert len(menu_tree.get_menu_items(MenuTree.ROOT)) == 3
    item = menu_tree.get_menu_by_id(item3.id)
    assert item == item3


def test_initialize_state_for_each_item():
    menu_tree = MenuTree()
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=sub_menu)
    menu_tree.add_menu_item(parent=sub_menu, item=item3)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item1)
    menu_tree.add_menu_item(parent=MenuTree.ROOT, item=item2)

    menu_tree.initialize_state_for_each_item()

    assert menu_tree.get_menu_state(item1)
    assert menu_tree.get_menu_state(item2)
    assert menu_tree.get_menu_state(item3)
    assert menu_tree.get_menu_state(sub_menu)
