from tcmenu.remote.commands.menu_button_type import MenuButtonType


def test_button_set():
    button = MenuButtonType.OK
    assert type(button.button_name) == str
    assert len(button.button_name) > 0
    assert type(button.type_value) == int


def test_button_not_set():
    button = MenuButtonType.NONE
    assert type(button.button_name) == str
    assert len(button.button_name) == 0
    assert type(button.type_value) == int


def test_button_type_from_id():
    assert MenuButtonType.OK == MenuButtonType.from_id(0)
    assert MenuButtonType.ACCEPT == MenuButtonType.from_id(1)
    assert MenuButtonType.CANCEL == MenuButtonType.from_id(2)
    assert MenuButtonType.CLOSE == MenuButtonType.from_id(3)
    assert MenuButtonType.NONE == MenuButtonType.from_id(4)
    assert MenuButtonType.NONE == MenuButtonType.from_id(5)
    assert MenuButtonType.NONE == MenuButtonType.from_id(100)
