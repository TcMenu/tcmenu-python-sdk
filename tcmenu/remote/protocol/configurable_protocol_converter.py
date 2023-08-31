import io
import logging
from typing import Any, Type, Callable, Dict, Union

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.menu_command_protocol import MenuCommandProtocol
from tcmenu.remote.protocol.command_protocol import CommandProtocol
from tcmenu.remote.protocol.message_field import MessageField
from tcmenu.remote.protocol.tag_val_menu_command_processors import TagValMenuCommandProcessors
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser


class ConfigurableProtocolConverter(MenuCommandProtocol):
    """
    An implementation of the menu command protocol interface that is configurable. By default, it can
    create all the regular tag value message processors so that regular embedCONTROL messages can be
    parsed and written. It is also possible to add extra command handlers for both TagVal protocol
    and also for binary format.
    """

    def __init__(self, include_default_processors=False):
        self._tag_val_incoming_parsers: Dict[MessageField, Callable[[TagValTextParser], MenuCommand]] = {}
        self._tag_val_output_writers: Dict[MessageField, ConfigurableProtocolConverter.OutputMsgConverterWithType] = {}
        self._raw_incoming_parsers: Dict[MessageField, Callable[[io.BytesIO, int], None]] = {}
        self._raw_output_writers: Dict[MessageField, ConfigurableProtocolConverter.OutputMsgConverterWithType] = {}

        if include_default_processors:
            tag_val_processors = TagValMenuCommandProcessors()
            tag_val_processors.add_handlers_to_protocol(self)

    def add_tag_val_in_processor(self, field: MessageField, processor: Callable[[TagValTextParser], MenuCommand]):
        """
        This method adds a tag value message processor that can convert an incoming wire message into a
        command. In this case the processor will take a TagValTextParser and convert that into a
        MenuCommand.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(parser: TagValTextParser) -> Type[MenuCommand]
        """
        self._tag_val_incoming_parsers[field] = processor

    def add_tag_val_out_processor(
        self, field: MessageField, processor: Callable[[io.StringIO, MenuCommand], None], clazz: Type[MenuCommand]
    ):
        """
        This method adds a tag value message processor that can convert a MenuCommand
        into the appropriate wire format for sending.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(buffer: io.StringIO, command: MenuCommand) -> None
        :param clazz: the specific message class.
        """
        self._tag_val_output_writers[field] = self.OutputMsgConverterWithType(processor, clazz)

    def add_raw_in_processor(self, field, processor):
        """
        This method adds a binary message processor that can convert an incoming wire message into a
        command. In this case the processor will take a byte buffer and length of the message in the buffer, it should
        convert this into a MenuCommand.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(buffer: io.BytesIO, length: int) -> MenuCommand
        """
        self._raw_incoming_parsers[field] = processor

    def add_raw_out_processor(self, field, processor, clazz):
        """
        This method adds a binary message processor that can convert a MenuCommand
        into the binary wire format; you must write 4 bytes containing the length first.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(buffer: io.BytesIO, command: MenuCommand) -> None
        :param clazz: the specific message class.
        """
        self._raw_output_writers[field] = self.OutputMsgConverterWithType(processor, clazz)

    def from_channel(self, buffer: io.BytesIO) -> MenuCommand:
        pass

    def to_channel(self, buffer: io.BytesIO, cmd: MenuCommand) -> None:
        pass

    def get_protocol_for_cmd(self, command: MenuCommand) -> CommandProtocol:
        pass

    class OutputMsgConverterWithType:
        """
        Converts MenuCommand into the appropriate wire format for sending.
        Note that unlike the input message processors we do additional type checking
        to make sure we're converting valid messages. Input processors just expect
        valid messages on the wire.

        :param processor: a conversion function with one of the following signatures:
        func(buffer: io.StringIO, command: MenuCommand) -> None for the TagVal protocol -or-
        func(buffer: io.BytesIO, command: MenuCommand) -> None for the raw protocol.
        :param the_clazz: Expected menu command class to process. If user tries to convert
        any other MenuCommand instance, we will raise an error.
        """

        def __init__(
            self,
            processor: Union[Callable[[io.StringIO, MenuCommand], None], Callable[[io.BytesIO, MenuCommand], None]],
            the_clazz: Type[MenuCommand],
        ):
            self._processor = processor
            self._the_clazz = the_clazz

        def apply(self, buffer, cmd: Any):
            if type(cmd) is not self._the_clazz:
                raise ValueError("Wrong type of command provided")
            self._processor(buffer, cmd)
