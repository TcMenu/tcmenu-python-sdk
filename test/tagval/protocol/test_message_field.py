import pytest

from tcmenu.tagval.protocol.message_field import MessageField


def test_message_field():
    MessageField._ALL_FIELDS_MAP.clear()
    message = MessageField("R", "V")

    assert message.first_byte is "R"
    assert message.second_byte is "V"
    assert message.high is "R"
    assert message.low is "V"
    assert message.id == "RV"
    assert str(message) == "Field[RV]"


def test_message_field_duplicate_entry():
    MessageField._ALL_FIELDS_MAP.clear()
    MessageField("A", "A")

    with pytest.raises(ValueError):
        MessageField("A", "A")


def test_message_from_id():
    MessageField._ALL_FIELDS_MAP.clear()
    MessageField("A", "A")

    message = MessageField.from_id("AA")

    assert isinstance(message, MessageField)
    assert message.id == "AA"

    # Invalid message
    with pytest.raises(ValueError):
        MessageField.from_id("AB")
