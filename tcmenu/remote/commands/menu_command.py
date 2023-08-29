from abc import ABC, abstractmethod

from tcmenu.remote.protocol.message_field import MessageField


class MenuCommand(ABC):
    """
    Classes extending from MenuCommand can be sent and received on a connector. They are protocol
    neutral in order to make replacing the protocol as easy as possible.
    """

    @property
    @abstractmethod
    def command_type(self) -> MessageField:
        """
        The type of message received.
        :return: the command type
        """
        pass
