class VersionInfo:
    """
    This class represents a version number in standard form, such as 1.2.3, it can parse from text and determine which
    is the newer of two versions.
    """

    def __init__(self, version: str):
        ver_split: list[str] = version.split(".")
        if len(ver_split) < 2:
            self._major = 0
            self._minor = 0
            self._patch = 0
        else:
            self._major = int(ver_split[0])
            self._minor = int(ver_split[1])

            if len(ver_split) == 3:
                self._patch = int(ver_split[2])
            else:
                self._patch = 0

    # noinspection PyProtectedMember
    def is_same_or_newer_than(self, other: "VersionInfo"):
        if self._major > other._major:
            return True

        if self._major < other._major:
            return False

        if self._minor > other._minor:
            return True

        if self._minor < other._minor:
            return False

        return self._patch >= other._patch

    def __repr__(self):
        return f"{self._major}.{self._minor}.{self._patch}"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __int__(self):
        return self._major * 1000000 + self._minor * 1000 + self._patch


VersionInfo.ERROR_VERSION = VersionInfo("0.0.0")
