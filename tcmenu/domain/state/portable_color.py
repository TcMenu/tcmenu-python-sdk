from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PortableColor:
    """
    A portable color that represents a color in the RGBA space with single byte values for each entry (between 0..255).
    It can convert to and from web color format strings.
    """

    red: int
    green: int
    blue: int
    alpha: int = 255

    @staticmethod
    def from_html(html_code: str) -> PortableColor:
        """
        Create a color object from a web color code such as #FFFFFF
        :param: html_code the html code
        """
        if html_code[0] == "#" and len(html_code) == 4:
            red = int(html_code[1], 16) << 4
            green = int(html_code[2], 16) << 4
            blue = int(html_code[3], 16) << 4
            return PortableColor(red, green, blue)
        elif html_code[0] == "#" and len(html_code) >= 7:
            red = int(html_code[1:3], 16)
            green = int(html_code[3:5], 16)
            blue = int(html_code[5:7], 16)
            alpha = 255

            if len(html_code) == 9:
                alpha = int(html_code[7:9], 16)

            return PortableColor(red, green, blue, alpha)
        else:
            return PortableColor(red=0, green=0, blue=0, alpha=255)

    def __str__(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}{self.alpha:02X}"
