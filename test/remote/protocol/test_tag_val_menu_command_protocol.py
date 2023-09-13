import io
import struct
import uuid
from dataclasses import replace, dataclass
from typing import Generic, TypeVar, ClassVar

import pytest

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import BooleanMenuItem, FloatMenuItem, Rgb32MenuItem, ScrollChoiceMenuItem
from tcmenu.domain.state.current_scroll_position import CurrentScrollPosition
from tcmenu.domain.state.list_response import ListResponse
from tcmenu.domain.state.portable_color import PortableColor
from tcmenu.remote.commands.ack_status import AckStatus
from tcmenu.remote.commands.command_factory import CommandFactory
from tcmenu.remote.commands.dialog_mode import DialogMode
from tcmenu.remote.commands.menu_acknowledgement_command import MenuAcknowledgementCommand
from tcmenu.remote.commands.menu_boot_commands import (
    MenuAnalogBootCommand,
    MenuFloatBootCommand,
    MenuRuntimeListBootCommand,
    MenuTextBootCommand,
    MenuEnumBootCommand,
    MenuLargeNumBootCommand,
    MenuSubBootCommand,
    MenuRgb32BootCommand,
    MenuScrollChoiceBootCommand,
    MenuActionBootCommand,
    MenuBooleanBootCommand,
)
from tcmenu.remote.commands.menu_bootstrap_command import MenuBootstrapCommand
from tcmenu.remote.commands.menu_button_type import MenuButtonType
from tcmenu.remote.commands.menu_change_command import MenuChangeCommand
from tcmenu.remote.commands.menu_command import MenuCommand
from tcmenu.remote.commands.menu_command_type import MenuCommandType
from tcmenu.remote.commands.menu_dialog_command import MenuDialogCommand
from tcmenu.remote.commands.menu_heartbeat_command import MenuHeartbeatCommand
from tcmenu.remote.commands.menu_join_command import MenuJoinCommand
from tcmenu.remote.commands.menu_pairing_command import MenuPairingCommand
from tcmenu.remote.menu_command_protocol import MenuCommandProtocol
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.command_protocol import CommandProtocol
from tcmenu.remote.protocol.configurable_protocol_converter import ConfigurableProtocolConverter
from tcmenu.remote.protocol.correlation_id import CorrelationId
from tcmenu.remote.protocol.message_field import MessageField
from tcmenu.remote.protocol.tag_val_menu_command_processors import TagValMenuCommandProcessors
from tcmenu.remote.protocol.tag_val_text_parser import TagValTextParser
from test.domain.domain_fixtures import DomainFixtures

protocol = ConfigurableProtocolConverter(include_default_processors=True)


# Custom spanner command to test serialization and deserialization of a user-defined command.
@dataclass(frozen=True)
class MenuSpannerCommand(MenuCommand):
    SPANNER_MSG_TYPE: ClassVar[MessageField] = MessageField("S", "Z")

    metric_size: int

    make: str

    @property
    def command_type(self) -> MessageField:
        return MenuSpannerCommand.SPANNER_MSG_TYPE


def process_spanner_command(parser: TagValTextParser) -> MenuSpannerCommand:
    return MenuSpannerCommand(metric_size=parser.get_value_as_int("ZA"), make=parser.get_value("ZB"))


# noinspection PyProtectedMember
def write_spanner_command(buffer: io.StringIO, command: MenuSpannerCommand) -> None:
    TagValMenuCommandProcessors._append_field(buffer, "ZA", command.metric_size)
    TagValMenuCommandProcessors._append_field(buffer, "ZB", command.make)


protocol.add_tag_val_in_processor(field=MenuSpannerCommand.SPANNER_MSG_TYPE, processor=process_spanner_command)
protocol.add_tag_val_out_processor(
    field=MenuSpannerCommand.SPANNER_MSG_TYPE, processor=write_spanner_command, clazz=MenuSpannerCommand
)


# Custom raw bin data serialization and deserialization.
@dataclass(frozen=True)
class BinaryDataCommand(MenuCommand):
    BIN_DATA_COMMAND: ClassVar[MessageField] = MessageField("S", "B")

    bin_data: bytes

    @property
    def command_type(self) -> MessageField:
        return BinaryDataCommand.BIN_DATA_COMMAND


def process_raw_bin_data(buffer: io.BytesIO, length: int) -> BinaryDataCommand:
    data: bytes = buffer.read(length)
    return BinaryDataCommand(bin_data=data)


