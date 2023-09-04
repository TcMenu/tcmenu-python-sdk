import io
import logging
from typing import Type, Callable, Dict, Union, TypeVar, Generic

from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.menu_command_protocol import MenuCommandProtocol
from tcmenu.remote.protocol.command_protocol import CommandProtocol
from tcmenu.remote.protocol.message_field import MessageField

from tcmenu.remote.protocol.tag_val_menu_command_processors import TagValMenuCommandProcessors
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser
from tcmenu.remote.protocol.tc_protocol_exception import TcProtocolException


T = TypeVar("T", bound=MenuCommand)


class ConfigurableProtocolConverter(MenuCommandProtocol):
    """
    An implementation of the menu command protocol interface that is configurable. By default, it can
    create all the regular tag value message processors so that regular embedCONTROL messages can be
    parsed and written. It is also possible to add extra command handlers for both TagVal protocol
    and also for binary format.
    """

    def __init__(self, include_default_processors=False):
        self._tag_val_incoming_parsers: Dict[MessageField, Callable[[TagValTextParser], Generic[T]]] = {}
        self._tag_val_output_writers: Dict[MessageField, Callable[[io.StringIO, Generic[T]], None]] = {}
        self._raw_incoming_parsers: Dict[MessageField, Callable[[io.BytesIO, int], Generic[T]]] = {}
        self._raw_output_writers: Dict[MessageField, Callable[[io.BytesIO, Generic[T]], None]] = {}

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
        self, field: MessageField, processor: Callable[[io.StringIO, Generic[T]], None], clazz: Type[MenuCommand]
    ):
        """
        This method adds a tag value message processor that can convert a MenuCommand
        into the appropriate wire format for sending.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(buffer: io.StringIO, command: MenuCommand) -> None
        :param clazz: the specific message class.
        """
        self._tag_val_output_writers[field] = self._output_msg_converter_with_type(processor, clazz)

    def add_raw_in_processor(self, field, processor):
        """
        This method adds a binary message processor that can convert an incoming wire message into a
        command. In this case the processor will take a byte buffer and length of the message in the buffer, it should
        convert this into a MenuCommand.

        :param field: the message type to convert.
        :param processor: a conversion function with the following signature:
        func(buffer: io.BytesIO, length: int) -> Type[MenuCommand]
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
        self._raw_output_writers[field] = self._output_msg_converter_with_type(processor, clazz)

    def from_channel(self, buffer: io.BytesIO) -> Generic[T]:
        proto_id = buffer.read(1)[0]
        protocol = CommandProtocol.from_protocol_id(proto_id)

        msg_type = self._get_msg_type_from_buffer(buffer)
        cmd_type = MessageField.from_id(msg_type)

        if not cmd_type:
            raise TcProtocolException(f"Received unexpected message: {msg_type}")

        if protocol == CommandProtocol.TAG_VAL_PROTOCOL and cmd_type in self._tag_val_incoming_parsers:
            parser = TagValTextParser(buffer)
            logging.debug(f"Protocol convert in: {parser}")
            return self._tag_val_incoming_parsers[cmd_type](parser)
        elif protocol.value == CommandProtocol.RAW_BIN_PROTOCOL and cmd_type in self._raw_incoming_parsers:
            length = int.from_bytes(buffer.read(4), byteorder="big")
            return self._raw_incoming_parsers[cmd_type](buffer, length)
        else:
            raise TcProtocolException(f"Unknown protocol used in message: {protocol.name}")

    def to_channel(self, buffer: io.BytesIO, command: Generic[T]) -> None:
        raw_processor = self._raw_output_writers.get(command.command_type)

        if raw_processor:
            self._write_standard_header(buffer, command, CommandProtocol.RAW_BIN_PROTOCOL)
            raw_processor(buffer, command)
        elif command.command_type in self._tag_val_output_writers:
            tag_writer = self._tag_val_output_writers.get(command.command_type)
            self._write_standard_header(buffer, command, CommandProtocol.TAG_VAL_PROTOCOL)
            string_buffer = io.StringIO()
            tag_writer(string_buffer, command)
            buffer.write(string_buffer.getvalue().encode("utf-8"))
            buffer.write(b"\x02")
        else:
            raise TcProtocolException(f"Message not processed: {command.command_type}")

    def get_protocol_for_cmd(self, command: Generic[T]) -> CommandProtocol:
        return (
            CommandProtocol.TAG_VAL_PROTOCOL
            if command.command_type in self._tag_val_output_writers
            else CommandProtocol.RAW_BIN_PROTOCOL
        )

    @staticmethod
    def _write_standard_header(buffer: io.BytesIO, command: Generic[T], protocol: CommandProtocol) -> None:
        buffer.write(MenuCommandProtocol.PROTO_START_OF_MSG)
        buffer.write(protocol.protocol_num)
        buffer.write(command.command_type.high[0].encode("utf-8"))
        buffer.write(command.command_type.low[0].encode("utf-8"))

    @staticmethod
    def _get_msg_type_from_buffer(buffer: io.BytesIO) -> str:
        char1 = buffer.read(1).decode()
        char2 = buffer.read(1).decode()

        return char1 + char2

    @staticmethod
    def _output_msg_converter_with_type(
        processor: Union[Callable[[io.StringIO, Generic[T]], None], Callable[[io.BytesIO, Generic[T]], None]],
        the_clazz: Type[MenuCommand],
    ):
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

        def apply(buffer: Union[io.StringIO, io.BytesIO], command: Generic[T]):
            if type(command) is not the_clazz:
                raise ValueError("Wrong type of command provided")
            processor(buffer, command)

        return apply
