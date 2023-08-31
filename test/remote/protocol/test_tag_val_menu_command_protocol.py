import io

from tcmenu.remote.protocol.command_protocol import CommandProtocol
from tcmenu.remote.protocol.configurable_protocol_converter import ConfigurableProtocolConverter
from tcmenu.remote.protocol.message_field import MessageField

protocol = ConfigurableProtocolConverter(include_default_processors=True)


def test_receive_join_command():
    # command = protocol.from_channel(
    #     to_buffer(
    #         MenuCommandType.JOIN.message_field,
    #         "NM=IoTdevice|UU=07cd8bc6-734d-43da-84e7-6084990becfc|US=987654321|VE=1223|PF=1|\u0002",
    #     )
    # )

    # assert type(command) is MenuJoinCommand
    # # noinspection PyTypeChecker
    # join: MenuJoinCommand = command
    # assert "07cd8bc6-734d-43da-84e7-6084990becfc" == str(join.app_uuid)
    # assert "IoTdevice" == join.my_name
    # assert 1223 == join.api_version
    # assert 987654321 == join
    # assert ApiPlatform.JAVA_API == join.platform
    # assert MenuCommandType.JOIN.message_field == join.command_type
    pass


def to_buffer(message_type: MessageField, s: str) -> io.BytesIO:
    buffer = io.BytesIO()
    buffer.write(CommandProtocol.TAG_VAL_PROTOCOL.protocol_num)
    buffer.write(message_type.high[0].encode("utf-8"))
    buffer.write(message_type.low[0].encode("utf-8"))
    buffer.write(s.encode("utf-8"))
    buffer.seek(0)  # Resetting the buffer's position to the beginning
    return buffer