def write_raw_bin_data(buffer: io.BytesIO, command: BinaryDataCommand) -> None:
    bin_data = command.bin_data
    length = len(bin_data)

    # Write the length of the binary data as an integer to the buffer
    buffer.write(struct.pack(">I", length))

    # Write the binary data itself
    buffer.write(bin_data)


protocol.add_raw_in_processor(field=BinaryDataCommand.BIN_DATA_COMMAND, processor=process_raw_bin_data)
protocol.add_raw_out_processor(
    field=BinaryDataCommand.BIN_DATA_COMMAND, processor=write_raw_bin_data, clazz=BinaryDataCommand
)


def test_receive_join_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.JOIN.message_field,
            "NM=IoTdevice|UU=07cd8bc6-734d-43da-84e7-6084990becfc|US=987654321|VE=1223|PF=1|\u0002",
        )
    )

    assert type(command) is MenuJoinCommand
    join: MenuJoinCommand = command
    assert "07cd8bc6-734d-43da-84e7-6084990becfc" == str(join.app_uuid)
    assert "IoTdevice" == join.my_name
    assert 1223 == join.api_version
    assert 987654321 == join.serial_number
    assert ApiPlatform.JAVA_API == join.platform
    assert MenuCommandType.JOIN.message_field == join.command_type


def test_receive_join_command_with_no_uuid_and_sn():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.JOIN.message_field,
            "NM=IoTdevice|VE=1223|PF=1|\u0002",
        )
    )

    assert type(command) is MenuJoinCommand
    join: MenuJoinCommand = command
    assert isinstance(join.app_uuid, uuid.UUID)
    assert "IoTdevice" == join.my_name
    assert 1223 == join.api_version
    assert 0 == join.serial_number
    assert ApiPlatform.JAVA_API == join.platform
    assert MenuCommandType.JOIN.message_field == join.command_type


def test_receive_dialog_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.DIALOG_UPDATE.message_field,
            "MO=S|HF=Hello\\||BU=Buffer\\=|B1=0|B2=4|\u0002",
        )
    )

    assert type(command) is MenuDialogCommand
    dlg: MenuDialogCommand = command
    assert DialogMode.SHOW == dlg.dialog_mode
    assert "Hello|" == dlg.header
    assert "Buffer=" == dlg.buffer
    assert MenuButtonType.OK, dlg.button1
    assert MenuButtonType.NONE, dlg.button2


def test_receive_heartbeat_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.HEARTBEAT.message_field,
            "\u0002",
        )
    )

    assert type(command) is MenuHeartbeatCommand
    hb: MenuHeartbeatCommand = command
    assert MenuCommandType.HEARTBEAT.message_field == hb.command_type
    assert hb.mode == MenuHeartbeatCommand.HeartbeatMode.NORMAL
    assert hb.heartbeat_interval == 10000


def test_receive_bootstrap_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOTSTRAP.message_field,
            "BT=START|\u0002",
        )
    )
    _check_bootstrap_fields(command, MenuBootstrapCommand.BootType.START)

    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOTSTRAP.message_field,
            "BT=END|\u0002",
        )
    )
    _check_bootstrap_fields(command, MenuBootstrapCommand.BootType.END)


T = TypeVar("T", bound=MenuCommand)


def _check_bootstrap_fields(command: Generic[T], boot_type: MenuBootstrapCommand.BootType):
    assert type(command) is MenuBootstrapCommand
    bs: MenuBootstrapCommand = command
    assert boot_type == bs.boot_type
    assert MenuCommandType.BOOTSTRAP.message_field == bs.command_type


def test_receive_analog_item_no_step():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ANALOG_BOOT_ITEM.message_field,
            "PI=321|ID=1|RO=1|VI=1|AM=255|AO=-180|AD=2|AU=dB|NM=Volume|VC=22|\u0002",
        )
    )

    assert type(command) is MenuAnalogBootCommand
    analog: MenuAnalogBootCommand = command
    assert -180 == analog.menu_item.offset
    assert 255 == analog.menu_item.max_value
    assert 2 == analog.menu_item.divisor
    assert "dB" == analog.menu_item.unit_name
    assert 1 == analog.menu_item.id
    assert 1 == analog.menu_item.step
    assert "Volume" == analog.menu_item.name
    assert 321 == analog.sub_menu_id
    assert analog.menu_item.read_only is True
    assert analog.menu_item.visible is True


