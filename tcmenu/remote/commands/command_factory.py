from typing import Optional
from uuid import UUID

from tcmenu.remote.commands.menu_commands import MenuJoinCommand
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.protocol_util import ProtocolUtil


class CommandFactory:
    """
    These static helper methods are the preferred way to create command message that can be sent and received from
    a remote connection. Each protocol can convert sent and received messages into this form.
    """

    @staticmethod
    def new_join_command(name: str, uuid: Optional[UUID] = None) -> MenuJoinCommand:
        """
        Create a new join command. You can either provide a fixed UUID
        or a random UUID will be generated for you.

        :param name: the name that the remote will show for the connection.
        :param uuid: optional; the UUID that identifies our client.
        :return: join command.
        """
        if not uuid:
            return MenuJoinCommand(my_name=name, platform=ApiPlatform.PYTHON_API,
                                   api_version=ProtocolUtil.get_version_from_properties())
        else:
            return MenuJoinCommand(my_name=name, platform=ApiPlatform.PYTHON_API,
                                   api_version=ProtocolUtil.get_version_from_properties(), app_uuid=uuid)
