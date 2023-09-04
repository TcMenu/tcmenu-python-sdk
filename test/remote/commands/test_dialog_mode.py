from tcmenu.remote.commands.dialog_mode import DialogMode


def test_enum_values():
    assert DialogMode.SHOW
    assert DialogMode.HIDE
    assert DialogMode.ACTION


def test_enum_uniqueness():
    values = [mode.value for mode in DialogMode]
    assert len(values) == len(set(values)), "Enum values are not unique"


def test_dialog_mode_from_string():
    assert DialogMode.SHOW == DialogMode.from_string("S")
    assert DialogMode.HIDE == DialogMode.from_string("H")
    assert DialogMode.ACTION == DialogMode.from_string("")
    assert DialogMode.ACTION == DialogMode.from_string("AA")