def test_receive_analog_item_with_step():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ANALOG_BOOT_ITEM.message_field,
            "PI=321|ID=1|RO=1|VI=1|AM=255|AO=-180|AD=2|AU=dB|AS=2|NM=Volume|VC=22|\u0002",
        )
    )

    assert type(command) is MenuAnalogBootCommand
    analog: MenuAnalogBootCommand = command
    assert -180 == analog.menu_item.offset
    assert 255 == analog.menu_item.max_value
    assert 2 == analog.menu_item.divisor
    assert "dB" == analog.menu_item.unit_name
    assert 1 == analog.menu_item.id
    assert 2 == analog.menu_item.step
    assert "Volume" == analog.menu_item.name
    assert 321 == analog.sub_menu_id
    assert analog.menu_item.read_only is True
    assert analog.menu_item.visible is True


def test_receive_float_boot_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.FLOAT_BOOT_ITEM.message_field,
            "PI=2|RO=1|VI=0|NM=menuName|ID=1|FD=5|VC=12.3456|\u0002",
        )
    )

    assert type(command) is MenuFloatBootCommand
    float_cmd: MenuFloatBootCommand = command

    epsilon = 1e-5
    assert abs(12.3456 - float_cmd.current_value) < epsilon

    assert 5 == float_cmd.menu_item.num_decimal_places
    assert "menuName" == float_cmd.menu_item.name
    assert 1 == float_cmd.menu_item.id
    assert 2 == float_cmd.sub_menu_id
    assert float_cmd.menu_item.read_only is True
    assert float_cmd.menu_item.visible is False


def test_receive_runtime_list_boot_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.RUNTIME_LIST_BOOT.message_field,
            "PI=2|RO=1|VI=1|NM=runList|ID=1|NC=3|CA=abc|CB=def|CC=ghi|\u0002",
        )
    )

    assert type(command) is MenuRuntimeListBootCommand
    runtime_list_cmd: MenuRuntimeListBootCommand = command
    assert "runList" == runtime_list_cmd.menu_item.name
    assert 1 == runtime_list_cmd.menu_item.id
    assert 2 == runtime_list_cmd.sub_menu_id
    assert 3 == len(runtime_list_cmd.current_value)
    assert "abc" == runtime_list_cmd.current_value[0]
    assert "def" == runtime_list_cmd.current_value[1]
    assert "ghi" == runtime_list_cmd.current_value[2]
    assert runtime_list_cmd.menu_item.read_only is True
    assert runtime_list_cmd.menu_item.visible is True


def test_receive_text_boot_command():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.TEXT_BOOT_ITEM.message_field,
            "PI=2|RO=0|VI=0|NM=menuName|ID=1|ML=10|EM=1|VC=12345678|\u0002",
        )
    )

    assert type(command) is MenuTextBootCommand
    text_cmd: MenuTextBootCommand = command
    assert MenuCommandType.TEXT_BOOT_ITEM.message_field == text_cmd.command_type
    assert "12345678" == text_cmd.current_value
    assert 10 == text_cmd.menu_item.text_length
    assert "menuName" == text_cmd.menu_item.name
    assert EditItemType.IP_ADDRESS == text_cmd.menu_item.item_type
    assert 1 == text_cmd.menu_item.id
    assert 2 == text_cmd.sub_menu_id
    assert text_cmd.menu_item.read_only is False
    assert text_cmd.menu_item.visible is False


def test_receive_text_boot_command_invalid_edit_mode():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.TEXT_BOOT_ITEM.message_field,
            "PI=2|RO=0|NM=menuName|ID=1|ML=10|EM=99999|VC=12345678|\u0002",
        )
    )

    assert type(command) is MenuTextBootCommand
    text_cmd: MenuTextBootCommand = command
    assert MenuCommandType.TEXT_BOOT_ITEM.message_field == text_cmd.command_type

    # The edit mode in the message was corrupt, should be set to plain text by default.
    assert EditItemType.PLAIN_TEXT == text_cmd.menu_item.item_type


def test_receive_enum_item():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ENUM_BOOT_ITEM.message_field,
            "PI=42|RO=1|ID=21|NM=Choices|NC=3|CA=Choice1|CB=Choice2|CC=Choice3|VC=2|\u0002",
        )
    )

    assert type(command) is MenuEnumBootCommand
    enum_cmd: MenuEnumBootCommand = command
    assert 21 == enum_cmd.menu_item.id
    assert "Choices" == enum_cmd.menu_item.name
    assert 42 == enum_cmd.sub_menu_id
    assert enum_cmd.menu_item.enum_entries == ("Choice1", "Choice2", "Choice3")
    assert enum_cmd.menu_item.read_only is True
    assert enum_cmd.menu_item.visible is True


