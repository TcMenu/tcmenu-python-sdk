from abc import ABC, abstractmethod

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser


class TagValProtocolIncomingMsgConverter(ABC):
    @abstractmethod
    def apply(self, parser: TagValTextParser) -> MenuCommand:
        raise NotImplementedError
