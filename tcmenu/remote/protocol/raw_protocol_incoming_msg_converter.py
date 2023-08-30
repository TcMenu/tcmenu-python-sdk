import io
from abc import ABC, abstractmethod

from tcmenu.remote.commands.menu_command import MenuCommand


class RawProtocolIncomingMsgConverter(ABC):
    @abstractmethod
    def apply(self, buffer: io.BytesIO, length: int) -> MenuCommand:
        raise NotImplementedError