def test_receive_large_number_negative_default():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.LARGE_NUM_BOOT_ITEM.message_field,
            "PI=10|ID=111|IE=64|NM=largeNum|RO=0|FD=4|ML=12|VC=11.1[2]34|\u0002",
        )
    )

    assert type(command) is MenuLargeNumBootCommand
    large_num_cmd: MenuLargeNumBootCommand = command
    assert 111 == large_num_cmd.menu_item.id
    assert "largeNum" == large_num_cmd.menu_item.name
    assert 10 == large_num_cmd.sub_menu_id
    assert 4 == large_num_cmd.menu_item.decimal_places
    assert 12 == large_num_cmd.menu_item.digits_allowed
    assert 64 == large_num_cmd.menu_item.eeprom_address

    epsilon = 1e-5
    assert abs(11.1234 - large_num_cmd.current_value) < epsilon
    assert large_num_cmd.menu_item.negative_allowed is True
    assert large_num_cmd.menu_item.read_only is False
    assert large_num_cmd.menu_item.visible is True


def test_receive_large_number():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.LARGE_NUM_BOOT_ITEM.message_field,
            "PI=10|ID=111|IE=64|NM=largeNum|RO=0|FD=4|NA=0|ML=12|VC=11.1[2]34|\u0002",
        )
    )

    assert type(command) is MenuLargeNumBootCommand
    large_num_cmd: MenuLargeNumBootCommand = command
    assert 111 == large_num_cmd.menu_item.id
    assert "largeNum" == large_num_cmd.menu_item.name
    assert 10 == large_num_cmd.sub_menu_id
    assert 4 == large_num_cmd.menu_item.decimal_places
    assert 12 == large_num_cmd.menu_item.digits_allowed

    epsilon = 1e-5
    assert abs(11.1234 - large_num_cmd.current_value) < epsilon
    assert large_num_cmd.menu_item.negative_allowed is False
    assert large_num_cmd.menu_item.read_only is False
    assert large_num_cmd.menu_item.visible is True


def test_receive_sub_menu_item():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.SUBMENU_BOOT_ITEM.message_field,
            "RO=0|PI=0|ID=1|NM=SubMenu|\u0002",
        )
    )

    assert type(command) is MenuSubBootCommand
    sub_menu: MenuSubBootCommand = command
    assert 1 == sub_menu.menu_item.id
    assert "SubMenu" == sub_menu.menu_item.name
    assert 0 == sub_menu.sub_menu_id
    assert sub_menu.menu_item.read_only is False
    assert sub_menu.menu_item.visible is True


def test_receive_rgb32_item():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOT_RGB_COLOR.message_field,
            "RO=0|PI=0|ID=1|NM=rgb|RA=1|VC=#22334455|\u0002",
        )
    )

    assert type(command) is MenuRgb32BootCommand
    rgb: MenuRgb32BootCommand = command
    assert 1 == rgb.menu_item.id
    assert "rgb" == rgb.menu_item.name
    assert 0 == rgb.sub_menu_id
    assert rgb.menu_item.include_alpha_channel is True
    assert rgb.menu_item.read_only is False
    assert rgb.menu_item.visible is True


def test_receive_scroll_choice():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOT_SCROLL_CHOICE.message_field,
            "RO=0|PI=0|ID=1|NM=scroll|WI=10|NC=20|VC=1-hello|\u0002",
        )
    )

    assert type(command) is MenuScrollChoiceBootCommand
    scroll_choice: MenuScrollChoiceBootCommand = command
    assert 1 == scroll_choice.menu_item.id
    assert "scroll" == scroll_choice.menu_item.name
    assert 0 == scroll_choice.sub_menu_id
    assert 10 == scroll_choice.menu_item.item_width
    assert 20 == scroll_choice.menu_item.num_entries
    assert 1 == scroll_choice.current_value.position
    assert "hello" == scroll_choice.current_value.value
    assert scroll_choice.menu_item.read_only is False
    assert scroll_choice.menu_item.visible is True


def test_receive_action_menu_item():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACTION_BOOT_ITEM.message_field,
            "RO=0|PI=0|ID=1|NM=Action|\u0002",
        )
    )

    assert type(command) is MenuActionBootCommand
    action_cmd: MenuActionBootCommand = command
    assert 1 == action_cmd.menu_item.id
    assert "Action" == action_cmd.menu_item.name
    assert 0 == action_cmd.sub_menu_id
    assert action_cmd.menu_item.read_only is False
    assert action_cmd.menu_item.visible is True


