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
