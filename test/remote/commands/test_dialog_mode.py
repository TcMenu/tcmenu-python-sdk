from tcmenu.remote.commands.dialog_mode import DialogMode


def test_enum_values():
    assert DialogMode.SHOW
    assert DialogMode.HIDE
    assert DialogMode.ACTION


def test_enum_uniqueness():
    values = [mode.value for mode in DialogMode]
    assert len(values) == len(set(values)), "Enum values are not unique"