def test_receive_boolean_menu_item():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field,
            "PI=0|RO=1|VI=1|ID=1|BN=1|NM=BoolItem|VC=1|\u0002",
        )
    )
    check_boolean_cmd_fields(command, True, BooleanMenuItem.BooleanNaming.ON_OFF)

    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field,
            "PI=0|RO=1|VI=1|ID=1|BN=0|NM=BoolItem|VC=0|\u0002",
        )
    )
    check_boolean_cmd_fields(command, False, BooleanMenuItem.BooleanNaming.TRUE_FALSE)

    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field,
            "PI=0|ID=1|RO=1|VI=1|BN=2|NM=BoolItem|VC=0|\u0002",
        )
    )
    check_boolean_cmd_fields(command, False, BooleanMenuItem.BooleanNaming.YES_NO)

    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.BOOLEAN_BOOT_ITEM.message_field,
            "PI=0|ID=1|RO=1|VI=1|BN=3|NM=BoolItem|VC=0|\u0002",
        )
    )
    check_boolean_cmd_fields(command, False, BooleanMenuItem.BooleanNaming.CHECKBOX)


def check_boolean_cmd_fields(command: MenuBooleanBootCommand, current: bool, naming: BooleanMenuItem.BooleanNaming):
    assert type(command) is MenuBooleanBootCommand
    bool_cmd: MenuBooleanBootCommand = command
    assert 1 == bool_cmd.menu_item.id
    assert "BoolItem" == bool_cmd.menu_item.name
    assert 0 == bool_cmd.sub_menu_id
    assert current == bool_cmd.current_value
    assert naming == bool_cmd.menu_item.naming
    assert bool_cmd.menu_item.read_only is True
    assert bool_cmd.menu_item.visible is True


def test_receive_pairing():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.PAIRING_REQUEST.message_field,
            "NM=someUI|UU=575d327e-fe76-4e68-b0b8-45eea154a126|\u0002",
        )
    )

    assert type(command) is MenuPairingCommand
    pairing: MenuPairingCommand = command
    assert "someUI" == pairing.name
    assert "575d327e-fe76-4e68-b0b8-45eea154a126" == str(pairing.uuid)


def test_receive_acknowledgement_cases():
    # Success.
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            "IC=FDE05CAD|ST=0",
        )
    )
    check_ack_fields(command, AckStatus.SUCCESS)
    assert AckStatus.SUCCESS.is_error() is False

    # Warning.
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            "IC=FDE05CAD|ST=-1",
        )
    )
    check_ack_fields(command, AckStatus.VALUE_RANGE_WARNING)
    assert AckStatus.VALUE_RANGE_WARNING.is_error() is False

    # ID not found.
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            "IC=FDE05CAD|ST=1",
        )
    )
    check_ack_fields(command, AckStatus.ID_NOT_FOUND)
    assert AckStatus.ID_NOT_FOUND.is_error() is True

    # Bad login ID.
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            "IC=FDE05CAD|ST=2",
        )
    )
    check_ack_fields(command, AckStatus.INVALID_CREDENTIALS)
    assert AckStatus.INVALID_CREDENTIALS.is_error() is True

    # Unknown error.
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.ACKNOWLEDGEMENT.message_field,
            "IC=FDE05CAD|ST=222",
        )
    )
    check_ack_fields(command, AckStatus.UNKNOWN_ERROR)
    assert AckStatus.UNKNOWN_ERROR.is_error() is True


def check_ack_fields(command: MenuAcknowledgementCommand, status: AckStatus):
    assert type(command) is MenuAcknowledgementCommand
    ack: MenuAcknowledgementCommand = command
    assert "fde05cad" == str(ack.correlation_id)
    assert status == ack.ack_status


def test_receive_delta_change():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.CHANGE_INT_FIELD.message_field,
            "IC=CA039424|ID=22|TC=0|VC=1|\u0002",
        )
    )
    verify_change_fields(command, MenuChangeCommand.ChangeType.DELTA, 1)


def test_receive_list_status_change():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.CHANGE_INT_FIELD.message_field,
            "IC=CA039424|ID=22|TC=3|VC=109:1|\u0002",
        )
    )
    assert type(command) is MenuChangeCommand
    change_command: MenuChangeCommand = command
    assert MenuCommandType.CHANGE_INT_FIELD.value, change_command.command_type
    assert MenuChangeCommand.ChangeType.LIST_STATE_CHANGE == change_command.change_type
    assert "109:1" == change_command.value


