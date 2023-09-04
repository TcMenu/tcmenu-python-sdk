from tcmenu.domain.edit_item_type import EditItemType


def test_enum_values():
    assert EditItemType.PLAIN_TEXT.value == 0
    assert EditItemType.IP_ADDRESS.value == 1
    assert EditItemType.TIME_24H.value == 2
    assert EditItemType.TIME_12H.value == 3
    assert EditItemType.TIME_24_HUNDREDS.value == 4
    assert EditItemType.GREGORIAN_DATE.value == 5
    assert EditItemType.TIME_DURATION_SECONDS.value == 6
    assert EditItemType.TIME_DURATION_HUNDREDS.value == 7
    assert EditItemType.TIME_24H_HHMM.value == 8
    assert EditItemType.TIME_12H_HHMM.value == 9


def test_edit_type_from_id():
    assert EditItemType.PLAIN_TEXT == EditItemType.from_id(0)
    assert EditItemType.IP_ADDRESS == EditItemType.from_id(1)
    assert EditItemType.TIME_24H == EditItemType.from_id(2)
    assert EditItemType.TIME_12H == EditItemType.from_id(3)
    assert EditItemType.TIME_24_HUNDREDS == EditItemType.from_id(4)
    assert EditItemType.GREGORIAN_DATE == EditItemType.from_id(5)
    assert EditItemType.TIME_DURATION_SECONDS == EditItemType.from_id(6)
    assert EditItemType.TIME_DURATION_HUNDREDS == EditItemType.from_id(7)
    assert EditItemType.TIME_24H_HHMM == EditItemType.from_id(8)
    assert EditItemType.TIME_12H_HHMM == EditItemType.from_id(9)
    assert EditItemType.PLAIN_TEXT == EditItemType.from_id(10)
    assert EditItemType.PLAIN_TEXT == EditItemType.from_id(100)
