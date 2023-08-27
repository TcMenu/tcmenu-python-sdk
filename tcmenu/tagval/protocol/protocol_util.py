from tcmenu.tagval.protocol.api_platform import ApiPlatform


class ProtocolUtil:
    """
    A few general helper methods to get the version and platform information to and from messages.
    """

    @staticmethod
    def get_module_version_code() -> int:
        """
        Gets the current version from the version properties file.
        :return: the current version as major * 100 + minor.
        """
        from tcmenu import __version__

        major, minor, patch = map(int, __version__.split("."))
        return major * 100 + minor

    @staticmethod
    def from_key_to_api_platform(key: int) -> ApiPlatform:
        return ApiPlatform.from_key(key)