def test_receive_absolute_change():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.CHANGE_INT_FIELD.message_field,
            "IC=ca039424|ID=22|TC=1|VC=-10000|\u0002",
        )
    )
    verify_change_fields(command, MenuChangeCommand.ChangeType.ABSOLUTE, -10000)


def test_receive_list_change():
    command = protocol.from_channel(
        to_buffer(
            MenuCommandType.CHANGE_INT_FIELD.message_field,
            "IC=ca039424|ID=22|TC=2|NC=2|cA=R1|CA=123|cB=R2|CB=456|\u0002",
        )
    )
    assert type(command) is MenuChangeCommand
    change_command: MenuChangeCommand = command
    assert MenuCommandType.CHANGE_INT_FIELD.value, change_command.command_type
    assert "ca039424" == str(change_command.correlation_id)
    assert 22 == change_command.menu_item_id
    assert MenuChangeCommand.ChangeType.ABSOLUTE_LIST == change_command.change_type
    assert set(change_command.value) == {"R1\t123", "R2\t456"}


def test_unknown_message_raises_exception():
    bb = io.BytesIO(b"??~")

    with pytest.raises(ValueError):
        protocol.from_channel(bb)


def verify_change_fields(command: MenuChangeCommand, change_type: MenuChangeCommand.ChangeType, value: int):
    assert type(command) is MenuChangeCommand
    change_command: MenuChangeCommand = command

    assert change_type == change_command.change_type
    assert value == int(change_command.value)
    assert 22 == change_command.menu_item_id
    assert MenuCommandType.CHANGE_INT_FIELD.value, change_command.command_type
    assert "ca039424" == str(change_command.correlation_id)


def test_write_heartbeat():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_heartbeat_command(frequency=10000, mode=MenuHeartbeatCommand.HeartbeatMode.NORMAL),
    )
    compare_buffer_against_expected(out_buffer, MenuCommandType.HEARTBEAT.value, "HI=10000|HR=0|\u0002")


def test_write_join():
    out_buffer = io.BytesIO()
    uuid_val: uuid.UUID = uuid.UUID("07cd8bc6-734d-43da-84e7-6084990becfc")
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuJoinCommand(
            app_uuid=uuid_val,
            my_name="dave",
            platform=ApiPlatform.ARDUINO,
            api_version=101,
            serial_number=999999999,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.JOIN.value,
        "NM=dave|UU=07cd8bc6-734d-43da-84e7-6084990becfc|VE=101|PF=0|US=999999999|\u0002",
    )


def test_write_large_num_boot_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuLargeNumBootCommand(
            sub_menu_id=10,
            menu_item=DomainFixtures.a_large_number(name="largeNum", item_id=111, dp=4, negative=True),
            current_value=1,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.LARGE_NUM_BOOT_ITEM.value,
        "PI=10|ID=111|IE=64|NM=largeNum|RO=0|VI=1|FD=4|NA=1|ML=12|VC=1.0000|\u0002",
    )


def test_write_bootstrap():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuBootstrapCommand(boot_type=MenuBootstrapCommand.BootType.START),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOTSTRAP.value,
        "BT=START|\u0002",
    )


def test_write_analog_item():
    out_buffer = io.BytesIO()
    analog_item = DomainFixtures.an_analog_item(name="Test", item_id=123)
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuAnalogBootCommand(sub_menu_id=321, menu_item=analog_item, current_value=25),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.ANALOG_BOOT_ITEM.value,
        "PI=321|ID=123|IE=104|NM=Test|RO=0|VI=1|AO=102|AD=2|AM=255|AS=1|AU=dB|VC=25|\u0002",
    )
    out_buffer = io.BytesIO()
    analog_item_with_step = replace(analog_item, step=2)
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuAnalogBootCommand(sub_menu_id=321, menu_item=analog_item_with_step, current_value=-22222),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.ANALOG_BOOT_ITEM.value,
        "PI=321|ID=123|IE=104|NM=Test|RO=0|VI=1|AO=102|AD=2|AM=255|AS=2|AU=dB|VC=-22222|\u0002",
    )


def test_write_enum_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuEnumBootCommand(
            sub_menu_id=22, menu_item=DomainFixtures.an_enum_item(name="Test", item_id=2), current_value=1
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.ENUM_BOOT_ITEM.value,
        "PI=22|ID=2|IE=101|NM=Test|RO=0|VI=1|VC=1|NC=2|CA=Item1|CB=Item2|\u0002",
    )


