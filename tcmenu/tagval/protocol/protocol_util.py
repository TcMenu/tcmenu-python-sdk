from tcmenu.tagval.protocol.api_platform import ApiPlatform


class ProtocolUtil:
    """
    A few general helper methods to get the version and platform information to and from messages.
    """

    @staticmethod
    def get_version_from_properties() -> int:
        """
        Gets and caches the current version from the version properties file.
        :return: the current version as major * 100 + minor.
        """
        # TODO: Implement.
        return 100
