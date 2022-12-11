from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition


def test_scroll_position():
    pos1 = CurrentScrollPosition(10, "ABC")
    pos2 = CurrentScrollPosition.from_text("20-Another Super-Duper")
    pos3 = CurrentScrollPosition.from_text("ABC")  # not valid but shouldn't fail
    pos4 = CurrentScrollPosition.from_text("a-ABC")  # not valid but shouldn't fail
    pos5 = CurrentScrollPosition.from_text("252-")

    assert pos1.position == 10
    assert pos1.value == "ABC"

    assert pos2.position == 20
    assert pos2.value == "Another Super-Duper"

    assert pos5.position == 252
    assert pos5.value == ""
    pos5.value = "987654321"

    assert pos2 == CurrentScrollPosition.from_text("20-Another Super-Duper")
    assert not pos2 == CurrentScrollPosition.from_text("10-Another Super-Duper")
    assert not pos2 == CurrentScrollPosition.from_text("20-Another Duper")

    assert str(pos1) == "10-ABC"
    assert str(pos2) == "20-Another Super-Duper"
    assert str(pos3) == "0-Unknown"
    assert str(pos4) == "0-ABC"
    assert str(pos5) == "252-987654321"