def test_write_submenu():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuSubBootCommand(
            sub_menu_id=22, menu_item=DomainFixtures.a_sub_menu(name="Sub", item_id=1), current_value=False
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.SUBMENU_BOOT_ITEM.value,
        "PI=22|ID=1|IE=102|NM=Sub|RO=0|VI=1|VC=0|\u0002",
    )


def test_write_boolean_item_true_false():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuBooleanBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_boolean_menu(
                name="Bool", item_id=1, naming=BooleanMenuItem.BooleanNaming.TRUE_FALSE
            ),
            current_value=False,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOLEAN_BOOT_ITEM.value,
        "PI=22|ID=1|IE=102|NM=Bool|RO=0|VI=1|BN=0|VC=0|\u0002",
    )


def test_write_boolean_item_on_off():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuBooleanBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_boolean_menu(
                name="Bool", item_id=1, naming=BooleanMenuItem.BooleanNaming.ON_OFF
            ),
            current_value=True,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOLEAN_BOOT_ITEM.value,
        "PI=22|ID=1|IE=102|NM=Bool|RO=0|VI=1|BN=1|VC=1|\u0002",
    )


def test_write_boolean_item_yes_no():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuBooleanBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_boolean_menu(
                name="Bool", item_id=1, naming=BooleanMenuItem.BooleanNaming.YES_NO
            ),
            current_value=True,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOLEAN_BOOT_ITEM.value,
        "PI=22|ID=1|IE=102|NM=Bool|RO=0|VI=1|BN=2|VC=1|\u0002",
    )


def test_write_boolean_item_checkbox():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuBooleanBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_boolean_menu(
                name="Bool", item_id=1, naming=BooleanMenuItem.BooleanNaming.CHECKBOX
            ),
            current_value=True,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOLEAN_BOOT_ITEM.value,
        "PI=22|ID=1|IE=102|NM=Bool|RO=0|VI=1|BN=3|VC=1|\u0002",
    )


def test_write_float_item():
    out_buffer = io.BytesIO()
    item: FloatMenuItem = replace(
        DomainFixtures.a_float_menu(name="FloatMenu", item_id=1),
        visible=False,
    )
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuFloatBootCommand(
            sub_menu_id=22,
            menu_item=item,
            current_value=12.0,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.FLOAT_BOOT_ITEM.value,
        "PI=22|ID=1|IE=105|NM=FloatMenu|RO=0|VI=0|FD=3|VC=12.0|\u0002",
    )


def test_write_runtime_list_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuRuntimeListBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_runtime_list_menu(name="List", item_id=1, rows=2),
            current_value=("ABC", "DEF"),
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.RUNTIME_LIST_BOOT.value,
        "PI=22|ID=1|IE=88|NM=List|RO=0|VI=1|NC=2|CA=ABC|CB=DEF|\u0002",
    )


def test_write_action_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuActionBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.an_action_menu(name="Action", item_id=1),
            current_value=False,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.ACTION_BOOT_ITEM.value,
        "PI=22|ID=1|IE=20|NM=Action|RO=0|VI=1|VC=|\u0002",
    )


def test_write_text_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=MenuTextBootCommand(
            sub_menu_id=22,
            menu_item=DomainFixtures.a_text_menu(name="TextItem", item_id=1),
            current_value="ABC",
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.TEXT_BOOT_ITEM.value,
        "PI=22|ID=1|IE=101|NM=TextItem|RO=0|VI=1|ML=10|EM=0|VC=ABC|\u0002",
    )


def test_write_an_absolute_change():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_absolute_menu_change_command(
            correlation_id=CorrelationId.from_string("00134654"), item=2, value=1
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.CHANGE_INT_FIELD.value,
        "IC=00134654|ID=2|TC=1|VC=1|\u0002",
    )


def test_write_a_delta_change():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_delta_menu_change_command(
            correlation_id=CorrelationId.from_string("C04239"), item=2, value=1
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.CHANGE_INT_FIELD.value,
        "IC=00c04239|ID=2|TC=0|VC=1|\u0002",
    )


def test_write_a_list_change():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_absolute_list_menu_change_command(
            correlation_id=CorrelationId.from_string("C04239"), item=2, values=("123", "456")
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.CHANGE_INT_FIELD.value,
        "IC=00c04239|ID=2|TC=2|NC=2|CA=123|CB=456|\u0002",
    )


def test_write_a_list_status_change():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_list_response_menu_change_command(
            correlation_id=CorrelationId.from_string("C04239"), item=2, value=ListResponse.from_string("12343:1")
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.CHANGE_INT_FIELD.value,
        "IC=00c04239|ID=2|TC=3|VC=12343:1|\u0002",
    )


