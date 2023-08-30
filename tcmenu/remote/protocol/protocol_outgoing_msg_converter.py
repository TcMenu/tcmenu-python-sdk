import io
from abc import ABC, abstractmethod

from tcmenu.remote.commands.menu_command import MenuCommand


class ProtocolOutgoingMsgConverter(ABC):
    @abstractmethod
    def apply(self, buffer: io.BytesIO, command: MenuCommand) -> None:
        raise NotImplementedError
