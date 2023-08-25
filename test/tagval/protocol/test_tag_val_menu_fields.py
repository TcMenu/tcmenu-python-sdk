from tcmenu.tagval.protocol.tag_val_menu_fields import TagValMenuFields


def test_enum_fields_length():
    for field in TagValMenuFields:
        # Fields having prepend in their name have the second char appended later.
        # Check whether the const has at least 1 character.
        if "prepend" in field.name.lower():
            assert len(field.value) >= 1, f"{field.name} value should be at least length 1"
        else:
            assert len(field.value) == 2, f"{field.name} value should be of length 2"


def test_enum_fields_not_start_with_digit():
    for field in TagValMenuFields:
        assert not field.value[0].isdigit(), f"{field.name} value should not start with a digit"
