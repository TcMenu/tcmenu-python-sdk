import io
import uuid
from typing import Generic, TypeVar

import pytest

from tcmenu.domain.edit_item_type import EditItemType
from tcmenu.domain.menu_items import BooleanMenuItem
from tcmenu.remote.commands.ack_status import AckStatus
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
from tcmenu.remote.protocol.api_platform import ApiPlatform
from tcmenu.remote.protocol.command_protocol import CommandProtocol
from tcmenu.remote.protocol.configurable_protocol_converter import ConfigurableProtocolConverter
from tcmenu.remote.protocol.message_field import MessageField

protocol = ConfigurableProtocolConverter(include_default_processors=True)


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


def to_buffer(message_type: MessageField, s: str) -> io.BytesIO:
    buffer = io.BytesIO()
    buffer.write(CommandProtocol.TAG_VAL_PROTOCOL.protocol_num)
    buffer.write(message_type.high[0].encode("utf-8"))
    buffer.write(message_type.low[0].encode("utf-8"))
    buffer.write(s.encode("utf-8"))
    buffer.seek(0)  # Resetting the buffer's position to the beginning
    return buffer
