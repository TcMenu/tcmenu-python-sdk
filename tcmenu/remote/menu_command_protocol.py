import io
from abc import ABC, abstractmethod

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.protocol.command_protocol import CommandProtocol


class MenuCommandProtocol(ABC):
    """
    This is a low-level part of the API that most people don't need to deal with. Implementations will translate
    commands to and from a given protocol. If you want to add custom messages then see the configurable protocol
    converter implementation from ConfigurableProtocolConverter.
    """

    PROTO_START_OF_MSG: bytes = b"\x01"
    PROTO_END_OF_MSG: bytes = b"\x02"

    @abstractmethod
    def from_channel(self, buffer: io.BytesIO) -> MenuCommand:
        """
        Retrieves a message from the channel, or raises an exception if the message is not fully formed.
        It is assumed that the buffer has been suitably flipped ready for reading.
        """
        pass

    @abstractmethod
    def to_channel(self, buffer: io.BytesIO, cmd: MenuCommand) -> None:
        """
        Puts the command specified into the byte buffer, it is assumed that the callee will flip the
        channel once complete.

        Parameters:
            - buffer: to write the data to
            - cmd: the command to write
        """
        pass

    @abstractmethod
    def get_protocol_for_cmd(self, command: MenuCommand) -> CommandProtocol:
        """
        Checks the message and sees which protocol it will be processed with. For example, the JOIN message would be
        processed using TagVal.

        Parameters:
            - command: the command to check the protocol of

        Returns:
            the protocol that will be used.
        """
        pass