def test_write_ack():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_acknowledgement_command(
            correlation_id=CorrelationId.from_string("1234567a"), status=AckStatus.ID_NOT_FOUND
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.ACKNOWLEDGEMENT.value,
        "IC=1234567a|ST=1|\u0002",
    )


def test_write_pairing():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_pairing_command(
            name="pairingtest", uuid=uuid.UUID("575d327e-fe76-4e68-b0b8-45eea154a126")
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.PAIRING_REQUEST.value,
        "NM=pairingtest|UU=575d327e-fe76-4e68-b0b8-45eea154a126|\u0002",
    )


def test_write_dialog_update():
    out_buffer = io.BytesIO()
    # noinspection PyUnresolvedReferences
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_dialog_command(
            mode=DialogMode.SHOW,
            header="Hello",
            message="Buffer",
            button1=MenuButtonType.NONE,
            button2=MenuButtonType.CLOSE,
            correlation_id=CorrelationId.EMPTY_CORRELATION,
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.DIALOG_UPDATE.value,
        "MO=S|HF=Hello|BU=Buffer|B1=4|B2=3|IC=00000000|\u0002",
    )


def test_write_runtime_rgb_color_item():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_menu_rgb32_boot_command(
            parent_id=0,
            item=Rgb32MenuItem(name="rgb", id=1, include_alpha_channel=True),
            current_value=PortableColor.from_html("#22334455"),
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOT_RGB_COLOR.value,
        "PI=0|ID=1|IE=-1|NM=rgb|RO=0|VI=1|RA=1|VC=#22334455|\u0002",
    )


def test_write_scroll_choice():
    out_buffer = io.BytesIO()
    protocol.to_channel(
        buffer=out_buffer,
        command=CommandFactory.new_menu_scroll_choice_boot_command(
            parent_id=0,
            item=ScrollChoiceMenuItem(name="scroll", id=1, item_width=10, num_entries=20),
            current_value=CurrentScrollPosition(position=1, value="hello"),
        ),
    )
    compare_buffer_against_expected(
        out_buffer,
        MenuCommandType.BOOT_SCROLL_CHOICE.value,
        "PI=0|ID=1|IE=-1|NM=scroll|RO=0|VI=1|WI=10|NC=20|VC=1-hello|\u0002",
    )


def test_send_and_receive_custom_tag_val():
    out_buffer = io.BytesIO()
    spanner_command: MenuSpannerCommand = MenuSpannerCommand(metric_size=15, make="Super Duper")
    protocol.to_channel(
        buffer=out_buffer,
        command=spanner_command,
    )
    out_buffer.seek(0)
    assert MenuCommandProtocol.PROTO_START_OF_MSG == out_buffer.read(1)
    decoded_command: MenuSpannerCommand = protocol.from_channel(out_buffer)
    assert MenuSpannerCommand.SPANNER_MSG_TYPE == decoded_command.command_type
    assert 15 == decoded_command.metric_size
    assert "Super Duper" == decoded_command.make


def test_send_and_receive_custom_bin_data():
    out_buffer = io.BytesIO()
    bin_data_cmd: BinaryDataCommand = BinaryDataCommand(bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    protocol.to_channel(
        buffer=out_buffer,
        command=bin_data_cmd,
    )
    out_buffer.seek(0)
    assert MenuCommandProtocol.PROTO_START_OF_MSG == out_buffer.read(1)
    decoded_command: BinaryDataCommand = protocol.from_channel(out_buffer)
    assert BinaryDataCommand.BIN_DATA_COMMAND == decoded_command.command_type
    assert decoded_command.bin_data == bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def to_buffer(message_type: MessageField, s: str) -> io.BytesIO:
    buffer = io.BytesIO()
    buffer.write(CommandProtocol.TAG_VAL_PROTOCOL.protocol_num)
    buffer.write(message_type.high[0].encode("utf-8"))
    buffer.write(message_type.low[0].encode("utf-8"))
    buffer.write(s.encode("utf-8"))
    buffer.seek(0)  # Resetting the buffer's position to the beginning
    return buffer


def compare_buffer_against_expected(out_buffer: io.BytesIO, expected_msg: MessageField, expected_data: str):
    out_buffer.seek(0)
    expected_data: str = f"\u0001\u0001{expected_msg.high}{expected_msg.low}{expected_data}"

    # Check the actual data is right.
    assert expected_data == out_buffer.getvalue().decode("utf-8")
