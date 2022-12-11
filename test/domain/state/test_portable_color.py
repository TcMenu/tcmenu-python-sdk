from tcmenu.domain.state.portable_color import PortableColor


def test_portable_color():
    color_alpha = PortableColor(128, 255, 127, 32)
    color_no_alpha = PortableColor(100, 200, 50)
    color_rgb4 = PortableColor.from_html("#f3b")
    color_rgb7 = PortableColor.from_html("#23f503")
    color_rgb9 = PortableColor.from_html("#365498aa")

    assert color_alpha == PortableColor(128, 255, 127, 32)
    assert not color_alpha == PortableColor(128, 255, 127, 2)
    assert not color_alpha == PortableColor(128, 255, 12, 32)
    assert not color_alpha == PortableColor(128, 25, 12, 32)
    assert not color_alpha == PortableColor(18, 255, 12, 32)

    assert_color(color_alpha, 128, 255, 127, 32, "#80FF7F20")
    assert_color(color_no_alpha, 100, 200, 50, 255, "#64C832FF")
    assert_color(color_rgb4, 0xF0, 0x30, 0xB0, 255, "#F030B0FF")
    assert_color(color_rgb7, 0x23, 0xF5, 0x03, 255, "#23F503FF")
    assert_color(color_rgb9, 0x36, 0x54, 0x98, 0xAA, "#365498AA")


def assert_color(color_to_test: PortableColor, red: int, green: int, blue: int, alpha: int, to_str: str):
    assert color_to_test.red == red
    assert color_to_test.green == green
    assert color_to_test.blue == blue
    assert color_to_test.alpha == alpha
    assert str(color_to_test) == to_str
