from tcmenu.domain.state.menu_tree import MenuTree
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
